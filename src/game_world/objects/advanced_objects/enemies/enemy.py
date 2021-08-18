from src.game_world.objects.basic_objects import AliveSprite
from src.Consts.settings import *
from src.game_world.objects.collision import CollisionMasks


class BasicEnemy(AliveSprite):
    """
    The Player is the object that the user has control on
    """

    def __init__(self, x, y, obj_width, obj_height, mask, sprite_img: str):
        super().__init__(x, y, obj_width, obj_height, mask, (CollisionMasks.WALLS,), PLAYER_HEALTH, PLAYER_SPEED, PLAYER_POWER,
                             sprite_img=sprite_img)

    def _movement(self):
        pass

    def take_hit(self):
        pass

    def _deal_dmg(self):
        pass

    def update(self):
        self._movement()
        self.collider.update(self.rect.x, self.rect.y)

    def late_update(self):
        self.collider.late_update()
