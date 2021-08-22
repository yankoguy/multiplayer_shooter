import pygame as pg
from src.Consts.settings import *
from src.structures.core_classes import Singleton
from src.game_world.world import World
import src.core_functionaletize.input_processing as input_processing
from src.game_world.window import Window
from src.core_functionaletize.game_time import GlobalTime
from src.core_functionaletize.event_system import EventListener
from enum import Enum
from src.game_world.UI.ui_enteties import Text


class GameStates(Enum):
    GAME_STATE = 0
    START_MENU = 1
    SETTINGS_MENU = 2
    END_MENU = 3


class Game(metaclass=Singleton):
    """
    The game class is the thing that runs the game by 3 actions: get_events, update and render
    """

    def __init__(self):
        # initialize pygame
        pg.init()
        pg.font.init()

        # game loop settings
        self._is_playing = True
        self._current_menu = None

        # create core objects
        self._window = Window()
        self._world = World()
        self._game_clock = GlobalTime()

        # Add game df events
        EventListener.add_handler(GO_TO_MENU_STATE, self._menu_state)
        EventListener.add_handler(GO_TO_GAME_STATE, self._game_state)
        EventListener.add_handler(KEY_DOWN + str(pg.K_ESCAPE), lambda: self._menu_state(SETTINGS_MENU))

    def start(self):
        """
        Start running game
        """
        self._menu_state(STARTING_MENU)  # first menu

        self._game_loop()

    def _update(self):
        """
        Update all the stuff in game
        """
        if self._current_menu is None:
            # If we are in game state
            self._game_clock.update()
            self._world.update()

        self._window.update()

    @staticmethod
    def _events():
        """
        Handle events
        """
        input_processing.key_to_event()
        pg.event.pump()

    def _render(self):
        """
        Shows all the object of the game to the screen
        """
        self._world.show_objects(self._window)

    def _game_loop(self):
        """
        The loop of the game - runs all the time
        """
        while self._is_playing:
            self._events()
            self._update()
            self._render()

    def _menu_state(self, menu_name):
        """
        Go into menu state - pause game and show menu
        """
        self._world.hide_all_objects()  # Hide all objects
        self._current_menu = self._world.menus[menu_name].canvas  # Get the chosen menu
        self._current_menu.show_all()  # Show only the chosen menu

    def _game_state(self):
        """
        Go into game state  (if you are not already in game) - resume game and hide menu
        """
        if self._current_menu is not None:
            GlobalTime.reset_delta_time()  # Reset the delta time (becuase the game paused)
            self._world.show_all_objects()  # Show all objects
            self._world.hide_all_menus()  # Hide all the menus
            self._current_menu = None


Game().start()
