from wsgiref.simple_server import make_server
import multiprocessing


class ForecastServer:

    def __init__(self):
        self._httpd_process = None

    def start(self, webservice):
        if not self._httpd_process:
            httpd = make_server('localhost', 8000, webservice)
            self._httpd_process = multiprocessing.Process(
                target=httpd.serve_forever)
            self._httpd_process.start()

    def stop(self):
        if self._httpd_process:
            self._httpd_process.join()
            self._httpd_process.terminate()

        del self._httpd_process
