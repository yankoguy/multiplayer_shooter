from src.game_world.objects.advanced_objects.items.item_collector import ItemTypes,Item
from src.Consts.settings import *
class Ammo(Item):
    """
    ammo is an object that gives you ammo
    """
    def __init__(self, x: int, y: int, collider_width: int, coliider_height: int):
        super().__init__(x, y, collider_width, coliider_height, 20, ItemTypes.AMMO,AMMO_BOX_IMAGE)
