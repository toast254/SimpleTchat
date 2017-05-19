# -*- coding: utf-8 -*-

import logging
from  tornado import web

logger = logging.getLogger(__name__)


class BaseHandler(web.RequestHandler):
    """Superclass for Handlers which require a connected user"""

    def get_current_user(self):
        """Get current connected user

        :return: current connected user
        """
        return self.get_secure_cookie('user')
