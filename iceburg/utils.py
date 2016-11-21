import operator
import urllib

from math import ceil, floor

import requests_cache
import six

from formats import FormatBank, discover_json, discover_yaml


formats = FormatBank()

discover_json(formats, content_type='application/json')
discover_yaml(formats, content_type='application/x-yaml')


def sort(items, key, reverse=False):
    tmp = []

    for i in items:
        tmp.append((i[key], i))

    tmp.sort(key=operator.itemgetter(0), reverse=reverse)

    return [i[1] for i in tmp]


def encode(data, encoding='utf8', *errors):
    if isinstance(data, dict):
        return {encode(k): encode(v) for k, v in six.iteritems(data)}

    if isinstance(data, list):
        return [encode(i) for i in data]

    if isinstance(data, unicode):
        return data.encode(encoding, *errors)

    return data


def build_query_string(params):
    if (not isinstance(params, dict)) or params == {}:
        return None

    param = lambda k, v: '='.join([k, str(v)])

    return '&'.join([param(k, v) for k, v in six.iteritems(params)])


def build_url(url, params=None):
    if params is None:
        return url

    return '?'.join([url, build_query_string(params)])


def clear_cache(config):
    session = requests_cache.CachedSession(**config)
    return session.cache.clear()
