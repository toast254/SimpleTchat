# -*- coding: utf-8 -*-

import logging
from tornado import escape
from Handlers.BaseHandler import BaseHandler
from Tools import Configuration

logger = logging.getLogger(__name__)

(secret_gen_range, try_limit, ban_time) = Configuration.load_security_conf()


class LoginHandler(BaseHandler):
    """Handle user login actions"""

    def failed_auth(self):
        """Increase wrong auth tries counter after a failed authentication"""
        logging.info('invalid credentials from %s', self.request.remote_ip)
        incorrect = self.redis_client.get(self.request.remote_ip)
        self.redis_client.setex(self.request.remote_ip, (int(incorrect) + 1 if incorrect else 1), ban_time)

    def get(self):
        """Get login form"""
        if not self.is_blocked():
            if not self.is_connected():
                self.render('login.html', user=self.current_user)
            else:
                self.redirect('/')

    def post(self):
        """Post connection form and try to connect with these credentials"""
        if not self.is_blocked():
            if not self.is_connected():
                getusername = escape.xhtml_escape(self.get_argument('username'))
                getpassword = escape.xhtml_escape(self.get_argument('password'))
                password = self.redis_client.get('users-' + getusername)
                if password and getpassword == bytes.decode(password):
                    # set user connected cookie
                    self.set_secure_cookie('user', getusername, expires_days=1)
                    # remove wrong auth tries counter
                    self.redis_client.delete(self.request.remote_ip)
                    # connected
                    logger.info('user connected : ' + getusername)
                    # self.set_status(status_code=200)  # default
                    return
                self.failed_auth()
            self.send_error(status_code=400)
