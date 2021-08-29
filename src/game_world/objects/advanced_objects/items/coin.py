from src.game_world.objects.basic_objects import Sprite
from src.Consts.settings import *
from src.game_world.objects.collision import CollisionMasks

class Coin(Sprite):
    """
    Coin is an object that represen money
    """
    def __init__(self, x: int, y: int, collider_width: int, coliider_height: int,sprite_img: str):
        super().__init__(x, y, collider_width, coliider_height, CollisionMasks.COLLECTABLE, (CollisionMasks.PLAYER,),sprite_img=sprite_img)

        self.__money = 5  # How much money does the coin contains



    def late_update(self):
        if self.collider.collision is not None:
            # If collides with Player
            self.collider.collision.item_collector.add_item(COINS, self.__money)
            self.destroy()
        super().late_update()