import json
import logging
import logging.config
import os

from requests_cache import CachedSession


__version__ = '0.1.0'


DEBUG_MAX_TEXT_LENGTH = 100

LOG_PATH = 'logging.json'
LOG_LEVEL = logging.DEBUG


cache = {
    'cache_name': 'cache',
    'backend': 'memory',
    'expires_after': 640800,
    'include_get_headers': True
}


def set_logger(path=LOG_PATH, level=LOG_LEVEL, env_key='LOG_CFG'):
    value = os.getenv(env_key, None)

    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=level)


def logger(path=LOG_PATH, level=LOG_LEVEL, env_key='LOG_CFG'):
    set_logger(path, level, env_key)
