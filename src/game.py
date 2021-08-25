import pygame as pg
from src.Consts.settings import *
from src.structures.meta_classes import Singleton
from src.game_world.world import World
import src.core_functionaletize.input_processing as input_processing
from src.core_functionaletize.game_time import GlobalTime
from src.core_functionaletize.event_system import EventListener
from enum import Enum
from src.game_world.rendering import Renderer
from src.multiplayer.client import Client
from src.game_world.camera import Camera
import src.debbuging as db


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
        pg.display.set_caption("My Game")  # Set window's name

        # game loop settings
        self.__is_playing = True
        self.__current_menu = None

        # create core objects
        self.__renderer = Renderer()
        self.__world = World()
        self.__game_clock = GlobalTime()
        self.__client = Client()
        self.__camera = Camera()  # Create camera to show stuff in window

        # Add game df events
        EventListener.add_handler(GO_TO_MENU_STATE, self.__menu_state)
        EventListener.add_handler(GO_TO_GAME_STATE, self.__game_state)
        EventListener.add_handler(KEY_DOWN + str(pg.K_ESCAPE), lambda: self.__menu_state(SETTINGS_MENU))

    def start(self):
        """
        Start running game
        """
       # self.__menu_state(STARTING_MENU)  # first menu
        self.__game_loop()

    def __update(self):
        """
        Update all the stuff in game
        """
        if self.__current_menu is None:
            # If we are in game state
            self.__game_clock.update()
            self.__world.update()

        elif self.__current_menu == MATCHMAKING_MENU and self.__client.communicate:
            # We are in matchmaking menu and found someone to play with
            self.__game_state()

        self.__camera.update(self.__world.get_player())


    @staticmethod
    def __events():
        """
        Handle events
        """
        input_processing.key_to_event()
        pg.event.pump()

    def __render(self):
        """
        Shows all the object of the game to the screen
        """
        self.__renderer.render(self.__camera,self.__world.get_objects_to_render())
        db.show_colliders_object(self.__renderer.screen,self.__world._sprites)
        pg.display.flip()

    def __game_loop(self):
        """
        The loop of the game - runs all the time
        """
        while self.__is_playing:
            self.__events()
            self.__update()
            self.__render()
            if self.__client.connected:
                self.__client.send_data() # Send data to server
                self.__client.get_input_from_server() # Get new data from server

    def __menu_state(self, menu_name):
        """
        Go into menu state - pause game and show menu
        """
        self.__world.hide_all_objects()  # Hide all objects
        self.__current_menu = self.__world.menus[menu_name].canvas.show_all()  # Show menu
        self.__current_menu = menu_name

        if menu_name == MATCHMAKING_MENU:
            self.__client.connect_to_server() # If the user is in matchmaking menu try to connect to server and find another player


    def __game_state(self):
        """
        Go into game state  (if you are not already in game) - resume game and hide menu
        """
        if self.__current_menu is not None:
            GlobalTime.reset_delta_time()  # Reset the delta time (becuase the game paused)
            self.__world.show_all_objects()  # Show all objects
            self.__world.hide_all_menus()  # Hide all the menus
            self.__current_menu = None


Game().start()
