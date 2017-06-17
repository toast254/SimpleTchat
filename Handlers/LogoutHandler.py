# -*- coding: utf-8 -*-

import logging
from tornado.web import authenticated
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class LogoutHandler(BaseHandler):
    """Handle user logout action"""

    @authenticated
    def get(self):
        """Disconnect an user, delete his cookie and redirect him"""
        logger.info('user connected : ' + self.get_current_user().decode())
        self.clear_cookie('user')
        self.redirect('/')
