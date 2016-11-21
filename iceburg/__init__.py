from urlparse import urlparse

from .config import __version__
from models import Client, Wrap
from .utils import sort


def api(url, **kwargs):
    return Wrap(wrap=url, **kwargs)


def delete(url, **kwargs):
	return Wrap(wrap=url, **kwargs).delete()


def get(url, **kwargs):
	return Wrap(wrap=url, **kwargs).get()


def head(url, **kwargs):
	return Wrap(wrap=url, **kwargs).head()


def patch(url, **kwargs):
	return Wrap(wrap=url, **kwargs).patch()


def post(url, **kwargs):
	return Wrap(wrap=url, **kwargs).post()


def put(url, **kwargs):
	return Wrap(wrap=url, **kwargs).put()


def api_info(api):
	return url_info(api.url)


def url_info(url):
	parsed_url = urlparse(url)

	return {
		'url': url,
		'base': '://'.join([parsed_url.scheme, parsed_url.netloc]),
		'path': parsed_url.path,
		'params': parsed_url.params,
		'query': parsed_url.query,
		'fragment': parsed_url.fragment,
		'username': parsed_url.username,
		'password': parsed_url.password,
		'hostname': parsed_url.hostname,
		'port': parsed_url.port
	}
