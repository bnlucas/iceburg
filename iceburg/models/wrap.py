import six

from iceburg.compat import string_type
from .client import Client


class Wrap(object):

    def __init__(self, wrap, cover=None, headers=None, params=None, debug=None,
                 silent=False, extension=None, data_format=None, delay=None):
        self._url = None
        self._cover = cover or Client(debug=debug)

        if isinstance(wrap, string_type):
            self._wrap = wrap[:-1] if wrap[-1:] == '/' else wrap
        else:
            self._wrap = str(wrap)

        self.config = {
            'headers': headers if headers else {},
            'params': params if params else {},
            'debug': debug,
            'silent': silent,
            'extension': extension,
            'data_format': data_format,
            'delay': delay,
            'url': wrap
        }

    def __str__(self):
        return self.url

    def __repr__(self):
        return '<{0} - {1}>'.format(self.__class__.__name__, self.url)

    def __call__(self, *wraps, **kwargs):
        self.config.update(**kwargs)

        if len(wraps) == 0:
            return self

        cover = self

        for wrap in wraps:
            try:
                cover = cover.__dict__[wrap]
            except KeyError:
                cover.__dict__[wrap] = Wrap(wrap=wrap, cover=cover)
                cover = cover.__dict__[wrap]

        return cover

    def __getattr__(self, wrap):
        try:
            return self.__dict__[wrap]
        except KeyError:
            self.__dict__[wrap] = Wrap(wrap=wrap, cover=self,
                                       debug=self.config['debug'])
            return self.__dict__[wrap]

    @property
    def url(self):
        if not self._url:
            try:
                self._url = '/'.join([self._cover.url, self._wrap])
            except:
                self._url = self._wrap

        return self._url

    def request(self, method, *wraps, **kwargs):
        if len(wraps) != 0:
            return self.__call__(*wraps).request(method=method, **kwargs)

        if 'url' not in kwargs:
            kwargs['url'] = self.url

        if 'params' in kwargs:
            kwargs['params'].update(self.config['params'])

        for k, v in six.iteritems(self.config):
            if v is not None:
                if not isinstance(v, dict):
                    kwargs.setdefault(k, v)
                    continue

                tmp = v.copy()

                if kwargs.get(k):
                    tmp.update(kwargs[k])

                kwargs[k] = tmp

        return self._cover.request(method=method, **kwargs)

    def delete(self, *wraps, **kwargs):
        return self.request('DELETE', *wraps, **kwargs)

    def get(self, *wraps, **kwargs):
        return self.request('GET', *wraps, **kwargs)

    def head(self, *wraps, **kwargs):
        return self.request('HEAD', *wraps, **kwargs)

    def patch(self, *wraps, **kwargs):
        return self.request('PATCH', *wraps, **kwargs)

    def post(self, *wraps, **kwargs):
        return self.request('POST', *wraps, **kwargs)

    def put(self, *wraps, **kwargs):
        return self.request('PUT', *wraps, **kwargs)
