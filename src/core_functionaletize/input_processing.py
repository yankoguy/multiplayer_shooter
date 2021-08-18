import pygame as pg
from src.core_functionaletize.event_system import EventListener


def key_to_event():
    """
    Fire events from the user input
    """
    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            EventListener.fire_events(f"KEYDOWN:{event.key}")
        if event.type == pg.MOUSEBUTTONDOWN:
            EventListener.fire_events("left_click",pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])
