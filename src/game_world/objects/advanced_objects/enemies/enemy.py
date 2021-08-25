from src.game_world.objects.basic_objects import AliveSprite
from src.Consts.settings import *
from src.game_world.objects.collision import CollisionMasks
from src.core_functionaletize.game_time import GlobalTime
import math
from src.core_functionaletize.game_time import Timer

class BasicEnemy(AliveSprite):
    """
    An enemy that chase the player
    """

    def __init__(self, x, y, obj_width, obj_height, targets:list, sprite_img: str):
        super().__init__(x, y, obj_width, obj_height,obj_width, obj_height-15, CollisionMasks.ENEMY, (CollisionMasks.PLAYER,), PLAYER_HEALTH, BASE_ENEMY_SPEED,
                         PLAYER_POWER,
                         sprite_img=sprite_img)
        self._players = targets # Where the enemy should go
        self._vx, self._vy = 0,0 # The velocity of the enemy
        self._attack_timer = Timer(1,self.deal_dmg)

    def _calculate_velocity(self):
        if self.collider.collision is None:
            # Move until you reach player (collide with him)
            target = self._get_closest_target()
            x_offset = target.rect.x - self.rect.x
            y_offset = target.rect.y - self.rect.y

            offset_sum = abs(x_offset)+abs(y_offset)

            if offset_sum !=0:
                self._vx +=  x_offset/offset_sum * self._speed * GlobalTime.delta_time()
                self._vy +=  y_offset/offset_sum * self._speed * GlobalTime.delta_time()

    def deal_dmg(self):
        if self.collider.collision:
            self.collider.collision.take_hit(self._damage)
        self._attack_timer = Timer(1, self.deal_dmg)

    def _get_closest_target(self) -> object:
        """
        Returns the player which is closest to the enemy
        """
        min = math.inf
        closest_player = self._players[0]
        for player in self._players:
            dis = math.dist([self.rect.x,self.rect.y],([player.rect.x,player.rect.y]))
            if min > dis:
                closest_player = player
                min = dis
        return closest_player


    def late_update(self):
        self._calculate_velocity()
        self._movement()
        self._attack_timer.update_timer()

        super().late_update()