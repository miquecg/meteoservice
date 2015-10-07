from abc import ABCMeta

from .exceptions import EmptyClient
from .exceptions import EventNotInitialized
from .exceptions import EventUnknown
from .exceptions import HandlerNotCallable
from .exceptions import NoDispatcherForStatusCode
import requests


class Client:

    def __init__(self, dispatcher_factory):
        self._factory = dispatcher_factory
        self._handlers = {}

    def temperature(self):
        response = requests.get('http://localhost:8000')
        dispatcher = self._factory.make_dispatcher(response.status_code,
                                                   response.json())
        dispatcher.fire_event(self)

    def register_handler(self, event_name, handler):
        if not callable(handler):
            raise HandlerNotCallable('Handlers must be of a callable type')

        self._handlers[event_name] = handler

    def __getitem__(self, event):
        if not self._handlers:
            raise EmptyClient('Register some handlers first')

        try:
            return self._handlers[event.name]
        except KeyError as e:
            raise EventUnknown(event.name + " doesn't have a handler") from e


class ClientEvent(metaclass=ABCMeta):

    @property
    def name(self):
        return type(self).__name__


class DataReceivedEvent(ClientEvent):

    def __init__(self, temperature):
        self.data = {
            'temperature': temperature
        }


class DispatcherFactory:

    _dispatchers = {}

    @classmethod
    def add_factory(cls, status_code):
        def decorator(dispatcher_class):
            cls._dispatchers[status_code] = dispatcher_class

            return dispatcher_class

        return decorator

    @classmethod
    def make_dispatcher(cls, status_code, content):
        try:
            return cls._dispatchers[status_code](content)
        except KeyError as e:
            raise NoDispatcherForStatusCode('Add a factory for status code ' +
                                            str(status_code)) from e


class BaseDispatcher(metaclass=ABCMeta):

    def fire_event(self, wsconsumer):
        # Issues mocking __call__
        # See: https://github.com/has207/flexmock/issues/109
        try:
            # noinspection PyUnresolvedReferences
            return wsconsumer[self._event].__call__(self._event)
        except AttributeError as e:
            raise EventNotInitialized(type(self).__name__ +
                                      " hasn't defined the event to fire") \
                from e


@DispatcherFactory.add_factory(status_code=200)
class DataDispatcher(BaseDispatcher):

    def __init__(self, content):
        self._event = DataReceivedEvent(temperature=content['temperature'])
