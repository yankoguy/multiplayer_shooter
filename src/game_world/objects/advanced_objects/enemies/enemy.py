from src.game_world.objects.basic_objects import AliveSprite
from src.Consts.settings import *
from src.game_world.objects.collision import CollisionMasks
from src.core_functionaletize.game_time import GlobalTime
import math
from src.core_functionaletize.game_time import Timer
from src.game_world.objects.advanced_objects.items.coin import Coin
from src.game_world.objects.advanced_objects.items.ammo import Ammo

from src.core_functionaletize.event_system import EventListener

class BasicEnemy(AliveSprite):
    """
    An enemy that chase the player
    """

    def __init__(self, x, y, collider_width, collider_height, targets:list, sprite_img: str):
        super().__init__(x, y, collider_width, collider_height, CollisionMasks.ENEMY, (CollisionMasks.PLAYER,), PLAYER_HEALTH, BASE_ENEMY_SPEED,
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

    def die(self):
        """
        when dead create ammo and coin
        """
        c = Coin(self.rect.x, self.rect.y, 20, 20)
        EventListener.fire_events(WORLD_ADD_OBJECT,c)
        a= Ammo(self.rect.x, self.rect.y+20, 20, 20)
        EventListener.fire_events(WORLD_ADD_OBJECT,a)
        super().die()