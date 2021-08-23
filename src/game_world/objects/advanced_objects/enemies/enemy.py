from src.game_world.objects.basic_objects import AliveSprite
from src.Consts.settings import *
from src.game_world.objects.collision import CollisionMasks
from src.core_functionaletize.game_time import GlobalTime

class BasicEnemy(AliveSprite):
    """
    An enemy that chase the player
    """

    def __init__(self, x, y, obj_width, obj_height, target:object, sprite_img: str):
        super().__init__(x, y, obj_width, obj_height,obj_width, obj_height-15, CollisionMasks.ENEMY, (CollisionMasks.PLAYER,), PLAYER_HEALTH, BASE_ENEMY_SPEED,
                         PLAYER_POWER,
                         sprite_img=sprite_img)
        self.__target = target # Where the enemy should go
        self._vx, self._vy = 0,0 # The velocity of the enemy

    def _calculate_velocity(self):
        if self.collider.collision is None:
            # Move until you reach player (collide with him)
            x_offset = self.__target.rect.x - self.rect.x
            y_offset = self.__target.rect.y - self.rect.y

            offset_sum = abs(x_offset)+abs(y_offset)

            if offset_sum !=0:
                self._vx +=  x_offset/offset_sum * self._speed * GlobalTime.delta_time()
                self._vy +=  y_offset/offset_sum * self._speed * GlobalTime.delta_time()


    def late_update(self):
        self._calculate_velocity()
        self._movement()
        super().late_update()