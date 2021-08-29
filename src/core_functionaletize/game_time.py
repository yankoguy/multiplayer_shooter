import pygame as pg
from src.Consts.settings import *
from src.structures.meta_classes import Singleton
from src.game_world.UI.ui_enteties import Text
from src.core_functionaletize.event_system import EventListener


class GlobalTime(metaclass=Singleton):
    """
    GlobalTime stores important time varibles
    """
    __delta_time = 0  # Fixed time that doesn't affected by the FPS rate
    __running_time = 0  # How much time does the game run
    __clock = pg.time.Clock()

    def __init__(self):
        self._fps_text = Text(50, 0, "fps: ", str(GlobalTime._get_fps_rate()) , 30)
        EventListener.fire_events(WORLD_ADD_OBJECT, self._fps_text)

    def update(self):
        GlobalTime.__delta_time = GlobalTime.__clock.tick(FPS) / 1000
        GlobalTime._running_time = GlobalTime.__delta_time
        self._fps_text.change_text(str(GlobalTime._get_fps_rate()))

    @classmethod
    def delta_time(cls):
        return cls.__delta_time

    @classmethod
    def running_time(cls):
        return cls.__running_time

    @classmethod
    def reset_delta_time(cls):
        GlobalTime.__clock.tick(FPS)

    @classmethod
    def _get_fps_rate(cls):
        return int(cls.__clock.get_fps())


class Timer:
    """
    The Timer used to determain time of actions in game, like the time between gun shoot for example
    Attributes:
        function_to_activate - which function to call when the timer reaches to zero
    """

    def __init__(self, start_time, function_to_activate=None):
        self.__time = start_time
        self.__function_to_activate = function_to_activate
        self.__pause = False  # Timer can be paused
        self.finish = False

    def update_timer(self):
        if not self.__pause:
            if self.__time <= 0:
                self.finish=True
                if self.__function_to_activate is not None:
                    self.__function_to_activate()
            else:
                self.__time -= GlobalTime.delta_time()

    def pause_timer(self):
        self.__pause = True

    def resume_timer(self):
        self.__pause = False
