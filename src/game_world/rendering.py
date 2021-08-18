import pygame as pg
from enum import Enum


class RenderMode(Enum):
    """
    Enum for all the modes an object can be rendered.
    """
    SPRITE_RENDER_MODE = 1
    UI_RENDER_MODE = 2
    TEXT_RENDER_MODE = 3

class Renderer:
    @staticmethod
    def render(screen:object, camera:object, objects_to_render:list, mode:RenderMode) -> None:
        """
        Draw the objects in the objects_to_render by the offset of the camera to the screen.
        You can use the mode param in order to draw the objects without the camera control (UI for example)
        """
        if mode == RenderMode.SPRITE_RENDER_MODE:
            # The objects are sprites
            for obj in objects_to_render:
                screen.blit(obj.image, camera.apply_pos(obj))
        elif mode == RenderMode.UI_RENDER_MODE:
            # The objects are UI
            for obj in objects_to_render:
                screen.blit(obj.image, obj.rect)
        elif mode == RenderMode.TEXT_RENDER_MODE:
            # The objects are UI
            for obj in objects_to_render:
                screen.blit(obj.text_surface, obj.pos)