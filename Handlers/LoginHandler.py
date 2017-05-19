# -*- coding: utf-8 -*-

import logging
from redis import Redis
from tornado import escape
from  Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class LoginHandler(BaseHandler):
    """Handle user login actions.
    """

    def initialize(self, redis_client: Redis):
        """Init this handler, use the given redis client.
        """
        self.redis_client = redis_client

    def get(self):
        """Get login form.
        """
        incorrect = self.redis_client.get(self.request.remote_ip)
        if incorrect and int(incorrect) > 5:
            logging.warning('an user have been blocked')
            self.write('<center>blocked</center>')
            return
        self.render('login.html', user=self.current_user)

    def post(self):
        """Post connection form and try to connect with these credentials.
        """
        getusername = escape.xhtml_escape(self.get_argument('username'))
        getpassword = escape.xhtml_escape(self.get_argument('password'))
        password = self.redis_client.get('users-' + getusername)
        if password and getpassword == bytes.decode(password):
            self.set_secure_cookie('user', getusername, expires_days=1)
            self.redis_client.delete(self.request.remote_ip)
            self.redirect('/')
        else:
            logging.info('invalid credentials')
            incorrect = self.redis_client.get(self.request.remote_ip)
            self.redis_client.setex(self.request.remote_ip,
                (int(incorrect) + 1 if incorrect else 1), 3600 * 24)
            self.render('login.html', user=self.current_user)
