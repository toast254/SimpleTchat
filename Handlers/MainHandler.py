# -*- coding: utf-8 -*-

import logging
from tornado.web import RequestHandler

logger = logging.getLogger(__name__)


class MainHandler(RequestHandler):
    """handle / endpoint"""

    def get(self):
        """Serve Get and return main page"""
        self.render('index.html')
