import pygame as pg
from src.game_world.objects.collision import CollisionMasks,CollisionPositions

from src.game_world.objects.basic_objects import AliveSprite
from src.structures.core_classes import SingletonABC
from src.core_functionaletize.game_time import GlobalTime
from src.Consts.settings import *


class Player(AliveSprite, metaclass=SingletonABC):
    """
    The Player is the object that the user has control on
    """

    def __init__(self, x, y, obj_width, obj_height, mask, sprite_img: str):
        AliveSprite.__init__(self, x, y, obj_width, obj_height, mask, (CollisionMasks.ENEMIES,),PLAYER_HEALTH, PLAYER_SPEED, PLAYER_POWER,
                             sprite_img=sprite_img)

    def _movement(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()

        if (keys[pg.K_LEFT] or keys[pg.K_a]) and CollisionPositions.LEFT not in self.collider.collistion_positions:
            # Checks for right border
            self.vx = PLAYER_SPEED

        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and  CollisionPositions.RIGHT not in self.collider.collistion_positions:
            # Checks for left border
            self.vx -= PLAYER_SPEED

        if (keys[pg.K_UP] or keys[pg.K_w]) and CollisionPositions.TOP not in self.collider.collistion_positions:
            # Checks for top border
            self.vy = PLAYER_SPEED

        if (keys[pg.K_DOWN] or keys[pg.K_s]) and CollisionPositions.BOTTOM not in self.collider.collistion_positions:
            # Checks for bottom border
            self.vy -= PLAYER_SPEED

        if self.vx != 0 and self.vy != 0:
            # Apply diagonal movement
            self.vx *= 0.7071
            self.vy *= 0.7071

        self._rect.x -= self.vx * GlobalTime.delta_time()
        self._rect.y -= self.vy * GlobalTime.delta_time()

        self._smooth_movement()

    def take_hit(self):
        pass

    def update(self):
        self._movement()
        self.collider.update(self.rect.x,self.rect.y)

    def late_update(self):
        self.collider.late_update()