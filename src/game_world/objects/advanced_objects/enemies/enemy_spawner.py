from src.game_world.objects.advanced_objects.enemies.enemy import BasicEnemy
from src.core_functionaletize.game_time import Timer
import random
from src.core_functionaletize.event_system import EventListener
from src.Consts.settings import *
from src.game_world.camera import Camera
from src.multiplayer.network_object import NetworkObject
from src.multiplayer.client import Client


class Spawner(NetworkObject):
    """
    Summons enemies
    """

    def __init__(self, x, y, spawn_time: float, enemy_targets: list):
        self.__pos = [x, y]
        self.__spawn_time = spawn_time
        self.__enemy_targets = enemy_targets
        self.__timer = Timer(spawn_time, self.__spawn_enemy)

        NetworkObject.__init__(self, True)
        Client.add_data_to_send(NETWORK_SPAWNER_POS, self.__pos, self._network_id)

    def update(self):
        self.__timer.update_timer()
        new_pos = Client.get_data(NETWORK_SPAWNER_POS + str(self._network_id))

        if new_pos is not None:
            self.__pos = new_pos

        else:
            while Camera.is_on_camera(self.__pos[0], self.__pos[1], ENEMY_WIDTH, ENEMY_HEIGHT):
                self.__pos[0] = random.randint(0, MAP_WIDTH)
                self.__pos[1] = random.randint(0, MAP_HEIGHT)
                Client.add_data_to_send(NETWORK_SPAWNER_POS, self.__pos, self._network_id)

    def __spawn_enemy(self):
        """
        spawns an enemy near spawner
        """
        enemy = BasicEnemy(self.__pos[0], self.__pos[1],
                           30, 30, self.__enemy_targets, BASIC_ENEMY_IMAGE)
        self.__timer = Timer(self.__spawn_time, self.__spawn_enemy)
        EventListener.fire_events(WORLD_ADD_OBJECT, enemy)
