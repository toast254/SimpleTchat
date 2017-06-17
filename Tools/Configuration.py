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
config_parser.read(conf_file)


def load_server_conf():
    section = 'SERVER'
    if section not in config_parser.sections() \
            or 'PORT' not in config_parser[section]:
        print('[ConfigurationError] Invalid "' + section + '" configuration !', file=sys.stderr)
        raise RuntimeError
    port = int(config_parser[section]['PORT'])
    logger.debug(section + ' configuration loaded : ' + str(port))
    return port


def load_redis_conf():
    section = 'REDIS'
    if section not in config_parser.sections() \
            or 'HOST' not in config_parser[section] \
            or 'PORT' not in config_parser[section]:
        print('[ConfigurationError] Invalid "' + section + '" configuration !', file=sys.stderr)
        raise RuntimeError
    host = config_parser[section]['HOST']
    port = int(config_parser[section]['PORT'])
    logger.debug(section + ' configuration loaded : ' + str((host, port)))
    return host, port


def load_security_conf():
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
    logger.debug(section + ' configuration loaded : ' + str((secret_gen_range, try_limit, ban_time)))
    return secret_gen_range, try_limit, ban_time


def load_signup_conf():
    section = 'SIGNUP'
    if section not in config_parser.sections() \
            or 'USERNAME_MIN_LEN' not in config_parser[section] \
            or 'USERNAME_MAX_LEN' not in config_parser[section] \
            or 'PASSWD_MIN_LEN' not in config_parser[section] \
            or 'PASSWD_MAX_LEN' not in config_parser[section]:
        print('[ConfigurationError] Invalid "' + section + '" configuration !', file=sys.stderr)
        raise RuntimeError
    user_min_len = int(config_parser[section]['USERNAME_MIN_LEN'])
    user_max_len = int(config_parser[section]['USERNAME_MAX_LEN'])
    passwd_min_len = int(config_parser[section]['PASSWD_MIN_LEN'])
    passwd_max_len = int(config_parser[section]['PASSWD_MAX_LEN'])
    logger.debug(section + ' configuration loaded : ' + str((user_min_len, user_max_len,
                                                             passwd_min_len, passwd_max_len)))
    return user_min_len, passwd_min_len, user_max_len, passwd_max_len
