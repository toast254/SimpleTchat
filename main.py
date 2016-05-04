#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
import string
import random
import uuid
import json
import redis


class Application(tornado.web.Application):

    def __init__(self, redis_client: redis.Redis):
        handlers = [
            (r'/', MainHandler),
            (r'/login', LoginHandler, dict(redis_client=redis_client)),
            (r'/logout', LogoutHandler),
            (r'/chatsocket/(.*)$', ChatSocketHandler, dict(redis_client=redis_client)),
        ]
        settings = {
            'cookie_secret': ''.join([random.choice(string.printable) for _ in range(64)]),
            'template_path': './templates',
            'static_path': './static',
            'login_url': '/login',
            'xsrf_cookies': True,
        }
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    """Superclass for Handlers which require a connected user
    """
    def get_current_user(self):
        """Get current connected user

        :return: current connected user
        """
        return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
    """Handle user login actions
    """
    def initialize(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def get(self):
        """Get login form
        """
        incorrect = self.get_secure_cookie('incorrect')
        if incorrect and int(incorrect) > 5:
            logging.warning('an user have been blocked')
            self.write('<center>blocked</center>')
            return
        self.render('login.html', user=self.current_user)

    def post(self):
        """Post connection form and try to connect with these credentials
        """
        getusername = tornado.escape.xhtml_escape(self.get_argument('username'))
        getpassword = tornado.escape.xhtml_escape(self.get_argument('password'))
        if getpassword == bytes.decode(self.redis_client.get('users-' + getusername)):
            self.set_secure_cookie("user", getusername, expires_days=1)
            self.set_secure_cookie("incorrect", "0")
            self.redirect('/')
        else:
            logging.info('invalid credentials')
            incorrect = self.get_secure_cookie('incorrect')
            if not incorrect:
                incorrect = 0
            self.set_secure_cookie('incorrect', str(int(incorrect) + 1), expires_days=1)
            self.render('login.html', user=self.current_user)


class LogoutHandler(BaseHandler):
    """Handle user logout action
    """
    def get(self):
        """Disconnect an user, delete his cookie and redirect him
        """
        self.clear_cookie('user')
        self.redirect('/')


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('index.html', messages=[])


class ChatSocketHandler(tornado.websocket.WebSocketHandler, BaseHandler):

    def initialize(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.subscrib = redis_client.pubsub()
        self.thread = None

    def get_compression_options(self):
        return {}  # Non-None enables compression with default options.

    @tornado.web.authenticated
    def open(self, path_request):
        self.channel = 'messages' + path_request
        self.subscrib.subscribe(**{self.channel: self.send_updates})
        self.thread = self.subscrib.run_in_thread(sleep_time=0.001)

    def on_close(self):
        self.subscrib.unsubscribe(self.channel)
        self.thread.stop()

    def send_updates(self, chat):
        try:
            self.write_message(chat['data'])
        except tornado.websocket.WebSocketClosedError:
            logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
                'id': str(uuid.uuid4()),
                'body': parsed['body'],
            }
        chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', message=chat))
        self.redis_client.publish(self.channel, json.dumps(chat))


def main():
    tchat_port = '8888'
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    #
    app = Application(redis_client=redis_client)
    app.listen(port=tchat_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
