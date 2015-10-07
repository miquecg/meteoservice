import pytest
import re
from server import Server

from meteoservice.client import Client
from meteoservice.client import DispatcherFactory
from meteoservice.commandline import App
from meteoservice.webservice import WebService


# noinspection PyUnresolvedReferences
@pytest.fixture(autouse=True)
def setupserver(request):
    """Starts a new web service for each test"""
    server = Server()
    server.start(WebService())

    request.addfinalizer(server.stop)


def test_temperature_for_tomorrow_in_vigo(capsys):
    wsclient = Client(DispatcherFactory)
    app = App(wsclient)

    app.main()

    out, err = capsys.readouterr()
    pattern = r'-?\d{1,2} ℃'
    assert re.match(pattern, out)
