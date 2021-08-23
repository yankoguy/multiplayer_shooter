import pygame as pg
from src.Consts.settings import *
from abc import ABC, abstractmethod
from src.game_world.objects.collision import Collider, CollisionMasks
from src.game_world.rendering import RenderMode
from src.core_functionaletize.event_system import EventListener


class RenderAbleObj(ABC):
    """
    An object that wants to be able to be rendered
    Attributes:
        render_mode - how the object should be render (like UI or like sprite)
        enable - to show the object or not
    """

    @abstractmethod
    def __init__(self, render_mode: RenderMode):
        self._render_mode = render_mode
        self._enable = True

    @abstractmethod
    def render_properties(self) -> tuple:
        """
        Returns how the object wants to be render
        """
        pass

    @property
    def enable(self):
        return self._enable

    @property
    def render_mode(self):
        return self._render_mode

    def show(self):
        self._enable = True

    def hide(self):
        self._enable = False


class BaseObject(RenderAbleObj, ABC):
    """
    The BaseObject is the most simple object in the game - it can only be shown to screen
    Attributes:
        x_size - the width of the object
        y_size - the height of the objects
        color - in which color the object will be displayed
        object_img - Sprites are displayed with an image instead of color, if no img_path was specified the sprite will be just white

    """

    @abstractmethod
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, render_mode: RenderMode, color: tuple = WHITE,
                 object_img: str = None):
        super().__init__(render_mode)
        self._image = pg.Surface((obj_width, obj_height))
        self._image.fill(color)
        self._rect = self._image.get_rect()
        self._rect.x = x
        self._rect.y = y
        if object_img is not None:
            self._image = pg.image.load(object_img).convert_alpha()

    @property
    def rect(self):
        return self._rect

    def render_properties(self) -> tuple:
        """
        Returns how the object wants to be render
        """
        return self._image, self.rect


class UpdatedObject(BaseObject, ABC):
    """
    An object with the ability to be updated every frame
    """

    @abstractmethod
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, color: tuple = WHITE, object_img: str = None):
        super().__init__(x, y, obj_width, obj_height, RenderMode.SPRITE_RENDER_MODE, color, object_img)
        self._exists = True  # If this parameter is False the object will be removed from game

    @abstractmethod
    def update(self):
        """
        Function that runs every frame
        """
        pass

    def late_update(self):
        """
        Function that runs every frame - after update
        """
        pass

    @property
    def exists(self):
        return self._exists

    def _destroy(self):
        self._exists = False


class Sprite(UpdatedObject, ABC):
    """
    Sprite is used as a backbone to create complicated sprites like: advanced_objects, enemy, buildings ...
    And it also supports collision
    attributes:
        mask - An indication to the type of objects that can collide with this object
        collider width, collider height - the height and the width of the collider
    """

    @abstractmethod
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, collider_width: int , collider_height: int,mask: CollisionMasks,
                 masks_to_collide_with: tuple, color=WHITE,
                 sprite_img: str = None):
        super().__init__(x, y, obj_width, obj_height, color, sprite_img)
        self._collider = Collider(x, y, collider_width, collider_height, mask, masks_to_collide_with)  # The collider is an
        # object that gives you the information about the sprite collision

    @property
    def collider(self):
        return self._collider

    def update(self):
        self.collider.update(self.rect.x, self.rect.y)

    def late_update(self):
        self.collider.late_update()


class AliveSprite(Sprite, ABC):
    """
    An alive sprite is a sprite that can move and take hit. It also has health, speed and damage.
    """

    @abstractmethod
    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, collider_width:int , collider_height: int, mask: CollisionMasks,
                 masks_to_collide_with: tuple, health: int, speed: int,
                 damage: int,
                 sprite_img=None):
        Sprite.__init__(self, x, y, obj_width, obj_height, collider_width,collider_height, mask,masks_to_collide_with, sprite_img=sprite_img)
        self._health = health
        self._speed = speed
        self._damage = damage
        self._vx, self._vy = 0,0 # The velocity of the object

    def take_hit(self, dmg_to_take):
        self._health -= dmg_to_take
        if self._health <= 0:
            self._destroy()


    @abstractmethod
    def _calculate_velocity(self):
        pass

    def _movement(self):
        self.rect.x += int(self._vx) # Move the bullet
        self.rect.y += int(self._vy) # Move the bullet
        self._vx -= int(self._vx) # Subtract from velocity
        self._vy -= int(self._vy) # Subtract from velocity