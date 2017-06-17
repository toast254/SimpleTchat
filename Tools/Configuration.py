# -*- coding: utf-8 -*-

import os
import sys
import logging
import configparser

logger = logging.getLogger(__name__)

conf_file = 'simpletchat.conf'

if not os.path.isfile(conf_file):
    logger.error('Configuration file not found : ' + conf_file)
    raise FileNotFoundError

config_parser = configparser.ConfigParser(allow_no_value=True)


def load_server_conf():
    config_parser.read(conf_file)
    section = 'SERVER'
    if section not in config_parser.sections() \
            or 'PORT' not in config_parser[section]:
        print('[ConfigurationError] Invalid "' + section + '" configuration !', file=sys.stderr)
        raise RuntimeError
    port = int(config_parser[section]['PORT'])
    return port


def load_redis_conf():
    config_parser.read(conf_file)
    section = 'REDIS'
    if section not in config_parser.sections() \
            or 'HOST' not in config_parser[section] \
            or 'PORT' not in config_parser[section]:
        print('[ConfigurationError] Invalid "' + section + '" configuration !', file=sys.stderr)
        raise RuntimeError
    host = config_parser[section]['HOST']
    port = int(config_parser[section]['PORT'])
    return host, port


def load_security_conf():
    config_parser.read(conf_file)
    section = 'SECURITY'
    if section not in config_parser.sections() \
            or 'SECRET_GEN_RANGE' not in config_parser[section] \
            or 'TRY_LIMIT' not in config_parser[section] \
            or 'BAN_TIME' not in config_parser[section]:
        print('[ConfigurationError] Invalid "' + section + '" configuration !', file=sys.stderr)
        raise RuntimeError
    secret_gen_range = int(config_parser[section]['SECRET_GEN_RANGE'])
    try_limit = int(config_parser[section]['TRY_LIMIT'])
    ban_time = int(config_parser[section]['BAN_TIME'])
    return secret_gen_range, try_limit, ban_time
