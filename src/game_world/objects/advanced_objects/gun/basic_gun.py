import pygame as pg
from src.game_world.objects.basic_objects import UpdatedObject
from src.Consts.settings import *
import src.core_functionaletize.utilitiez as utilitiez
from src.core_functionaletize.event_system import EventListener
from src.game_world.objects.advanced_objects.gun.bullet import Bullet
from src.game_world.objects.collision import CollisionMasks
from src.multiplayer.client import Client
from src.multiplayer.network_object import NetworkObject
from src.game_world.camera import Camera

class Gun(UpdatedObject,NetworkObject):
    """
    Gun is an object that rotate to mouse and can shoot bullets
    attributes:
        holder - the object the gun should stick to (if it is None it just stays in place)
    """

    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, holder: object = None,
                 object_img: str = None):
        super().__init__(x, y, obj_width, obj_height, WHITE, object_img)
        NetworkObject.__init__(self)
        if holder is None:
            holder = self

        self.__current_angle = 0
        self.__holder = holder
        self.__x_offset = x - self.__holder.rect.x  # The offset of the gun from the holder
        self.__y_offset = y - self.__holder.rect.y  # The offset of the gun from the holder


    def start(self):
        if not self._online_object:
            EventListener.add_handler(MOUSE_LEFT_CLICK, self.__shoot)

    def update(self):
        self.__stick_to_holder()
        if self._online_object:
            if Client.get_data("mouse click") == 1:
                self.__shoot()

    def __stick_to_holder(self):
        """
        Put the gun at the same offset from his owner
        """
        self._rect.x = self.__holder.rect.x + self.__x_offset
        self._rect.y = self.__holder.rect.y + self.__y_offset

    def __rotate_to_mouse(self, angle: float):
        """
              Returns new rect and image of the sprite in certina angle
        """
        self.__current_angle = angle
        rotated_image = pg.transform.rotate(self._image, angle)
        new_rect = rotated_image.get_rect(center=self._image.get_rect(topleft=self.rect.topleft).center)
        return rotated_image, new_rect

    def render_properties(self) -> tuple:
        """
        Returns how the object should be rendered - image and rect
        """
        if not self._online_object:
            world_pos = Camera.normal_to_world_pos(pg.mouse.get_pos())
            angle = utilitiez.get_angle(self.rect.x, self.rect.y, world_pos[0], world_pos[1])
            Client.add_data_to_send("gun rotation", int(angle))
        else:
            angle = Client.get_data("gun rotation")
            if angle is None:
                angle = self.__current_angle
        return self.__rotate_to_mouse(angle)

    def __shoot(self, *args):
        bullet = Bullet(self.rect.x, self.rect.y, 5, 5, CollisionMasks.BULLET, (CollisionMasks.ENEMY,), 1, BULLET_SPEED, 20,
                        self.__current_angle, BULLET_TIME_TO_LIVE,
                        BULLET_IMAGE)

        EventListener.fire_events(WORLD_ADD_OBJECT, bullet)
