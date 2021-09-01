from src.structures.meta_classes import Singleton
from src.game_world.UI.ui_enteties import Text
from src.core_functionaletize.event_system import EventListener
from src.Consts.settings import *
from src.game_world.objects.basic_objects import Sprite
from src.game_world.objects.collision import CollisionMasks
from enum import Enum



class ItemTypes(Enum):
    COINS = 0
    AMMO = 1

class ItemCollector:
    """
    A class that stores all the items the player has
    """
    AMOUNT_INDEX = 0
    TEXT_INDEX = 1

    def __init__(self):
        self.__items = {ItemTypes.COINS: [STARTING_COINS, Text(WINDOW_WIDTH / 2, 0, "coins: ", str(STARTING_COINS), 20)],
                        ItemTypes.AMMO: [STARTING_AMMO, Text(WINDOW_WIDTH / 6 * 5, 40, "ammo: ", str(STARTING_AMMO), 20)]}

    @property
    def items(self):
        return self.__items

    def add_item(self, item_name, amount):
        self.__items[item_name][ItemCollector.AMOUNT_INDEX] += amount
        self.__update_text(item_name, self.__items[item_name][ItemCollector.AMOUNT_INDEX])

    def set_item(self, item, amount):
        self.__items[item][ItemCollector.AMOUNT_INDEX] = amount
        self.__update_text(item, self.__items[item][ItemCollector.AMOUNT_INDEX])

    def __update_text(self, item_to_update, new_text):
        self.__items[item_to_update][ItemCollector.TEXT_INDEX].change_text(str(new_text))


class Item(Sprite):
    """
    Item is a collacteable object in the game which has an amount of him
    amount - how much of this object you will get if you collacte with it
    """
    def __init__(self, x: int, y: int, collider_width: int, coliider_height: int, amount: int, __item_name:ItemTypes ,sprite_img: str):
        super().__init__(x, y, collider_width, coliider_height, CollisionMasks.COLLECTABLE, (CollisionMasks.PLAYER,),sprite_img=sprite_img)

        self.__amount = amount  # How much money does the coin contains
        self.__item_name = __item_name

    def late_update(self):
        if self.collider.collision is not None:
            # If collides with Player
            self.collider.collision.pick_item(self.__item_name, self.__amount)
            self.destroy()
        super().late_update()