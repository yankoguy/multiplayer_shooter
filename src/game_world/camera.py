import pygame as pg
from src.Consts.settings import *
from src.structures.core_classes import Singleton
from src.core_functionaletize.game_time import GlobalTime

"""
The camera is responsible of representing specific objects to the screen
"""


class Camera(metaclass=Singleton):
    def __init__(self):
        self.__camera_view = pg.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT) # The part of the map that shown in screen
        self.__camera_move_speed = CAMERA_SPEED

    def update(self) -> None:
        pass
        '''self._camera_movement(GlobalTime.delta_time())'''

    def apply_pos(self, entity:pg.rect) -> pg.rect:
        """
        In order to "move" the camera we should move all the objects on the screen because we there is not real camera :)
        So we change the camera position and when we render an object we render it with the offset of the _camera

        attributes:
            entity - the object we are about to show
        """
        return entity.move(self.__camera_view.topleft)

    """
    def _camera_movement(self, delta_time):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()

        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self._camera_view.x < WINDOW_WIDTH:
            # Checks for right border
            self.vx = self._camera_move_speed

        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self._camera_view.x > -WINDOW_WIDTH:
            # Checks for left border
            self.vx -= self._camera_move_speed

        if (keys[pg.K_UP] or keys[pg.K_w]) and self._camera_view.y < WINDOW_HEIGHT:
            # Checks for top border
            self.vy = self._camera_move_speed

        if (keys[pg.K_DOWN] or keys[pg.K_s]) and self._camera_view.y > -WINDOW_HEIGHT:
            # Checks for bottom border
            self.vy -= self._camera_move_speed

        if self.vx != 0 and self.vy != 0:
            # Apply diagonal movement
            self.vx *= 0.7071
            self.vy *= 0.7071

        self._camera_view.x -= self.vx * delta_time
        self._camera_view.y -= self.vy * delta_time
    """