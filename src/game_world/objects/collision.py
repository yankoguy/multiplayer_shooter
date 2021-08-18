from enum import Enum
from src.core_functionaletize import utilitiez
from src.Consts.settings import *

class CollisionMasks(Enum):
    WALLS = 1
    BUILDINGS = 2
    ENEMIES = 3
    PLAYER = 4
    
class CollisionPositions(Enum):
    NO_CLLOISTION = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4


class Collider:
    """
    An object that responsible for checking collision between objects
    """
    COLLIDER_HEIGHT_OFFSET = 15 # In order to make the collider fit the object better

    def __init__(self, x, y, width, height, mask: CollisionMasks, masks_to_collide_with: tuple):
        self.x = x
        self.y = y
        self.width = width
        self.height = height - Collider.COLLIDER_HEIGHT_OFFSET
        self.mask = mask
        self._masks_to_collide_with = masks_to_collide_with
        self.collision = None # Will be equal to the sprite this object collided with in current frame
        self.collistion_positions = [] # In which border of the collider did the collide occurred
        
    def update(self, x, y):
        """
        Update the collider position
        """
        self.x = x
        self.y = y

    def late_update(self):
        self._reset_collision()

    def _reset_collision(self):
        self.collision = None
        self.collistion_positions = []

    def _get_collision_pos(self) -> list:
        collistions = []
        if self.y > self.collision.collider.y:
            collistions.append(CollisionPositions.TOP)
        else:
            collistions.append(CollisionPositions.BOTTOM)
        if self.x > self.collision.collider.x:
            collistions.append(CollisionPositions.LEFT)
        else:
            collistions.append(CollisionPositions.RIGHT)

        return collistions

    def get_collision(self, sprites: list) -> None:
        """
        Returns The object that collide with, if collide with nothing returns None

        Attributes:
            sprites - A list of sprites that the player may collide with
        """
        for sprite in sprites:
            collider = sprite.collider
            if collider is not self and collider.mask in self._masks_to_collide_with:
                if utilitiez.on_object(self.x,self.y,self.width,self.height,collider.x,collider.y,collider.width,collider.height):
                    self.collision = sprite
                    self.collistion_positions = self._get_collision_pos()

