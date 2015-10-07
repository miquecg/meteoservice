import json
from wsgi_intercept import add_wsgi_intercept
from wsgi_intercept import requests_intercept


class WSGIProxy:

    def __init__(self, host='localhost', port=8000, deserialized_content=None):
        self._host = host
        self._port = port

        if not deserialized_content:
            deserialized_content = {}

        self._content = deserialized_content

    def __enter__(self):
        requests_intercept.install()
        add_wsgi_intercept(self._host, self._port, self)

        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        requests_intercept.uninstall()

    # noinspection PyUnusedLocal
    def __call__(self, *args, **kwargs):
        # noinspection PyUnusedLocal
        def app(environ, start_response):
            start_response('200 OK',
                           [('Content-Type', 'application/json; charset=utf-8')]
                           )

            return [json.dumps(self._content).encode('utf-8')]

        return app
