import pygame as pg
from src.Consts.settings import *
from src.game_world.camera import Camera

def show_colliders_object(screen,sprites:list) -> None:
    """
    Draw to screen the collider of an object (for debbuging purpose)
    """
    for sprite in sprites:
        collider = sprite.collider
        world_pos = Camera.normal_to_world_pos((sprite.rect.x,sprite.rect.y))
        pg.draw.rect(screen, BLACK, (collider.x,collider.y, collider.width, collider.height), 1)