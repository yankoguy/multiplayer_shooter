from abc import ABC, abstractmethod, ABCMeta


class MetaNetworkObject(ABCMeta):
    """
    If there is more then one one of the same network object he will become online object
    """
    __instances = {}

    def __call__(cls, *args, **kwargs):
        network_object = super(MetaNetworkObject, cls).__call__(*args, **kwargs)

        if cls in cls.__instances:
            network_object._online_object = True # If there is another object he will be online object

        cls.__instances[cls] = network_object

        return network_object


class NetworkObject(ABC, metaclass=MetaNetworkObject):
    """
    Each object that is affected by the server should inhire from this class
    """

    @abstractmethod
    def __init__(self):
        self._online_object = False  # If this attribute is true this means that the object controled by the server
                                    # The object is not online by deafult

