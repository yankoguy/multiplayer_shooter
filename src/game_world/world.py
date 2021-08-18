from src.core_functionaletize.game_time import GlobalTime
from src.structures.core_classes import Singleton
from src.Consts.settings import *
from src.game_world.window import Window
from src.game_world.objects.advanced_objects.Player.player import Player
from src.game_world.objects.advanced_objects.enemies.enemy import BasicEnemy
from src.game_world.UI.ui_enteties import Text,Button
from src.game_world.rendering import RenderMode
from src.game_world.objects.collision import CollisionMasks
from src.game_world.Map.map import Map
import debbuging

class World(metaclass=Singleton):
    """
    The world is used to apply changes on all the objects in the game
    """

    def __init__(self):
        # Game objects
        self._sprites = []  # All the sprites entities in game
        self._ui = []  # All the UI entities in game
        self._texts = []
        self._buttons = []

        # Singleton objects
        self._window = Window()
        self._game_timer = GlobalTime()
        self._map = Map()

        self._create_world()

    def _create_world(self):
        # Create the map and the objects (the map will create the objects and return them)
        self._sprites.append(Player(400, 300, 30, 50, CollisionMasks.PLAYER,
                                    "D:\\Guy\\PycharmProjects\\multiplayer_game\\images\\sprites"
                                    "\\solider.png"))
        self._sprites.append(BasicEnemy(100, 100, 30, 50, CollisionMasks.ENEMIES,
                                        "D:\\Guy\\PycharmProjects\\multiplayer_game\\images\\sprites"
                                        "\\solider.png"))

        self._texts.append(Text(400, 400, "first text", 20))


    def update(self):
        """
        Runs every frame and update every single object that need to be updated
        """
        self._show_objects()

        self._window.update()
        self._game_timer.update()
        self._collision()

        self._update_sprites()
        self._late_update_sprites()

    def _collision(self):
        """
        Check colliders collisions
        """
        for sprite in self._sprites:
            sprite.collider.get_collision(self._sprites)

    def _update_sprites(self):
        """
        Update all sprites in game
        """
        for sprite in self._sprites:
            sprite.update()

    def _late_update_sprites(self):
        """
           LateUpdate all sprites in game
        """
        for sprite in self._sprites:
            sprite.late_update()

    def _show_objects(self):
        self._window.clear_screen(WHITE)
        self._window.draw_objects_on_screen(self._map.tiles, RenderMode.SPRITE_RENDER_MODE)
        self._window.draw_objects_on_screen(self._sprites, RenderMode.SPRITE_RENDER_MODE)
        self._window.draw_objects_on_screen(self._texts, RenderMode.TEXT_RENDER_MODE)
        self._window.draw_objects_on_screen(self._buttons, RenderMode.SPRITE_RENDER_MODE)

        debbuging.show_colliders_object(self._window._screen,self._sprites)
