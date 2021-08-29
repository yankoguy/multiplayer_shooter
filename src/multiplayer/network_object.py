from abc import ABC, abstractmethod, ABCMeta
from collections import defaultdict



class MetaNetworkObject(ABCMeta):
    """
    If there is more then one one of the same network object he will become online object
    """
    __instances = defaultdict(lambda: [])

    def __call__(cls, *args, **kwargs):

        network_object = super(MetaNetworkObject, cls).__call__(*args, **kwargs)

        network_object._network_id = len(cls.__instances[cls])
        cls.__instances[cls].append(network_object)

        return network_object

class NetworkObject(ABC,metaclass=MetaNetworkObject):
    """
    Each object that is affected by the server should inhire from this class
    """

    @abstractmethod
    def __init__(self,is_online=False):
        self._online_object = is_online  # If this attribute is true this means that the object controled by the server
                                    # The object is not online by deafult
        self._network_id = 0
