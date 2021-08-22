import pygame as pg
from enum import Enum


class RenderMode(Enum):
    """
    Enum for all the modes an object can be rendered.
    """
    SPRITE_RENDER_MODE = 1 # Render wth camera control
    UI_RENDER_MODE = 2 # Render wthout camera control


class Renderer:
    @staticmethod
    def render(screen: object, camera: object, objects_to_render: list) -> None:
        """
        Draw the objects in the objects_to_render by the offset of the camera to the screen.
        """
        for obj in objects_to_render:
            if obj.enable:  # If the UI has the show flag only than show him
                if obj.render_mode == RenderMode.SPRITE_RENDER_MODE:
                    # The object is Sprite
                    screen.blit(obj.render_properties()[0], camera.apply_pos(obj.render_properties()[1]))

                elif obj.render_mode == RenderMode.UI_RENDER_MODE:
                    # The object is UI
                        screen.blit(obj.render_properties()[0], obj.render_properties()[1])
