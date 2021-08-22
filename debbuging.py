import pygame as pg
from src.Consts.settings import *

def show_colliders_object(DISPLAY:object,sprites:list) -> None:
    """
    Draw to screen the collider of an object (for debbuging purpose)
    """
    for sprite in sprites:
        collider = sprite.collider
        pg.draw.rect(DISPLAY, DEBUGGING_COLOR, (collider.x, collider.y, collider.width, collider.height), 1)