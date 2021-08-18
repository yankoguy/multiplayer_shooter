import pygame as pg
from src.structures.core_classes import Singleton
from src.Consts.settings import *
from src.game_world.rendering import Renderer, RenderMode
from src.game_world.camera import Camera
"""
The window class is used for displaying the the game window
"""


class Window(metaclass=Singleton):
    def __init__(self):
        # initialize pygame window
        pg.display.set_caption("My Game")
        self._screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._camera = Camera()

    def draw_objects_on_screen(self, object_to_draw: list, mode: RenderMode) -> None:
        Renderer.render(self._screen, self._camera, object_to_draw, mode)

    def clear_screen(self, color: tuple = BLACK):
        self._screen.fill(color)

    def update(self) -> None:
        self._camera.update()
        pg.display.flip()

