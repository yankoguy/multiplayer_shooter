from src.structures.core_classes import Singleton
from src.game_world.UI.ui_enteties import Text
from src.core_functionaletize.event_system import EventListener
from src.Consts.settings import *

class ItemCollector(metaclass=Singleton):
    """
    A class that stores all the items the player has
    """
    AMOUNT_INDEX = 0
    TEXT_INDEX = 1

    def __init__(self):
        self.__items = {COINS : [0,Text(1000, 0, "coins: ", str(0), 20)]}
        EventListener.fire_events(WORLD_ADD_OBJECT, self.__items[COINS][ItemCollector.TEXT_INDEX])

    def add_item(self,item,amount):
        print(self.__items[item][ItemCollector.AMOUNT_INDEX],amount)
        self.__items[item][ItemCollector.AMOUNT_INDEX] += amount
        self.__update_text(item,amount)

    def __update_text(self,item_to_update, new_text):
        self.__items[item_to_update][ItemCollector.TEXT_INDEX].change_text(str(new_text))