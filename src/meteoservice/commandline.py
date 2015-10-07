from .client import Client
from .client import DispatcherFactory


class App:

    def __init__(self, wsconsumer):
        self._wsconsumer = wsconsumer

    @property
    def wsconsumer(self):
        return self._wsconsumer

    def main(self):
        bootstrap(self)
        self._wsconsumer.temperature()

    @staticmethod
    def data_received_handler(event):
        temperature = event.data['temperature']
        print('{} ℃'.format(temperature))


def bootstrap(app):
    app.wsconsumer.register_handler('DataReceivedEvent',
                                    app.data_received_handler)
