from src.game_world.objects.advanced_objects.enemies.enemy import BasicEnemy
from src.core_functionaletize.game_time import Timer
import random
from src.core_functionaletize.event_system import EventListener
from src.Consts.settings import *

class Spawner:
    """
    Summons enemies
    """
    def __init__(self,x,y,spawn_time:float,enemy_targets:list):
        self.__pos = (x,y)
        self.__spawn_time = spawn_time
        self.__enemy_targets = enemy_targets
        self.__timer = Timer(spawn_time,self.__spawn_enemy)

    def update(self):
        self.__timer.update_timer()

    def __spawn_enemy(self):
        """
        spawns an enemy near spawner
        """
        enemy = BasicEnemy(self.__pos[0] + random.randint(-10,10),self.__pos[1] + random.randint(-10,10),
                           10,10,self.__enemy_targets,BASIC_ENEMY_IMAGE)
        self.__timer = Timer(self.__spawn_time,self.__spawn_enemy)
        EventListener.fire_events(WORLD_ADD_OBJECT, enemy)
