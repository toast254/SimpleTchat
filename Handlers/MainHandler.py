# -*- coding: utf-8 -*-

import logging
from tornado import web
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class MainHandler(BaseHandler):
    """handle / endpoint"""

    @web.authenticated
    def get(self):
        """Serve Get and return main page"""
        self.render('index.html', messages=[])
