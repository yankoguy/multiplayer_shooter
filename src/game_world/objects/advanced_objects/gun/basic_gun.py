import pygame as pg
from src.game_world.objects.basic_objects import UpdatedObject
from src.Consts.settings import *
import src.core_functionaletize.utilitiez as utilitiez
from src.core_functionaletize.event_system import EventListener
from src.game_world.objects.advanced_objects.gun.bullet import Bullet
from src.game_world.objects.collision import CollisionMasks
from src.multiplayer.client import Client
from src.game_world.camera import Camera
from src.core_functionaletize.game_time import Timer
from src.game_world.UI.ui_enteties import Text
from src.multiplayer.network_object import NetworkObject
from enum import Enum


class GunsID(Enum):
    """
    Enum that contains all guns id
    """
    PISTOL_ID = 0
    RIFLE_ID = 1
    SHOTGUN_ID = 2
    SNIPER_ID = 3

    ONLINE_PISTOL_ID = 10
    ONLINE_RIFLE_ID = 11
    ONLINE_SHOTGUN_ID = 12
    ONLINE_SNIPER_ID = 13


class Gun(UpdatedObject, NetworkObject):
    """
    Gun is an object that rotate to mouse and can shoot bullets
    attributes:
        time_between_shots - how much time should you wait before you shoot another shoot
        ammo - how much ammo does the guy have when you got him
        max_ammo - what is the maximun ammount of ammo it can have
        gun_power_multiplier - how much power does the gun adds to the bullet
        gun_speed_multiplier - how much speed does the gun adds to the bullet
        online_object - if the gun holds by the onlune player this will be True
    """

    def __init__(self, x_offset, y_offset, time_between_shoots: float, ammo: int,
                 _magazine_size: int,
                 gun_power_multiplier: float, gun_speed_multiplier: float, gun_health_multiplier: int, price: int,
                 gunID: GunsID,
                 object_img: str):

        super().__init__(0, 0, 0, 0, WHITE, object_img)

        NetworkObject.__init__(self)

        self._gun_power_multiplier = gun_power_multiplier
        self._gun_speed_multiplier = gun_speed_multiplier
        self._gun_health_multiplier = gun_health_multiplier  # How much times can it hit something before die
        self._time_between_shoots = time_between_shoots
        self._shot_timer = Timer(self._time_between_shoots)
        self.ammo = ammo
        self._ammo_in_magazine = 0
        self._magazine_size = _magazine_size
        self._current_angle = 0
        self._x_offset = x_offset
        self._y_offset = y_offset
        self.__price = price
        self.__gunID = gunID

    @property
    def price(self):
        return self.__price

    @property
    def gunID(self):
        return self.__gunID

    def update(self):
        self._shot_timer.update_timer()

    def stick_to_holder(self, x, y):
        """
        Changes the gun position (in order to stay near the holder)
        """
        self._rect.x = x + self._x_offset
        self._rect.y = y + self._y_offset

    def _rotate_to_mouse(self, angle: float):
        """
              Returns new rect and image of the sprite in certina angle
        """
        self._current_angle = angle
        rotated_image = pg.transform.rotate(self._image, angle)
        new_rect = rotated_image.get_rect(center=self._image.get_rect(topleft=self.rect.topleft).center)
        return rotated_image, new_rect

    def _create_bullet_to_shot(self) -> list:
        return [Bullet(self.rect.x + 5, self.rect.y + 5, CollisionMasks.BULLET, (CollisionMasks.ENEMY,),
                       self._current_angle,
                       BULLET_BASE_HEALTH * self._gun_health_multiplier, BULLET_BASE_SPEED * self._gun_speed_multiplier,
                       BULLET_BASE_POWER * self._gun_power_multiplier,
                       BULLET_IMAGE)]

    def _reload_gun(self):
        if self.ammo > self._magazine_size:
            self.ammo -= self._magazine_size
            self._ammo_in_magazine = self._magazine_size
        else:
            self._ammo_in_magazine = self.ammo
            self.ammo=0


    def _shoot(self, *args):
        if self._ammo_in_magazine > 0 and self._shot_timer.finish:
            bullets = self._create_bullet_to_shot()
            for bullet in bullets:
                EventListener.fire_events(WORLD_ADD_OBJECT, bullet)
            self._shot_timer = Timer(self._time_between_shoots)  # reset Timer
            self._ammo_in_magazine -= 1


class LocalGun(Gun):
    def __init__(self, x, y, time_between_shoots: float, ammo: int,
                 max_ammo: int,
                 gun_power_multiplier: float, gun_speed_multiplier: float, gun_health_multiplier: int, price, gunID,
                 object_img: str):
        super().__init__(x, y, time_between_shoots, ammo, max_ammo, gun_power_multiplier,
                         gun_speed_multiplier, gun_health_multiplier, price, gunID,
                         object_img)

        self._ammo_text = Text(WINDOW_WIDTH / 6 * 5 , 0, "magazine: ", str(self._ammo_in_magazine), 20)
        EventListener.fire_events(WORLD_ADD_OBJECT, self._ammo_text)
        EventListener.add_handler(KEY_DOWN+str(pg.K_SPACE), self._reload_gun)

    def _reload_gun(self):
        super()._reload_gun()
        self._ammo_text.change_text(str(self._ammo_in_magazine))

    def die(self):
        self._ammo_text.destroy()

    def _shoot(self, *args):
        super()._shoot()
        self._ammo_text.change_text(str(self._ammo_in_magazine))

    def render_properties(self) -> tuple:
        world_pos = Camera.normal_to_world_pos(pg.mouse.get_pos())
        angle = int(utilitiez.get_angle(self.rect.x, self.rect.y, world_pos[0], world_pos[1]))
        Client.add_data_to_send(NETWORK_GUN_ROTATION, angle)
        return self._rotate_to_mouse(angle)


class OnlineGun(Gun):
    def __init__(self, x, y, time_between_shoots: float, ammo: int,
                 max_ammo: int,
                 gun_power_multiplier: float, gun_speed_multiplier: float, gun_health_multiplier: int, price, gunID,
                 object_img: str):
        super().__init__(x, y, time_between_shoots, ammo, max_ammo, gun_power_multiplier,
                         gun_speed_multiplier, gun_health_multiplier, price, gunID,
                         object_img)
        self._online_object = True

    def render_properties(self) -> tuple:
        angle = Client.get_data(NETWORK_GUN_ROTATION)
        if angle is None:
            angle = self._current_angle
        reload = Client.get_data(NETWORK_KEYDOWN + str(pg.K_SPACE))
        if reload:
            self._reload_gun()
        return self._rotate_to_mouse(angle)


class Pistol(LocalGun):
    def __init__(self,ammo):
        super().__init__(5, -5, PISTOL_TIME_BETWEEN_SHOTS, ammo, PISTOL_MAGAZINE_SIZE,
                         PISTOL_POWER_MULTIPLIER, PISTOL_SPEED_MULTIPLIER, PISTOL_HEALTH_MULTIPLIER, PISTOL_PRICE,
                         GunsID.PISTOL_ID,
                         PISTOL_IMAGE)
        EventListener.add_handler(MOUSE_LEFT_CLICK, self._shoot)

    def die(self):
        EventListener.remove_handler(MOUSE_LEFT_CLICK, self._shoot)
        super().die()


class OnlinePistol(OnlineGun):
    def __init__(self,ammo):
        super().__init__(5, -5, PISTOL_TIME_BETWEEN_SHOTS, ammo, PISTOL_MAGAZINE_SIZE,
                         PISTOL_POWER_MULTIPLIER, PISTOL_SPEED_MULTIPLIER, PISTOL_HEALTH_MULTIPLIER, PISTOL_PRICE,
                         GunsID.ONLINE_PISTOL_ID,
                         PISTOL_IMAGE)

    def update(self):
        if Client.get_data(NETWORK_MOUSE_LEFT_CLICK):
            self._shoot()
        super().update()


class Rifle(LocalGun):
    def __init__(self,ammo):
        super().__init__(10, -10, RIFLE_TIME_BETWEEN_SHOTS, ammo, RIFLE_MAGAZINE_SIZE,
                         RIFLE_POWER_MULTIPLIER, RIFLE_SPEED_MULTIPLIER, RIFLE_HEALTH_MULTIPLIER, RIFLE_PRICE,
                         GunsID.RIFLE_ID,
                         RIFLE_IMAGE)

        EventListener.add_handler(MOUSE_LEFT_PRESSED, self._shoot)

    def die(self):
        EventListener.remove_handler(MOUSE_LEFT_PRESSED, self._shoot)
        super().die()


class OnlineRifle(OnlineGun):
    def __init__(self,ammo):
        super().__init__(10, -10, RIFLE_TIME_BETWEEN_SHOTS, ammo, RIFLE_MAGAZINE_SIZE,
                         RIFLE_POWER_MULTIPLIER, RIFLE_SPEED_MULTIPLIER, RIFLE_HEALTH_MULTIPLIER, RIFLE_PRICE,
                         GunsID.ONLINE_RIFLE_ID,
                         RIFLE_IMAGE)

    def update(self):
        if Client.get_data(NETWORK_MOUSE_LEFT_PRESSED):
            self._shoot()
        super().update()


class Sniper(LocalGun):
    def __init__(self,ammo):
        super().__init__(10, -10, SNIPER_TIME_BETWEEN_SHOTS, ammo, SNIPER_MAGAZINE_SIZE,
                         SNIPER_POWER_MULTIPLIER, RIFLE_SPEED_MULTIPLIER, SNIPER_HEALTH_MULTIPLIER, SNIPER_PRICE,
                         GunsID.SNIPER_ID,
                         SNIPER_IMAGE)
        EventListener.add_handler(MOUSE_LEFT_CLICK, self._shoot)


    def die(self):
        EventListener.remove_handler(MOUSE_LEFT_CLICK, self._shoot)
        super().die()

class OnlineSniper(OnlineGun):
    def __init__(self,ammo):
        super().__init__(10, -10, SNIPER_TIME_BETWEEN_SHOTS, ammo, SNIPER_MAGAZINE_SIZE,
                         SNIPER_POWER_MULTIPLIER, RIFLE_SPEED_MULTIPLIER, SNIPER_HEALTH_MULTIPLIER, SNIPER_PRICE,
                         GunsID.ONLINE_SNIPER_ID,
                         SNIPER_IMAGE)

    def update(self):
        if Client.get_data(NETWORK_MOUSE_LEFT_PRESSED):
            self._shoot()
        super().update()

class Shotgun(LocalGun):
    def __init__(self,ammo):
        super().__init__(10, -10, SHOTGUN_TIME_BETWEEN_SHOTS, ammo, SHOTGUN_MAGAZINE_SIZE,
                         SHOTGUN_POWER_MULTIPLIER, SHOTGUN_SPEED_MULTIPLIER, SHOTGUN_HEALTH_MULTIPLIER, SHOTGUN_PRICE,
                         GunsID.SHOTGUN_ID,
                         SHOTGUN_IMAGE)
        EventListener.add_handler(MOUSE_LEFT_CLICK, self._shoot)

    def __get_bullet_angle(self, bullet_number) -> float:
        """
        returns the angle of a bullet from a shotgun (they spread)
        """
        place = 1 if bullet_number % 2 == 0 else -1  # if the bullet position is odd it will go down if even it will go up
        return self._current_angle + bullet_number * SHOTGUN_ANGLE_CHANGE * place

    def _create_bullet_to_shot(self) -> list:
        bullets = []
        for i in range(SHOTGUN_BULLET_NUMBER):
            bullets.append(Bullet(self.rect.x + 5, self.rect.y + 5, CollisionMasks.BULLET, (CollisionMasks.ENEMY,),
                                  self.__get_bullet_angle(i),
                                  BULLET_BASE_HEALTH, BULLET_BASE_SPEED * self._gun_speed_multiplier,
                                  BULLET_BASE_POWER * self._gun_power_multiplier,
                                  BULLET_IMAGE))

        return bullets

    def die(self):
        EventListener.remove_handler(MOUSE_LEFT_CLICK, self._shoot)
        super().die()


class OnlineShotgun(OnlineGun):
    def __init__(self,ammo):
        super().__init__(10, -10, SHOTGUN_TIME_BETWEEN_SHOTS, ammo, SHOTGUN_MAGAZINE_SIZE,
                         SHOTGUN_POWER_MULTIPLIER, SHOTGUN_SPEED_MULTIPLIER, SHOTGUN_HEALTH_MULTIPLIER, SHOTGUN_PRICE,
                         GunsID.SHOTGUN_ID,
                         SHOTGUN_IMAGE)

    def __get_bullet_angle(self, bullet_number) -> float:
        """
        returns the angle of a bullet from a shotgun (they spread)
        """
        place = 1 if bullet_number % 2 == 0 else -1  # if the bullet position is odd it will go down if even it will go up
        return self._current_angle + bullet_number * SHOTGUN_ANGLE_CHANGE * place

    def _create_bullet_to_shot(self) -> list:
        bullets = []
        for i in range(SHOTGUN_BULLET_NUMBER):
            bullets.append(Bullet(self.rect.x + 5, self.rect.y + 5, CollisionMasks.BULLET, (CollisionMasks.ENEMY,),
                                  self.__get_bullet_angle(i),
                                  BULLET_BASE_HEALTH, BULLET_BASE_SPEED * self._gun_speed_multiplier,
                                  BULLET_BASE_POWER * self._gun_power_multiplier,
                                  BULLET_IMAGE))

        return bullets

    def update(self):
        if Client.get_data(NETWORK_MOUSE_LEFT_PRESSED):
            self._shoot()
        super().update()



class GunsData:
    Guns = {GunsID.PISTOL_ID: Pistol, GunsID.RIFLE_ID: Rifle, GunsID.SHOTGUN_ID: Shotgun, GunsID.SNIPER_ID: Sniper,
            GunsID.ONLINE_PISTOL_ID: OnlinePistol, GunsID.ONLINE_RIFLE_ID: OnlineRifle,
            GunsID.ONLINE_SHOTGUN_ID: OnlineShotgun,
            GunsID.ONLINE_SNIPER_ID: OnlineSniper}  # A dictionary to hold all guns IDs

    @staticmethod
    def gunID_to_online_gunID(gunID: GunsID) -> GunsID:
        """
        returns gun id of the same gun but te online version
        """
        return GunsID(gunID.value + 10)
