import pygame as pg

from src.game_world.objects.basic_objects import BaseObject
from src.Consts.settings import *
from src.core_functionaletize.event_system import EventListener
from src.core_functionaletize import utilitiez


class Text:
    """
    A class used to create texts and change them
    """

    def __init__(self, x, y, text, font_size):
        self._font = pg.font.SysFont(COSMIC_SANS_FONT, font_size)
        self.text_surface = self._font.render(text, False, (0, 0, 0))
        self.pos = (x, y)

    def change_font_size(self, new_font_size):
        self._font = pg.font.SysFont(COSMIC_SANS_FONT, new_font_size)

    def change_text(self, new_text):
        self.text_surface = self._font.render(new_text, False, (0, 0, 0))


class Button(BaseObject):
    """
    Button is a clickable object
    """

    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, color: tuple, function_to_activate):
        super().__init__(x, y, obj_width, obj_height, color)
        self._function_to_activate = function_to_activate
        EventListener.add_handler("left_click", self._check_if_got_pressed)

    def _check_if_got_pressed(self, mouse_x_pos, mouse_y_pos):
        """
        Function that gets called whenever left mouse button is clicked
        """
        if utilitiez.on_object(self.rect.x, self.rect.y, self.rect.width, self.rect.height, mouse_x_pos, mouse_y_pos,
                               MOUSE_WIDTH, MOUSE_HEIGHT):
            self._on_click(mouse_x_pos, mouse_y_pos)

    def _on_click(self, mouse_x_pos, mouse_y_pos):
        """
        Function that gets called if the mouse clicked on button
        """
        self._function_to_activate(mouse_x_pos, mouse_y_pos)
