#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import json
from redis import Redis
import logging
from Handlers.BaseHandler import BaseHandler
from Handlers.MainHandler import MainHandler
from Handlers.LoginHandler import LoginHandler
from Handlers.LogoutHandler import LogoutHandler
from Handlers.ChatSocketHandler import ChatSocketHandler
from  tornado import escape, ioloop, web, websocket


class Application(web.Application):

    def __init__(self, redis_client: Redis):
        handlers = [
            (r'/', MainHandler),
            (r'/login', LoginHandler,
                dict(redis_client=redis_client)),
            (r'/logout', LogoutHandler),
            (r'/chatsocket/(.*)$', ChatSocketHandler,
                dict(redis_client=redis_client)),
        ]
        settings = {
            'cookie_secret': ''.join([str(uuid.uuid4()) for _ in range(8)]),
            'template_path': './templates',
            'static_path': './static',
            'login_url': '/login',
            'xsrf_cookies': True,
        }
        super(Application, self).__init__(handlers, **settings)


def main():
    tchat_port = '8888'
    redis_client = Redis(host='localhost', port=6379, db=0)
    app = Application(redis_client=redis_client)
    app.listen(port=tchat_port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
