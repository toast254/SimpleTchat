# -*- coding: utf-8 -*-

import os
import logging
from redis import Redis

logger = logging.getLogger(__name__)

redis_host = 'localhost'
redis_port = 6379

if 'REDIS_HOST' in os.environ:
    redis_host = os.environ['REDIS_HOST']
if 'REDIS_PORT' in os.environ:
    redis_port = os.environ['REDIS_PORT']


def get_redis_client():
    """Create and return a redis client"""
    logger.debug('new redis client open')
    return Redis(host=redis_host, port=redis_port, db=0)
