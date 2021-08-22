import pygame as pg
from src.structures.core_classes import Singleton
from enum import Enum
from src.game_world.objects.basic_objects import BaseObject
from src.Consts.settings import *
from src.game_world.rendering import RenderMode


class Tile(BaseObject):
    """
    Tile is a static object which is created by the map class from map.txt.
    attributes:
        map_x_index is the x index of the tile object in the map (0 is the most left)
        map_y_index is the y index of the tile object in the map (0 is the most top)
    """

    def __init__(self, color: tuple, map_x_index: int, map_y_index: int):
        super().__init__(map_x_index * TILE_WIDTH, map_y_index * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT,
                         RenderMode.SPRITE_RENDER_MODE, color)
        self.map_x_index = map_x_index
        self.map_y_index = map_y_index


class TileType(Enum):
    WATER = 1
    GRASS = 2


class Map(metaclass=Singleton):
    """
    The map is used to build the map of the game and the first object in there
    """
    __map_file = "D:\\Guy\\PycharmProjects\\multiplayer_game\\src\\game_world\\Map\\map.txt"
    __tile_symbols = {'0': BLUE, '1': GREEN}

    def __init__(self):
        self.__tiles = []
        self.__create_map()


    @property
    def tiles(self):
        return self.__tiles

    def __create_map(self):
        """
        Used to create the map of the game
        """
        with open(Map.__map_file, 'r') as tiles:
            for y_tile_index, line in enumerate(tiles):
                for x_tile_index, tile_symbol in enumerate(line.strip()):
                    self.tiles.append(Tile(Map.__tile_symbols[tile_symbol], x_tile_index, y_tile_index))
