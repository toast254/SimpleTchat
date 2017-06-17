# -*- coding: utf-8 -*-

import logging
from tornado import escape
from Tools import RedisClient
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)

try_limit = 5  # 5 failed auth before block
ban_time = 3600 * 24  # 1 day in seconds


class LoginHandler(BaseHandler):
    """Handle user login actions"""

    def initialize(self):
        """Init this handler, init a redis connection"""
        self.redis_client = RedisClient.get_redis_client()

    def is_blocked(self):
        """send 403 to a blocked ip"""
        incorrect = self.redis_client.get(self.request.remote_ip)
        if incorrect and try_limit < int(incorrect):
            logging.warning('blocked %s', self.request.remote_ip)
            self.send_error(status_code=403)
            self.finish()
            return True

    def failed_auth(self):
        """send 401 to a failed authentication"""
        logging.info('invalid credentials from %s', self.request.remote_ip)
        incorrect = self.redis_client.get(self.request.remote_ip)
        self.redis_client.setex(self.request.remote_ip, (int(incorrect) + 1 if incorrect else 1), ban_time)
        self.send_error(status_code=401)
        self.finish()

    def get(self):
        """Get login form"""
        if not self.is_blocked():
            self.render('login.html', user=self.current_user)

    def post(self):
        """Post connection form and try to connect with these credentials"""
        if not self.is_blocked():
            getusername = escape.xhtml_escape(self.get_argument('username'))
            getpassword = escape.xhtml_escape(self.get_argument('password'))
            password = self.redis_client.get('users-' + getusername)
            if not password or getpassword != bytes.decode(password):
                self.failed_auth()
                return
            self.set_secure_cookie('user', getusername, expires_days=1)
            self.redis_client.delete(self.request.remote_ip)
            self.redirect('/')
