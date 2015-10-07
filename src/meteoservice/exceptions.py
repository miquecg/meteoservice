class EventNotInitialized(AttributeError):
    """Raised when a dispatcher doesn't define what event is going to fire"""


class HandlerNotCallable(TypeError):
    """Raised if the handler to be registered isn't of a callable type"""


class EmptyClient(TypeError):
    """Raised when the client doesn't have any handler"""


class EventUnknown(KeyError):
    """Raised for events without handler"""


class NoDispatcherForStatusCode(KeyError):
    """Raised during the creation of a dispatcher if the status code was not set
    in the factory
    """
