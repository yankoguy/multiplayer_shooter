import pygame as pg
from src.Consts.settings import *
from src.structures.core_classes import Singleton


class GlobalTime(metaclass=Singleton):
    """
    GlobalTime stores important time varibles
    """
    _delta_time = 0  # Fixed time that doesn't affected by the FPS rate
    _running_time = 0  # How much time does the game run

    @classmethod
    def update(cls):
        cls._delta_time = pg.time.Clock().tick(FPS) / 1000
        cls._running_time = cls._delta_time

    @classmethod
    def delta_time(cls):
        return cls._delta_time

    @classmethod
    def running_time(cls):
        return cls._running_time


class Timer:
    """
    The Timer used to determain time of actions in game, like the time between gun shoot for example
    """

    def __init__(self, start_time=0):
        self.timer = start_time
        self._pause = False  # Timer can be paused

    def update_timer(self):
        if not self._pause:
            self.timer += GlobalTime.delta_time()

    def pause_timer(self):
        self._pause = True

    def resume_timer(self):
        self._pause = False
