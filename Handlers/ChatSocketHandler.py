# -*- coding: utf-8 -*-

import uuid
import json
import logging
from redis import Redis
from tornado import escape, websocket, web
from  Handlers.BaseHandler import BaseHandler

logger = logging.getLogger(__name__)


class ChatSocketHandler(websocket.WebSocketHandler, BaseHandler):

    def initialize(self, redis_client: Redis):
        self.redis_client = redis_client
        self.subscrib = redis_client.pubsub()
        self.thread = None

    def get_compression_options(self):
        return {}  # Non "None" enables compression with default options.

    @web.authenticated
    def open(self, path_request):
        self.channel = 'messages' + path_request
        self.subscrib.subscribe(**{self.channel: self.send_updates})
        self.thread = self.subscrib.run_in_thread(sleep_time=0.001)

    def on_close(self):
        self.subscrib.unsubscribe(self.channel)
        self.thread.stop()

    def send_updates(self, chat):
        try:
            self.write_message(chat['data'])
        except websocket.WebSocketClosedError:
            logging.error('Error sending message', exc_info=True)

    def on_message(self, message):
        logging.info('got message %r', message)
        parsed = escape.json_decode(message)
        chat = {
            'id': str(uuid.uuid4()),
            'body': parsed['body'],
        }
        chat['html'] = escape.to_basestring(self.render_string('message.html',
            message=chat))
        self.redis_client.publish(self.channel, json.dumps(chat))
