import pygame as pg
from src.Consts.settings import *
from abc import ABC, abstractmethod
from src.game_world.objects.collision import Collider, CollisionMasks


class BaseObject(ABC):
    """
    The BaseObject is the most simple object in the game - it can only be shown to screen
    Attributes:
        x - starting x position (top left)
        y - starting y position (bottom left)
        x_size - the width of the object
        y_size - the height of the objects
        color - in which color the object will be displayed
    """

    @abstractmethod
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, color: tuple):
        self.image = pg.Surface((obj_width, obj_height))
        self.image.fill(color)
        self._rect = self.image.get_rect()
        self._rect.x = x
        self._rect.y = y

    @property
    def rect(self):
        return self._rect


class Sprite(BaseObject, ABC):
    """
    Sprite is used as a backbone to create complicated sprites like: advanced_objects, enemy, buildings ...
    And it also supports collision
    attributes:
        sprite_img - Sprites are displayed with an image instead of color, if no img_path was specified the sprite will be just white
        mask - An indication to the type of objects that can collide with this object
    """

    @abstractmethod
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, mask: CollisionMasks, masks_to_collide_with:tuple, color=WHITE,
                 sprite_img=None):
        super().__init__(x, y, obj_width, obj_height, color)
        self.collider = Collider(x, y, obj_width, obj_height, mask, masks_to_collide_with)
        if sprite_img is not None:
            self.image = pg.image.load(sprite_img).convert_alpha()

    @abstractmethod
    def update(self):
        """
        Function that runs every frame
        """
        pass

    @abstractmethod
    def late_update(self):
        """
        Function that runs every frame - after update
        """
        pass

class AliveSprite(Sprite, ABC):
    """
    An alive sprite is a sprite that can movement, take_hit and deal_dmg. It also has health, speed and damage.
    """

    @abstractmethod
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, mask: CollisionMasks, masks_to_collide_with: tuple, health: int, speed: int,
                 damage: int,
                 sprite_img=None):
        Sprite.__init__(self, x, y, obj_width, obj_height, mask, masks_to_collide_with,sprite_img=sprite_img)
        self._health = health
        self._speed = speed
        self._damage = damage

    @abstractmethod
    def _movement(self):
        pass

    @abstractmethod
    def take_hit(self):
        pass
