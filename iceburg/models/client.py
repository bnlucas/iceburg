import logging
import time

import requests
import requests_cache

from iceburg import config
from iceburg.compat import string_type
from iceburg.utils import encode, formats


class Client(object):

    def __init__(self, debug=False):
        self.debug = debug
        self._last = None

        self.headers = {}

        if config.cache:
            self.session = requests_cache.CachedSession(**config.cache)
        else:
            self.session = requests.session()

    def request(self, method, url, path=(), extension=None, params={},
                headers={}, data=None, debug=None, silent=False,
                ignore_cache=False, data_format='json', delay=0.0, **kwargs):
        if debug is None:
            debug = self.debug

        _req = _res = data_format

        if type(data_format) in (list, tuple) and (len(data_format) == 2):
            _req = data_format[0]
            _res = data_format[1]

        if _req and (data is not None):
            data = formats.compose(_req, data)

            content_type = formats.meta(_req).get('content_type')
            headers.setdefault('Content-Type', content_type)

        self.headers.update(headers)

        if not isinstance(path, string_type):
            path = '/'.join(path)

        if extension is None:
            extension = ''
        elif not extension.startswith('.'):
            extension = '.{0}'.format(extension)

        url = '{0}{1}{2}'.format(url, path, extension)

        if delay > 0:
            elapsed = time.time() - self._last

            if elapsed < delay:
                time.sleep(delay - elapsed)

        params.update(**kwargs)

        if ignore_cache:
            with self.session.cache_disabled():
                results = self.session.request(method, url, params=params,
                                               headers=self.headers, data=data)
        else:
            results = self.session.request(method, url, params=params,
                                           headers=self.headers, data=data)

        self._last = time.time()

        try:
            results.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(e.message)

            if silent:
                return None

            raise e

        try:
            response = None

            if len(results.text) > 0:
                response = formats.parse(_res, results.text)
        except ValueError as e:
            if silent:
                return None

            raise e

        if len(results.text) > 0:
            return encode(response)

        return None
