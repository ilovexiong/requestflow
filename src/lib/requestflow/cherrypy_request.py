import urlparse

class CherrypyRequest(object):
    """
    Wrapper for cherrypy request object
    """

    def __init__(self, request):
        self._request = request

    @property
    def args(self):
        return urlparse.parse_qs(self._request.query_string)

    @property
    def form(self):
        return self._request.body_params

    @property
    def headers(self):
        return self._request.headers

    @property
    def host(self):
        url_parts = urlparse.urlparse(self._request.base)
        return "{}:{}".format(url_parts.hostname, url_parts.port)

    @property
    def method(self):
        return self._request.method

    @property
    def path(self):
        return self._request.path_info

    @property
    def url(self):
        return '{}{}?{}'.format(self._request.base, self._request.path_info, self._request.query_string)
