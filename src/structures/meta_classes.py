from abc import ABCMeta
from src.custom_exception.exception import SingletonException


class Singleton(type):
    """
    Every class which has only one instance should define its meta class as this class in order to prevent multiple instances
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            raise SingletonException
        else:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class SingletonABC(ABCMeta):
    """
    Same as Singleton but also supports abstract methods
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            raise SingletonException(cls)
        else:
            cls._instances[cls] = super(SingletonABC, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

