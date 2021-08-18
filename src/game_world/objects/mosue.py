import pygame as pg
from src.structures.core_classes import Singleton
from src.core_functionaletize.event_system import EventListener

class Mouse(metaclass=Singleton):
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self):
        self.x, self.y = pg.mouse.get_pos()
