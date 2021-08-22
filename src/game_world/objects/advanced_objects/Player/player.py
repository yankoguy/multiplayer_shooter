import pygame as pg
from src.game_world.objects.collision import CollisionMasks, CollisionPositions

from src.game_world.objects.basic_objects import AliveSprite
from src.structures.core_classes import SingletonABC
from src.core_functionaletize.game_time import GlobalTime
from src.Consts.settings import *
from src.game_world.UI.ui_enteties import Text
from src.core_functionaletize.event_system import EventListener


class Player(AliveSprite, metaclass=SingletonABC):
    """
    The Player is the object that the user has control on
    """

    def __init__(self, x, y, obj_width, obj_height, mask, sprite_img: str):
        AliveSprite.__init__(self, x, y, obj_width, obj_height, mask, (CollisionMasks.ENEMY,), PLAYER_HEALTH,
                             PLAYER_SPEED, PLAYER_POWER,
                             sprite_img=sprite_img)

        self.__vx = 0  # Velocity in X axis
        self.__vy = 0  # Velocity in Y axis
        self.__player_health_text = Text(500, 0, "", 20)
        EventListener.fire_events(WORLD_ADD_OBJECT, self.__player_health_text)

    def _check_movement(self):
        self.__vx, self.__vy = 0, 0  # Reset velocity
        keys = pg.key.get_pressed()

        if (keys[pg.K_LEFT] or keys[pg.K_a]) and CollisionPositions.LEFT not in self.collider.collistion_positions:
            # Apply velocity to right
            self.__vx = self._speed

        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and CollisionPositions.RIGHT not in self.collider.collistion_positions:
            # Apply velocity to left
            self.__vx -= self._speed

        if (keys[pg.K_UP] or keys[pg.K_w]) and CollisionPositions.TOP not in self.collider.collistion_positions:
            # Apply velocity to top
            self.__vy = self._speed

        if (keys[pg.K_DOWN] or keys[pg.K_s]) and CollisionPositions.BOTTOM not in self.collider.collistion_positions:
            # Apply velocity to bottom
            self.__vy -= self._speed

        if self.__vx != 0 and self.__vy != 0:
            # Apply diagonal movement
            self.__vx *= 0.7071
            self.__vy *= 0.7071

        self.__vx *= GlobalTime.delta_time()  # Delta time the velocity to make it smooth
        self.__vy *= GlobalTime.delta_time()  # Delta time the velocity to make it smooth

    def _movement(self):
        if CollisionPositions.LEFT in self.collider.collistion_positions:
            # Checks for right border
            if self.__vx > 0:
                self.__vx = 0

        if CollisionPositions.RIGHT in self.collider.collistion_positions:
            # Checks for left border
            if self.__vx < 0:
                self.__vx = 0

        if CollisionPositions.TOP in self.collider.collistion_positions:
            # Checks for top border
            if self.__vy > 0:
                self.__vy = 0

        if CollisionPositions.BOTTOM in self.collider.collistion_positions:
            # Checks for bottom border
            if self.__vy < 0:
                self.__vy = 0

        self._rect.x -= self.__vx
        self._rect.y -= self.__vy

    def take_hit(self,dmg_to_take):
        pass

    def update(self):
        self._check_movement()
        self.collider.update(self.rect.x - self.__vx,
                             self.rect.y - self.__vy)  # Update the collider to the position the player wants to move to

        self.__player_health_text.change_text(f"player health: {self._health}")

    def late_update(self):
        self._movement()
        super().late_update()
