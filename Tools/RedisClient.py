# -*- coding: utf-8 -*-

import logging
from redis import Redis

logger = logging.getLogger(__name__)

redis_host = 'localhost'
redis_port = 6379


def get_redis_client():
    """Create and return a redis client"""
    logger.debug('new redis client open')
    return Redis(host=redis_host, port=redis_port, db=0)
