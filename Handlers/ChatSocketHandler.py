# -*- coding: utf-8 -*-

import uuid
import json
import logging
from Tools import RedisClient
from tornado import escape, websocket, web
from Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class ChatSocketHandler(websocket.WebSocketHandler, BaseHandler):

    def initialize(self):
        """Init this handler, init a redis connection"""
        self.redis_client = RedisClient.get_redis_client()
        self.subscrib = self.redis_client.pubsub()

    def get_compression_options(self):
        return {}  # Non "None" enables compression with default options.

    @web.authenticated
    def open(self, path_request):
        """Websocket opened"""
        self.channel = 'messages' + path_request
        logger.debug('websocket open : ' + self.channel + ' : ' + self.current_user.decode())
        self.subscrib.subscribe(**{self.channel: self.send_updates})
        self.thread = self.subscrib.run_in_thread(sleep_time=0.001)

    def on_close(self):
        """Websocket closed"""
        logger.debug('websocket close : ' + self.channel + ' : ' + self.current_user.decode())
        self.subscrib.unsubscribe(self.channel)
        self.thread.stop()

    def send_updates(self, chat):
        """Websocket send a message"""
        logger.debug('websocket send update : ' + self.channel + ' : ' + self.current_user.decode())
        try:
            self.write_message(chat['data'])
        except websocket.WebSocketClosedError:
            logging.error('Error sending message', exc_info=True)

    def on_message(self, message):
        """Websocket message received"""
        logger.debug('websocket receive update : ' + self.channel + ' : ' + self.current_user.decode())
        parsed = escape.json_decode(message)
        chat = {
            'id': str(uuid.uuid4()),
            'author': self.get_current_user().decode(),
            'body': parsed['body'],
            'timestamp': parsed['timestamp'],
        }
        self.redis_client.publish(self.channel, json.dumps(chat))
