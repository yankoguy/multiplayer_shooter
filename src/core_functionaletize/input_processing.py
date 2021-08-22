import pygame as pg
from src.core_functionaletize.event_system import EventListener
from src.Consts.settings import *


def key_to_event():
    """
    Fire events from the user input
    """
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            EventListener.fire_events(KEY_DOWN + str(event.key))
        if event.type == pg.MOUSEBUTTONDOWN:
            EventListener.fire_events(MOUSE_LEFT_CLICK, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
