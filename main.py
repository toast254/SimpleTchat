#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import logging
from tornado import ioloop, web
from Handlers.MainHandler import MainHandler
from Handlers.LoginHandler import LoginHandler
from Handlers.LogoutHandler import LogoutHandler
from Handlers.ChatSocketHandler import ChatSocketHandler
from Tools import Configuration

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', filename='simpletchat.log', level=logging.INFO)

server_port = Configuration.load_server_conf()
(secret_gen_range, _, _) = Configuration.load_security_conf()


class Application(web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/chatsocket/(.*)$', ChatSocketHandler),
        ]
        settings = {
            'cookie_secret': ''.join([str(uuid.uuid4()) for _ in range(secret_gen_range)]),
            'template_path': './templates',
            'static_path': './static',
            'login_url': '/login',
            'xsrf_cookies': True,
        }
        super(Application, self).__init__(handlers, **settings)


def main():
    app = Application()
    app.listen(port=server_port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
