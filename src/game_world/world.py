from src.structures.meta_classes import Singleton
from src.Consts.settings import *
from src.game_world.objects.basic_objects import RenderAbleObj, UpdatedObject, Sprite
from src.game_world.objects.advanced_objects.Player.player import LocalPlayer, OnlinePlayer
from src.game_world.objects.advanced_objects.enemies.enemy import BasicEnemy
from src.game_world.UI.menus import StartingMenu, SettingsMenu, Setting2sMenu, MatchMakingMenu,ShopMenu,WonMenu,LostMenu
from src.game_world.Map.map import Map
from src.game_world.objects.advanced_objects.gun.basic_gun import Pistol, OnlinePistol, Rifle, OnlineRifle
from src.core_functionaletize.event_system import EventListener
from src.game_world.objects.advanced_objects.items.coin import Coin
from src.game_world.objects.advanced_objects.enemies.enemy_spawner import Spawner
import pygame as pg
from src.multiplayer.client import Client


class World(metaclass=Singleton):
    """
    The _world is used to apply changes on all the objects in the game
    """

    def __init__(self):
        # Game objects
        self.__objects = []  # All the object that should be rendered
        self.__updated_objects = []  # All the object that should be updated
        self._sprites = []  # All the sprites entities in game
        self.__menus = {}  # All the canvases in game
        self.__player = None  # The player is an important object for the rest of the game
        self.spawners = []

        # Singleton objects
        self.__map = Map()
        self.__objects += self.__map.tiles  # Add tiles to map

        # Event
        EventListener.add_handler(WORLD_ADD_OBJECT, self.__add_rederable_object)

        self.__create_world()

    @property
    def menus(self):
        return self.__menus


    def reset(self):
        self.__objects = []  # All the object that should be rendered
        self.__updated_objects = []  # All the object that should be updated
        self._sprites = []  # All the sprites entities in game
        self.__player = None  # The player is an important object for the rest of the game
        self.spawners = []
        self.__objects += self.__map.tiles  # Add tiles to map
        self.__create_world()

    def __create_world(self):
        # Create texts--------------------------------

        # Create object in game--------------------------------------

        g = Pistol(STARTING_AMMO)

        self.__add_rederable_object(g)

        g2 = OnlinePistol(STARTING_AMMO)

        self.__add_rederable_object(g2)

        self.__player = LocalPlayer(10, 10, 30, 50, g,
                                    PLAYER_IMAGE)

        self.__add_rederable_object(self.__player)

        p2 = OnlinePlayer(2000, 2000, 30, 50, g2,
                          ONLINE_PLAYER_IMAGE)

        self.__add_rederable_object(p2)

        self.spawners.append(Spawner(0, 0, 2, [self.__player, p2]))
        self.spawners.append(Spawner(1000, 1000, 3, [self.__player, p2]))
        self.spawners.append(Spawner(2000, 2000, 5, [self.__player, p2]))

        if not self.menus:
            self.create_menus()
        # Create menus------------------------------------------

    def create_menus(self):
        starting_menu = StartingMenu()
        starting_menu.canvas.apply_function_on_UI_objects(self.__add_rederable_object)
        self.__menus[STARTING_MENU] = starting_menu

        matchmaking_menu = MatchMakingMenu()
        matchmaking_menu.canvas.apply_function_on_UI_objects(self.__add_rederable_object)
        self.__menus[MATCHMAKING_MENU] = matchmaking_menu

        shop_menu = ShopMenu()
        shop_menu.canvas.apply_function_on_UI_objects(self.__add_rederable_object)
        self.__menus[SHOP_MENU] = shop_menu

        settings_menu = SettingsMenu()
        settings_menu.canvas.apply_function_on_UI_objects(self.__add_rederable_object)
        self.__menus[SETTINGS_MENU] = settings_menu

        settings_menu2 = Setting2sMenu()
        settings_menu2.canvas.apply_function_on_UI_objects(self.__add_rederable_object)
        self.__menus[SETTINGS2_MENU] = settings_menu2

        won_menu = WonMenu()
        won_menu.canvas.apply_function_on_UI_objects(self.__add_rederable_object)
        self.__menus[WON_MENU] = won_menu

        lost_menu = LostMenu()
        lost_menu.canvas.apply_function_on_UI_objects(self.__add_rederable_object)
        self.__menus[LOST_MENU] = lost_menu

    def get_player(self):
        return self.__player

    def get_objects_to_render(self):
        return self.__objects

    def hide_all_menus(self):
        """
        Hide all menus in game
        """
        for menu in self.__menus.values():
            menu.canvas.hide_all()

    def hide_all_objects(self):
        """
        Hide everything in game
        """
        for obj in self.__objects:
            obj.hide()

    def show_all_objects(self):
        """
        Show everything in game
        """
        for obj in self.__objects:
            obj.show()

    def update(self):
        """
        Runs every frame and update every single object that need to be updated
        """
        for spawner in self.spawners:
            spawner.update()
        self.__remove_objects()
        self.__update_objects()
        self.__collision()
        self.__late_update_sprites()

    def __add_rederable_object(self, object_to_add: RenderAbleObj):
        """
        Add object to the list of baseObjects
        """
        self.__objects.append(object_to_add)
        if isinstance(object_to_add, UpdatedObject):
            self.__add_updated_object(object_to_add)

    def __add_updated_object(self, object_to_add: UpdatedObject):
        """
            Add object to the list of UpdatedObjects
        """
        self.__updated_objects.append(object_to_add)
        object_to_add.start()
        if isinstance(object_to_add, Sprite):
            self.__add_sprite(object_to_add)

    def __add_sprite(self, object_to_add: Sprite):
        """
            Add object to the list of AliveObjects
        """
        self._sprites.append(object_to_add)

    def __collision(self):
        """
        Check colliders collisions
        """
        for sprite in self._sprites:
            sprite.collider.get_collision(self._sprites)

    def __remove_objects(self):
        for obj in self.__objects:
            if not obj.exists:
                # If object need to be dead remove him from game
                self.__remove_object(obj)

    def __update_objects(self):
        """
        Update all sprites in game
        """
        for updated_obj in self.__updated_objects:
            updated_obj.update()

    def __late_update_sprites(self):
        """
           LateUpdate all sprites in game
        """
        for updated_obj in self.__updated_objects:
            updated_obj.late_update()

    def __remove_object(self, object_to_remove):
        self.__objects.remove(object_to_remove)
        if isinstance(object_to_remove, UpdatedObject):
            self.__updated_objects.remove(object_to_remove)
            object_to_remove.die()
            if isinstance(object_to_remove, Sprite):
                self._sprites.remove(object_to_remove)
