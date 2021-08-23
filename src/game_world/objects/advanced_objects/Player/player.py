import pygame as pg
from src.game_world.objects.collision import CollisionMasks, CollisionPositions

from src.game_world.objects.basic_objects import AliveSprite
from src.structures.core_classes import SingletonABC
from src.core_functionaletize.game_time import GlobalTime
from src.Consts.settings import *
from src.game_world.UI.ui_enteties import Text
from src.core_functionaletize.event_system import EventListener
from src.game_world.objects.advanced_objects.items.item_collector import ItemCollector

class Player(AliveSprite, metaclass=SingletonABC):
    """
    The Player is the object that the user has control on
    """

    def __init__(self, x, y, obj_width, obj_height, sprite_img: str):
        AliveSprite.__init__(self, x, y, obj_width, obj_height, obj_width, obj_height-15 ,CollisionMasks.PLAYER, (CollisionMasks.ENEMY,), PLAYER_HEALTH,
                             PLAYER_SPEED, PLAYER_POWER,
                             sprite_img=sprite_img)

        self.__player_health_text = Text(500, 0, "health: ",str(self._health), 20)
        self.items = ItemCollector() # The items the player has
        EventListener.fire_events(WORLD_ADD_OBJECT, self.__player_health_text)

    def _calculate_velocity(self):
        self._vx, self._vy = 0, 0  # Reset velocity
        keys = pg.key.get_pressed()

        if (keys[pg.K_LEFT] or keys[pg.K_a]) and CollisionPositions.LEFT not in self.collider.collistion_positions:
            # Apply velocity to right
            self._vx = self._speed

        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and CollisionPositions.RIGHT not in self.collider.collistion_positions:
            # Apply velocity to left
            self._vx -= self._speed

        if (keys[pg.K_UP] or keys[pg.K_w]) and CollisionPositions.TOP not in self.collider.collistion_positions:
            # Apply velocity to top
            self._vy = self._speed

        if (keys[pg.K_DOWN] or keys[pg.K_s]) and CollisionPositions.BOTTOM not in self.collider.collistion_positions:
            # Apply velocity to bottom
            self._vy -= self._speed

        if self._vx != 0 and self._vy != 0:
            # Apply diagonal movement
            self._vx *= 0.7071
            self._vy *= 0.7071

        self._vx *= GlobalTime.delta_time()  # Delta time the velocity to make it smooth
        self._vy *= GlobalTime.delta_time()  # Delta time the velocity to make it smooth

    def _movement(self):
        if CollisionPositions.LEFT in self.collider.collistion_positions:
            # Checks for right border
            if self._vx > 0:
                self._vx = 0

        if CollisionPositions.RIGHT in self.collider.collistion_positions:
            # Checks for left border
            if self._vx < 0:
                self._vx = 0

        if CollisionPositions.TOP in self.collider.collistion_positions:
            # Checks for top border
            if self._vy > 0:
                self._vy = 0

        if CollisionPositions.BOTTOM in self.collider.collistion_positions:
            # Checks for bottom border
            if self._vy < 0:
                self._vy = 0

        self._rect.x -= self._vx
        self._rect.y -= self._vy

    def take_hit(self,dmg_to_take):
        pass

    def update(self):
        self._calculate_velocity()
        self.collider.update(self.rect.x - self._vx,
                             self.rect.y - self._vy)  # Update the collider to the position the player wants to move to

        self.__player_health_text.change_text(f"player health: {self._health}")

    def late_update(self):
        self._movement()
        super().late_update()
