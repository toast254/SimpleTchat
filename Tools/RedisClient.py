# -*- coding: utf-8 -*-

from redis import Redis

redis_host = 'localhost'
redis_port = 6379


def get_redis_client():
    """Create and return a redis client"""
    return Redis(host=redis_host, port=redis_port, db=0)
