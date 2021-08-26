import pygame as pg
from src.Consts.settings import *
from src.game_world.camera import Camera

def show_colliders_object(screen,sprites:list) -> None:
    """
    Draw to screen the collider of an object (for debbuging purpose)
    """
    for sprite in sprites:
        collider = sprite.collider
        world_pos = Camera.screen_pos_to_world_pos((sprite.rect.x,sprite.rect.y))
        pg.draw.rect(screen, BLACK, (world_pos[0],world_pos[1], collider.width, collider.height), 1)