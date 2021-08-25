import pygame as pg
from enum import Enum
from src.Consts.settings import *


class RenderMode(Enum):
    """
    Enum for all the modes an object can be rendered.
    """
    SPRITE_RENDER_MODE = 1  # Render wth camera control
    UI_RENDER_MODE = 2  # Render wthout camera control


class Renderer:
    def __init__(self):
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Set screen's size

    def render(self,camera: object, objects_to_render: list) -> None:
        """
        Draw the objects in the objects_to_render by the offset of the camera to the screen.
        """
        self.screen.fill(WHITE)

        for obj in objects_to_render:
            if obj.enable:  # If the UI has the show flag only than show him
                if obj.render_mode == RenderMode.SPRITE_RENDER_MODE:
                    # The object is Sprite
                    self.screen.blit(obj.render_properties()[0], camera.apply_pos(obj.render_properties()[1]))

                elif obj.render_mode == RenderMode.UI_RENDER_MODE:
                    # The object is UI
                    self.screen.blit(obj.render_properties()[0], obj.render_properties()[1])

