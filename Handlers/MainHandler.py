# -*- coding: utf-8 -*-

import logging
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class MainHandler(BaseHandler):
    """handle / endpoint"""

    def get(self):
        """Serve Get and return main page"""
        if self.is_connected():
            self.redirect('/room')
            return
        self.render('index.html')
