import pygame as pg
from src.game_world.objects.collision import CollisionMasks, CollisionPositions
from src.game_world.objects.basic_objects import AliveSprite
from src.multiplayer.network_object import NetworkObject
from src.core_functionaletize.game_time import GlobalTime
from src.Consts.settings import *
from src.game_world.UI.ui_enteties import Text
from src.core_functionaletize.event_system import EventListener
from src.game_world.objects.advanced_objects.items.item_collector import ItemCollector
from src.multiplayer.client import Client
from src.game_world.objects.advanced_objects.gun.basic_gun import Pistol, OnlinePistol, Rifle, OnlineRifle


class Player(AliveSprite, NetworkObject):
    """
    The Player is the object that the user has control on
    gun - the gun the player is holding now
    """

    def __init__(self, x, y, cllider_width, collider_height, gun: object, sprite_img: str):
        AliveSprite.__init__(self, x, y, cllider_width, collider_height, CollisionMasks.PLAYER,
                             (CollisionMasks.ENEMY,), PLAYER_HEALTH,
                             PLAYER_SPEED, PLAYER_POWER,
                             sprite_img=sprite_img)

        NetworkObject.__init__(self)
        self._gun = gun
        self.item_collector = ItemCollector()  # The items the player has

    def switch_gun(self, new_gun):
        """replace the current gun that the player is holding with a new on"""
        self._gun.destroy()
        self._gun = new_gun

    def take_hit(self, dmg_to_take):
        self._health -= dmg_to_take

    def update(self):
        self.collider.update(self.rect.x - self._vx,
                             self.rect.y - self._vy)  # Update the collider to the position the player wants to move to
        self._gun.stick_to_holder(self.rect.x + 5,self.rect.y + 5)

    @property
    def online_object(self):
        return self._online_object


class LocalPlayer(Player):
    def __init__(self, x, y, cllider_width, collider_height, gun:object, sprite_img: str):
        super().__init__(x, y, cllider_width, collider_height, gun, sprite_img)

        self.__player_health_text = Text(WINDOW_WIDTH / 4, 0, "health: ", str(self._health), 20)
        EventListener.fire_events(WORLD_ADD_OBJECT, self.__player_health_text)
        self.__player_health_text.change_text(f"player health: {self._health}")

        EventListener.fire_events(WORLD_ADD_OBJECT, self.item_collector.items[COINS][ItemCollector.TEXT_INDEX])

        self._online_object = False

    def _calculate_velocity(self):
        keys = pg.key.get_pressed()
        self._vx, self._vy = 0, 0
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and CollisionPositions.LEFT not in self.collider.collistion_positions:
            # Apply velocity to right
            self._vx += self._speed

        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and CollisionPositions.RIGHT not in self.collider.collistion_positions:
            # Apply velocity to left
            self._vx -= self._speed

        if (keys[pg.K_UP] or keys[pg.K_w]) and CollisionPositions.TOP not in self.collider.collistion_positions:
            # Apply velocity to top
            self._vy += self._speed

        if (keys[pg.K_DOWN] or keys[pg.K_s]) and CollisionPositions.BOTTOM not in self.collider.collistion_positions:
            # Apply velocity to bottom
            self._vy -= self._speed


        self._vx *= GlobalTime.delta_time()  # Delta time the velocity to make it smooth
        self._vy *= GlobalTime.delta_time()  # Delta time the velocity to make it smooth

    def _movement(self):
        if CollisionPositions.LEFT in self.collider.collistion_positions or self.rect.x <= 0:
            # Checks for right border
            if self._vx > 0:
                self._vx = 0

        if CollisionPositions.RIGHT in self.collider.collistion_positions or self.rect.x + self._collider.width >= MAP_WIDTH:
            # Checks for left border
            if self._vx < 0:
                self._vx = 0

        if CollisionPositions.TOP in self.collider.collistion_positions or self.rect.y <= 0:
            # Checks for top border
            if self._vy > 0:
                self._vy = 0

        if CollisionPositions.BOTTOM in self.collider.collistion_positions or self.rect.y + self._collider.height >= MAP_HEIGHT:
            # Checks for bottom border
            if self._vy < 0:
                self._vy = 0

        self._rect.x -= self._vx
        self._rect.y -= self._vy

    def update(self):
        self._calculate_velocity()
        super().update()

    def late_update(self):
        self._movement()
        Client.add_data_to_send(NETWORK_PLAYER_POS, (self.rect.x, self.rect.y))
        super().late_update()


class OnlinePlayer(Player):
    def __init__(self, x, y, cllider_width, collider_height, gun:object, sprite_img: str):
        super().__init__(x, y, cllider_width, collider_height, gun, sprite_img)
        self._online_object = True

    def late_update(self):
        data = Client.get_data(NETWORK_PLAYER_POS)
        if data is not None:
            self._rect.x, self._rect.y = data
        data = Client.get_data(NETWORK_NEW_GUN)
        if data == 1:
            g = OnlinePistol()
            EventListener.fire_events(WORLD_ADD_OBJECT, g)
            self.switch_gun(g)
        if data==2:
            g = OnlineRifle()
            EventListener.fire_events(WORLD_ADD_OBJECT, g)
            self.switch_gun(g)