import pygame as pg

from src.game_world.objects.basic_objects import BaseObject, RenderAbleObj
from src.Consts.settings import *
from src.core_functionaletize.event_system import EventListener
from src.core_functionaletize import utilitiez
from abc import ABC, abstractmethod
from src.game_world.rendering import RenderMode


class Text(RenderAbleObj):
    """
    A class used to create texts and change them
    """

    def __init__(self, x, y, text, font_size):
        super().__init__(RenderMode.UI_RENDER_MODE)
        self.__font = pg.font.SysFont(COSMIC_SANS_FONT, font_size)
        self.__text_surface = self.__font.render(text, False, (0, 0, 0))
        self.__pos = (x, y)

    def change_font_size(self, new_font_size):
        self.__font = pg.font.SysFont(COSMIC_SANS_FONT, new_font_size)

    def change_text(self, new_text):
        self.__text_surface = self.__font.render(new_text, False, (0, 0, 0))

    def render_properties(self) -> tuple:
        return self.__text_surface, self.__pos

    def get_text_size(self):
        """
        returns the width and the height of the text
        """
        return self.__text_surface.get_width(), self.__text_surface.get_height()

    def change_pos(self, new_pos):
        self.__pos = new_pos


class Button(BaseObject):
    """
    Button is a clickable object that can have a text inside of it
    """

    def __init__(self, x: int, y: int, obj_width: int, obj_height: int, color: tuple, function_to_activate,
                 button_text: Text = None):
        self.__function_to_activate = function_to_activate
        if button_text is not None:
            self.__button_text = button_text
            button_text.change_pos((x,y))  # Change the position of the text to the center of the button
            obj_width, obj_height = button_text.get_text_size()
        super().__init__(x, y, obj_width, obj_height, RenderMode.UI_RENDER_MODE, color)

        EventListener.add_handler(MOUSE_LEFT_CLICK, self.__check_if_got_pressed)

    def render_properties(self) -> tuple:
        return self._image, self._rect


    def __check_if_got_pressed(self, mouse_x_pos, mouse_y_pos):
        """
        Function that gets called whenever left mouse button is clicked
        """
        if utilitiez.on_object(self.rect.x, self.rect.y, self.rect.width, self.rect.height, mouse_x_pos, mouse_y_pos,
                               MOUSE_WIDTH, MOUSE_HEIGHT):
            self.__on_click(mouse_x_pos, mouse_y_pos)

    def __on_click(self, mouse_x_pos, mouse_y_pos):
        """
        Function that gets called if the mouse clicked on button
        """
        self.__function_to_activate(mouse_x_pos, mouse_y_pos)


class Canvas:
    """
    A class that groups together UI enteties with the same common ground like : start menu/ setting menu
    """

    def __init__(self):
        self.__UI_objects = []

    def add_ui_object(self, UI_object: object):
        """
        Add UI_object to the canvas
        """
        self.__UI_objects.append(UI_object)

    def show_all(self):
        """
        Show all UI_objects to the canvas
        """
        for UI_object in self.__UI_objects:
            UI_object.show()

    def hide_all(self):
        """
        Hide all UI_objects to the canvas
        """
        for UI_object in self.__UI_objects:
            UI_object.hide()

    def apply_function_on_UI_objects(self, function_to_apply) -> None:
        """
        Apply a certain action on all the the UI_objects in the canvas
        """
        for UI_object in self.__UI_objects:
            function_to_apply(UI_object)
