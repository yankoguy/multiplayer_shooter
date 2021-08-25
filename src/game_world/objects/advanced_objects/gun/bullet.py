import pygame as pg
from src.game_world.objects.basic_objects import AliveSprite
from src.game_world.objects.collision import CollisionMasks
from src.core_functionaletize.game_time import GlobalTime
import src.core_functionaletize.utilitiez as utilitiez
from src.core_functionaletize.game_time import Timer


class Bullet(AliveSprite):
    """
    Bullet is an object that being created from a gun and has zero health (when he touches something he dies)
    angle : the angle the bullet is rotating to
    time_to_live how many seconds the bullet is going to live
    """

    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, mask: CollisionMasks,
                 masks_to_collide_with: tuple,
                 health: int,
                 speed: int,
                 damage: int,
                 angle: float,
                 time_to_live: int,
                 sprite_img=None):

        super().__init__(x, y, obj_width, obj_height,obj_width+3, obj_height+2, mask, masks_to_collide_with, health, speed, damage, sprite_img)
        self.__angle = angle  # The angle the bullet got shot at
        self.__vx, self.__vy = 0, 0  # The Velocity of the bullet
        self.__timer_until_died = Timer(time_to_live,
                                        self._destroy)  # How much time does it takes to the bullet until he disapear
        self._image, self._rect = self.__rotate_to_angle()



    def __rotate_to_angle(self):
        """
        Returns new rect and image of the sprite in certain angle
        """
        rotated_image = pg.transform.rotate(self._image, self.__angle)
        new_rect = rotated_image.get_rect(center=self._image.get_rect(topleft=self.rect.topleft).center)

        return rotated_image, new_rect

    def render_properties(self) -> tuple:
        """
         Returns how the object should be rendered - image and rect
         """
        return self.__rotate_to_angle()

    def update(self):
        super().update()
        self.__timer_until_died.update_timer()

    def late_update(self):
        self._calculate_velocity()
        self._movement()
        self.__deal_dmg()
        super().late_update()

    def _calculate_velocity(self):
        velocity = utilitiez.calculat_new_xy(self._speed * GlobalTime.delta_time(),
                                             self.__angle)  # Calculate the velocity of the bullet
        self._vx += velocity[0]  # Add it to the currect velocity
        self._vy += velocity[1]  # Add it to the currect velocity

    def __deal_dmg(self):
        if self.collider.collision is not None:
            if isinstance(self.collider.collision, AliveSprite):
                # If object is alive sprite
                self.collider.collision.take_hit(self._damage)
                self.take_hit(1)  # Bullet takes 1 damgage when hit something
