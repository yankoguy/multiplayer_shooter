import pygame as pg
from src.structures.core_classes import Singleton
from src.Consts.settings import *
from src.game_world.rendering import Renderer, RenderMode
from src.game_world.camera import Camera



class Window(metaclass=Singleton):
    """
    The window that opens in the user's computer, used for displaying the the game window
    """

    def __init__(self):
        pg.display.set_caption("My Game")  # Set window's name
        self.__screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Set screen's size
        self.__camera = Camera()  # Create camera to show stuff in window


    def draw_objects_on_screen(self, object_to_draw: list) -> None:
        self._clear_screen(WHITE)
        Renderer.render(self.__screen, self.__camera, object_to_draw)

    def _clear_screen(self, color: tuple = BLACK):
        self.__screen.fill(color)

    def update(self) -> None:
        self.__camera.update()
        pg.display.flip()

    @property
    def screen(self):
        return self.__screen

    def scale(self, new_width, new_height):
        pass
