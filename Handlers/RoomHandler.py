# -*- coding: utf-8 -*-

import logging
from tornado.web import authenticated
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class RoomHandler(BaseHandler):
    """handle / endpoint"""

    @authenticated
    def get(self):
        """Serve Get and return main page"""
        self.render('room.html')
