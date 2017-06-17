# -*- coding: utf-8 -*-

import logging
from tornado import escape
from Tools import Configuration
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)

(secret_gen_range, try_limit, ban_time) = Configuration.load_security_conf()
(user_min_len, passwd_min_len, user_max_len, passwd_max_len) = Configuration.load_signup_conf()


def verify_form(form_data: tuple):
    """Verify form data, ensure the defined policy"""
    (getusername, getpassword) = form_data
    if getusername and getpassword \
            and user_min_len <= len(getusername) <= user_max_len \
            and passwd_min_len <= len(getpassword) <= passwd_max_len:
        return True
    return False


class RegisterHandler(BaseHandler):
    """Handle user register actions"""

    def get(self):
        """Get login form"""
        if not self.is_blocked():
            if not self.is_connected():
                self.render('register.html', user=self.current_user)
            else:
                self.redirect('/')

    def post(self):
        """Post connection form and try to connect with these credentials"""
        if not self.is_blocked():
            if not self.is_connected():
                # get form data
                getusername = escape.xhtml_escape(self.get_argument('username'))
                getpassword = escape.xhtml_escape(self.get_argument('password'))
                # verify form data
                if verify_form((getusername, getpassword)) and not self.redis_client.exists('users-' + getusername):
                    # register
                    self.redis_client.set('users-' + getusername, getpassword)
                    # set user connected cookie
                    self.set_secure_cookie('user', getusername, expires_days=1)
                    # user created
                    logger.info('user created : ' + getusername)
                    self.set_status(status_code=201)
                    return
            # already connected or wrong form data
            self.send_error(status_code=400)
