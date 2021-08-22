from src.game_world.UI.ui_enteties import Text, Button, Canvas
from src.Consts.settings import *
from src.structures.core_classes import Singleton
from src.core_functionaletize.event_system import EventListener


class StartingMenu(metaclass=Singleton):

    def __init__(self):
        self.__canvas = Canvas()
        b_1 = Button(500, 500, 100, 100, BLACK, self.__start_game)
        t_1 = Text(500, 50, "Welcome to start menu", 40)
        self.__canvas.add_ui_object(b_1)
        self.__canvas.add_ui_object(t_1)
        self.__canvas.hide_all()

    @property
    def canvas(self):
        return self.__canvas

    def __start_game(self, *args):
        """
        Go from start menu to game
        """
        EventListener.fire_events(GO_TO_GAME_STATE)


class SettingsMenu(metaclass=Singleton):

    def __init__(self):
        self.__canvas = Canvas()
        b_1_text =  Text(0, 0, "go back to game", 20)
        b_1 = Button(400, 500, 100, 100, BLUE, self.__return_to_game,b_1_text)

        b_2_text =  Text(0, 0, "go to settings 2", 20)
        b_2 = Button(100, 500, 100, 100, BLUE, self.__go_to_settings_two_menu,b_2_text)

        t_1 = Text(500, 50, "Welcome to settings menu", 40)
        self.__canvas.add_ui_object(b_1)
        self.__canvas.add_ui_object(b_1_text)
        self.__canvas.add_ui_object(b_2)
        self.__canvas.add_ui_object(b_2_text)
        self.__canvas.add_ui_object(t_1)
        self.__canvas.hide_all()

    @property
    def canvas(self):
        return self.__canvas

    def __return_to_game(self, *args):
        """
        Return to game from settings menu
        """
        EventListener.fire_events(GO_TO_GAME_STATE)

    def __go_to_settings_two_menu(self,*args):
        EventListener.fire_events(GO_TO_MENU_STATE,SETTINGS2_MENU)


class Setting2sMenu(metaclass=Singleton):

    def __init__(self):
        self.__canvas = Canvas()
        b_1_text = Text(0, 0, "go back to game", 20)
        b_1 = Button(400, 500, 100, 100, BLUE, self.__return_to_game, b_1_text)



        t_1 = Text(500, 50, "Welcome to settings2 menu", 40)
        self.__canvas.add_ui_object(b_1)
        self.__canvas.add_ui_object(b_1_text)

        self.__canvas.add_ui_object(t_1)
        self.__canvas.hide_all()

    @property
    def canvas(self):
        return self.__canvas

    def __return_to_game(self, *args):
        """
        Return to game from settings menu
        """
        EventListener.fire_events(GO_TO_GAME_STATE)

