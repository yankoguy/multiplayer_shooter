class EventListener:
    """
    The EventListener controls all events in game. It lets you to create new events and activate a function you want
    """
    handlers = {}

    @classmethod
    def add_handler(cls, handler_name, handle):
        if handler_name not in cls.handlers.keys():
            cls.handlers[handler_name] = []
        cls.handlers[handler_name].append(handle)

    @classmethod
    def remove_handler(cls, handler_name, handle):
        if cls.handlers.get(handler_name) is not None:
            if handle in cls.handlers[handler_name]:
                cls.handlers[handler_name].remove(handle)
                if cls.handlers.get(handler_name) is []:
                    del cls.handlers[handler_name]

    @classmethod
    def fire_events(cls, handler_name, *event_information):
        if cls.handlers.get(handler_name) is not None:
            for handler in cls.handlers.get(handler_name):
                handler(*event_information)


def event_handle(func):
    """
    A decorator used to check if a function can be handler or not - by checking if it can get arguments.
    """
    def wrapper(*args, **kwargs):
        func(*args)
    return wrapper
