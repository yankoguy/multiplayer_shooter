import pygame as pg
from src.Consts.settings import *
from src.structures.core_classes import Singleton
from src.game_world.world import World
import src.core_functionaletize.input_processing as input_processing

pg.init()


class Game(metaclass=Singleton):
    def __init__(self):
        # initialize pygame
        pg.init()
        pg.font.init()

        # game loop settings
        self.is_playing = True

        # create core objects
        self.world = World()

    def run(self):
        self._game_loop()

    def _update(self):
        # Process events
        input_processing.key_to_event()

        # update all of the game core objects
        self.world.update()

    def _game_loop(self):
        while self.is_playing:
            self._update()
            pg.event.pump()

Game().run()
