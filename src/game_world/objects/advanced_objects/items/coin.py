from src.game_world.objects.basic_objects import Sprite
from src.Consts.settings import *
from src.game_world.objects.collision import CollisionMasks


class Coin(Sprite):
    """
    Coin is an object that represen money
    """
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, color=WHITE,
                 sprite_img: str = None):
        super().__init__(x, y, obj_width, obj_height, obj_width, obj_height, CollisionMasks.COLLECTABLE, (CollisionMasks.PLAYER,), color=color)

        self.__money = 5  # How much money does the coin contains



    def late_update(self):
        if self.collider.collision is not None:
            # If collides with Player
            self.collider.collision.item_collector.add_item(COINS, self.__money)
            self._destroy()

        super().late_update()