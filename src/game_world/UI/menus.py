from src.game_world.UI.ui_enteties import Text, Button, Canvas
from src.Consts.settings import *
from src.structures.meta_classes import SingletonABC
from src.core_functionaletize.event_system import EventListener
from abc import ABC, abstractmethod
from src.game_world.objects.advanced_objects.gun.basic_gun import GunsID, GunsData
from src.multiplayer.client import Client


class Menu(ABC):
    @abstractmethod
    def __init__(self):
        self._canvas = Canvas()

    @property
    def canvas(self) -> Canvas:
        return self._canvas


class StartingMenu(Menu, metaclass=SingletonABC):

    def __init__(self):
        super().__init__()
        b_1_t = Text(0, 0, "Start game", "", 40)
        b_1 = Button(500, 500, 100, 100, YELLOW, self.__start_game, b_1_t)

        t_1 = Text(500, 50, "Welcome to start menu", "", 40)
        self.canvas.add_ui_object(b_1)
        self.canvas.add_ui_object(b_1_t)

        self.canvas.add_ui_object(t_1)
        self.canvas.hide_all()

    def __start_game(self, *args):
        """
        Go from start menu to game
        """
        EventListener.fire_events(GO_TO_MENU_STATE, MATCHMAKING_MENU)


class MatchMakingMenu(Menu, metaclass=SingletonABC):

    def __init__(self):
        super().__init__()
        t_1 = Text(500, 50, "waiting for players", "", 40)
        self.canvas.add_ui_object(t_1)
        self.canvas.hide_all()

    def __go_back_to_starting_menu(self, *args):
        """
        Go from start menu to game
        """
        EventListener.fire_events(GO_TO_MENU_STATE, STARTING_MENU)


class WonMenu(Menu, metaclass=SingletonABC):

    def __init__(self):
        super().__init__()

        b_1_text = Text(0, 0, "You Won", "", 20)

        b_3_text = Text(0, 0, "Play again", "", 20)
        b_3 = Button(400, 100, 100, 100, YELLOW, self.__reset_game, b_3_text)

        self.canvas.add_ui_object(b_1_text)
        self.canvas.add_ui_object(b_3)
        self.canvas.add_ui_object(b_3_text)

        self.canvas.hide_all()

    def __reset_game(self):
        """
        Return to game from settings menu
        """
        EventListener.fire_events(RESET_GAME)


class LostMenu(Menu, metaclass=SingletonABC):

    def __init__(self):
        super().__init__()

        b_1_text = Text(0, 0, "You Lost", "", 20)

        b_3_text = Text(0, 0, "Play again", "", 20)
        b_3 = Button(400, 100, 100, 100, YELLOW, self.__reset_game, b_3_text)

        self.canvas.add_ui_object(b_1_text)
        self.canvas.add_ui_object(b_3)
        self.canvas.add_ui_object(b_3_text)

        self.canvas.hide_all()

    def __reset_game(self):
        """
        Return to game from settings menu
        """
        EventListener.fire_events(RESET_GAME)



class ShopMenu(Menu, metaclass=SingletonABC):

    def __init__(self):
        super().__init__()
        b_1_text = Text(0, 0, f"Buy shotgun: {SHOTGUN_PRICE}", "", 20)
        b_1 = Button(100, 100, 100, 100, YELLOW, lambda: self.__create_gun(GunsID.SHOTGUN_ID), b_1_text)

        b_3_text = Text(0, 0, f"Buy rifle: {RIFLE_PRICE}", "", 20)
        b_3 = Button(400, 100, 100, 100, YELLOW, lambda: self.__create_gun(GunsID.RIFLE_ID), b_3_text)

        b_4_text = Text(0, 0, f"Buy sniper: {SNIPER_PRICE}", "", 20)
        b_4 = Button(550, 100, 100, 100, YELLOW, lambda: self.__create_gun(GunsID.SNIPER_ID), b_4_text)

        b_5_text = Text(0, 0, "Quit", "", 20)
        b_5 = Button(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 200, 100, 100, YELLOW, self.__return_to_game, b_5_text)

        self.canvas.add_ui_object(b_1)
        self.canvas.add_ui_object(b_1_text)

        self.canvas.add_ui_object(b_3)
        self.canvas.add_ui_object(b_3_text)
        self.canvas.add_ui_object(b_4)
        self.canvas.add_ui_object(b_4_text)

        self.canvas.add_ui_object(b_5)
        self.canvas.add_ui_object(b_5_text)

        self.canvas.hide_all()

    def __create_gun(self, gun_number: GunsID):
        """
        It gives the player the gun he clicked on
        """
        EventListener.fire_events(BUY_GUN, gun_number)

    def __return_to_game(self, *args):
        """
        Return to game from settings menu
        """
        EventListener.fire_events(GO_TO_GAME_STATE)

    def __go_to_settings_two_menu(self, *args):
        EventListener.fire_events(GO_TO_MENU_STATE, SETTINGS2_MENU)


class SettingsMenu(Menu, metaclass=SingletonABC):

    def __init__(self):
        super().__init__()
        b_1_text = Text(0, 0, "go back to game", "", 20)
        b_1 = Button(400, 500, 100, 100, YELLOW, self.__return_to_game, b_1_text)

        b_2_text = Text(0, 0, "go to settings 2", "", 20)
        b_2 = Button(100, 500, 100, 100, YELLOW, self.__go_to_settings_two_menu, b_2_text)

        t_1 = Text(500, 50, "Welcome to settings menu", "", 40)
        self.canvas.add_ui_object(b_1)
        self.canvas.add_ui_object(b_1_text)
        self.canvas.add_ui_object(b_2)
        self.canvas.add_ui_object(b_2_text)
        self.canvas.add_ui_object(t_1)
        self.canvas.hide_all()

    def __return_to_game(self, *args):
        """
        Return to game from settings menu
        """
        EventListener.fire_events(GO_TO_GAME_STATE)

    def __go_to_settings_two_menu(self, *args):
        EventListener.fire_events(GO_TO_MENU_STATE, SETTINGS2_MENU)


class Setting2sMenu(Menu, metaclass=SingletonABC):

    def __init__(self):
        super().__init__()
        b_1_text = Text(0, 0, "go back to game")
        b_1 = Button(400, 500, 100, 100, YELLOW, self.__return_to_game, b_1_text)

        t_1 = Text(500, 50, "Welcome to settings2 menu")
        self.canvas.add_ui_object(b_1)
        self.canvas.add_ui_object(b_1_text)

        self.canvas.add_ui_object(t_1)
        self.canvas.hide_all()

    def __return_to_game(self, *args):
        """
        Return to game from settings menu
        """
        EventListener.fire_events(GO_TO_GAME_STATE)
