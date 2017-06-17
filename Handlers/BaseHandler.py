# -*- coding: utf-8 -*-

import logging
from tornado.web import RequestHandler
from Tools import RedisClient, Configuration

logger = logging.getLogger(__name__)

(_, try_limit, ban_time) = Configuration.load_security_conf()


class BaseHandler(RequestHandler):
    """Superclass for Handlers which require a connected user"""

    def get_current_user(self):
        """Get current connected user

        :return: current connected user
        """
        return self.get_secure_cookie('user')

    def initialize(self):
        """Init this handler, init a redis connection"""
        self.redis_client = RedisClient.get_redis_client()

    def is_connected(self):
        """True if the user is connected"""
        return self.get_current_user() and len(self.get_current_user()) > 1

    def is_blocked(self):
        """Send 403 to a blocked ip"""
        incorrect = self.redis_client.get(self.request.remote_ip)
        if incorrect and try_limit < int(incorrect):
            logging.warning('blocked %s', self.request.remote_ip)
            self.send_error(status_code=403)
            self.finish()
            return True
