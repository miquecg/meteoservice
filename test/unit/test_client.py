from flexmock import flexmock
from proxy import WSGIProxy
import pytest

from meteoservice.client import BaseDispatcher
from meteoservice.client import Client
from meteoservice.client import ClientEvent
from meteoservice.client import DataDispatcher
from meteoservice.client import DataReceivedEvent
from meteoservice.client import DispatcherFactory
from meteoservice.exceptions import EmptyClient
from meteoservice.exceptions import EventNotInitialized
from meteoservice.exceptions import EventUnknown
from meteoservice.exceptions import HandlerNotCallable
from meteoservice.exceptions import NoDispatcherForStatusCode


# noinspection PyMethodMayBeStatic
class TestClient:

    def test_event_is_fired_on_response_from_the_web_service(self):
        with WSGIProxy():
            factory = flexmock()
            dispatcher = flexmock()
            wsconsumer = Client(factory)

            (factory
                .should_receive('make_dispatcher')
                .with_args(int, dict)
                .and_return(dispatcher)
                .once())
            (dispatcher
                .should_receive('fire_event')
                .with_args(wsconsumer)
                .once())

            wsconsumer.temperature()

    def test_retrieve_a_previously_registered_handler(self):
        class MyCoolEvent(ClientEvent):
            pass

        wsconsumer = Client(dispatcher_factory=None)
        wsconsumer.register_handler('MyCoolEvent', lambda: 'yep!')

        assert 'yep!' == wsconsumer[MyCoolEvent()]()

    def test_registering_a_handler_not_callable_causes_an_exception(self):
        wsconsumer = Client(dispatcher_factory=None)

        # noinspection PyUnresolvedReferences
        with pytest.raises(HandlerNotCallable):
            wsconsumer.register_handler(event_name='FinalCountdown',
                                        handler='humble_string')

    def test_event_lookup_fails_when_meteoclient_is_empty(self):
        wsconsumer = Client(dispatcher_factory=None)

        # noinspection PyUnresolvedReferences
        with pytest.raises(EmptyClient):
            wsconsumer[DataReceivedEvent(temperature=23)]()

    def test_exception_is_raised_for_events_without_handler(self):
        class FooEvent(ClientEvent):
            pass

        wsconsumer = Client(dispatcher_factory=None)
        wsconsumer.register_handler('SampleEvent', lambda: None)

        # noinspection PyUnresolvedReferences
        with pytest.raises(EventUnknown):
            wsconsumer[FooEvent()]()


# noinspection PyMethodMayBeStatic
class TestClientEvents:

    def test_events_must_know_their_names(self):
        event = DataReceivedEvent(temperature=5)

        assert 'DataReceivedEvent' == event.name

    def test_datareceivedevent_has_a_temperature_value(self):
        temperature = 21
        event = DataReceivedEvent(temperature)

        assert temperature == event.data['temperature']


# noinspection PyMethodMayBeStatic
class TestDispatchers:

    def test_dispatcher_calls_the_correct_handler_for_the_event(self):
        wsconsumer = flexmock(Client(dispatcher_factory=None))
        handler = flexmock()
        dispatcher = DataDispatcher(content={'temperature': 18})

        (wsconsumer
            .should_receive('__getitem__')
            .with_args(DataReceivedEvent)
            .and_return(handler)
            .once())
        # Issues mocking __call__
        # See: https://github.com/has207/flexmock/issues/109
        (handler
            .should_receive('__call__')
            .with_args(DataReceivedEvent)
            .once())

        dispatcher.fire_event(wsconsumer)

    def test_exception_occurs_when_the_dispatcher_does_not_set_the_event(self):
        class BadDispatcher(BaseDispatcher):
            pass

        dispatcher = BadDispatcher()
        wsconsumer = Client(dispatcher_factory=None)

        # noinspection PyUnresolvedReferences
        with pytest.raises(EventNotInitialized):
            dispatcher.fire_event(wsconsumer)


# noinspection PyMethodMayBeStatic
class TestDispatcherFactory:

    def test_a_dispatcher_can_be_added_to_the_factory_using_a_class_decorator(self):
        class FakeDispatcher(BaseDispatcher):
            def __init__(self, content):
                self.content = content

        decorator = DispatcherFactory.add_factory(status_code=200)

        assert issubclass(decorator(FakeDispatcher), BaseDispatcher)

        message = 'Hello'
        dispatcher = DispatcherFactory.make_dispatcher(status_code=200,
                                                       content=message)

        assert isinstance(dispatcher, FakeDispatcher)
        assert message == dispatcher.content

    def test_making_a_dispatcher_passing_a_status_code_not_set_in_the_factory_raises_an_exception(self):
        # noinspection PyUnresolvedReferences
        with pytest.raises(NoDispatcherForStatusCode):
            DispatcherFactory.make_dispatcher(status_code=404, content=None)
