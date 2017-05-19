# -*- coding: utf-8 -*-

import logging
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class LogoutHandler(BaseHandler):
    """Handle user logout action"""

    def get(self):
        """Disconnect an user, delete his cookie and redirect him"""
        self.clear_cookie('user')
        self.redirect('/')
