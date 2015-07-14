import unittest
from tests.end_to_end.forecastserver import ForecastServer
import src.forecast.webservice as webservice
import requests


class TestForecastEndToEnd(unittest.TestCase):

    def setUp(self):
        # Start the forecast server
        self.server = ForecastServer()
        self.server.start(webservice.app)

    def tearDown(self):
        # Stop the forecast server
        self.server.stop()

    def test_webservice_receives_a_request(self):
        response = requests.get('http://localhost:8000')
        print(response.text)


if __name__ == '__main__':
    unittest.main()
