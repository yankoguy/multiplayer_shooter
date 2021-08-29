import pygame as pg
from src.Consts.settings import *
from src.structures.meta_classes import Singleton
from src.core_functionaletize.game_time import GlobalTime
import src.core_functionaletize.utilitiez as  utilitiez
"""
The camera is responsible of representing specific objects to the screen
"""


class Camera(metaclass=Singleton):
    __x_offset = 0
    __y_offset = 0

    def __init__(self):
        self.__camera_view = pg.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)  # The part of the map that shown in screen
        self.__camera_move_speed = CAMERA_SPEED

    def update(self,target) -> None:
        x = -target.rect.x + int(WINDOW_WIDTH/2)
        y = -target.rect.y + int(WINDOW_HEIGHT/2)
        Camera.__x_offset = x
        Camera.__y_offset = y
        self.__camera_view = pg.Rect(x,y,WINDOW_WIDTH,WINDOW_HEIGHT)

    def apply_pos(self, entity: pg.rect) -> pg.rect:
        """
        In order to "move" the camera we should move all the objects on the screen because we there is not real camera :)
        So we change the camera position and when we render an object we render it with the offset of the _camera

        attributes:
            entity - the object we are about to show
        """
        return entity.move(self.__camera_view.topleft)


    @classmethod
    def normal_to_world_pos(cls,pos) -> tuple:
        """
        get the position of an object which is not affected by camera (like mouse) to world pos
        """
        return pos[0] - cls.__x_offset, pos[1] - cls.__y_offset

    @classmethod
    def screen_pos_to_world_pos(cls,pos) -> tuple:
        """
        get the position of screen object (like rect) to world pos
        """
        return pos[0] + cls.__x_offset, pos[1] + cls.__y_offset


    @classmethod
    def is_on_camera(cls,x,y,width,height) -> bool:
        """
        Returns if an object is visable to player
        """
        if utilitiez.on_object(-cls.__x_offset,-cls.__y_offset
                ,WINDOW_WIDTH,WINDOW_HEIGHT,x,y,width,height):
                    return True

        return False