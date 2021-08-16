"""
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        print(cls._instances)
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    @classmethod
    def margherita(cls):
        return cls()

class Logger2(metaclass=Singleton):
    pass


l=Logger()
l.margherita()
"""

"""
class EventListener:
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
            #[handler(event_information) for handler in cls.handlers.get(handler_name)]


def event_handle(func):
    def wrapper(*args, **kwargs):
        func(*args)
    return wrapper


class mouse:
    def click(self):
        print("mosue clicked")
        EventListener.fire_events("A",23,1)


@event_handle
def handle_a(x, y):
    print(x,y)


def handle_b():
    print('b')
    

def handle_c():
    print('c')


def handle_d():
    print('d')


EventListener.add_handler("A", handle_a)
EventListener.add_handler("B", handle_b)
EventListener.add_handler("C", handle_c)
EventListener.add_handler("D", handle_d)

n = mouse()
n.click()
n.click()

n.click()
"""

