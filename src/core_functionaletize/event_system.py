class EventListener:
    """
    The EventListener controls all events in game. It lets you to create new events and activate a function you want
    """
    __handlers = {}

    @classmethod
    def add_handler(cls, handler_name, handle):
        if handler_name not in cls.__handlers.keys():
            cls.__handlers[handler_name] = []
        cls.__handlers[handler_name].append(handle)

    @classmethod
    def remove_handler(cls, handler_name, handle):
        if cls.__handlers.get(handler_name) is not None:
            if handle in cls.__handlers[handler_name]:
                cls.__handlers[handler_name].remove(handle)
                if cls.__handlers.get(handler_name) is []:
                    del cls.__handlers[handler_name]

    @classmethod
    def fire_events(cls, handler_name, *event_information):
        if cls.__handlers.get(handler_name) is not None:
            for handler in cls.__handlers.get(handler_name):
                handler(*event_information)
