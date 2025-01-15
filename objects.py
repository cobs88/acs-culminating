import random
from renderer import render_element
import pygame as pg

from renderer import calc_y, calc_z

class GameObject:
    def __init__(self, distance):
        self.sprite = None
        self.w_scale_factor = 200
        self.h_scale_factor = 200
        self.x = distance
        self.y = None
        self.z = 0
        
    def render(self, screen, car, z_buffer):
        scale = max(0.0001, 1 / (self.x - car.x))
        render_element(screen, self.sprite, scale * self.w_scale_factor, scale * self.h_scale_factor, scale, self.x, car, self.y + car.y, 0, z_buffer)

    def get_hitbox(self, car):
        scale = max(0.0001, 1 / (self.x - car.x))
        y = calc_y(self.x) - (self.y + car.y)
        z = calc_z(self.x) - car.z

        vertical = int(60 + 160 * scale + z * scale)
        if vertical >= 1 and vertical < 180:
            horizontal = 160 - (160 - y) * scale + car.angle * (vertical - 150)

            hitbox_width = scale * self.w_scale_factor
            hitbox_height = scale * self.h_scale_factor

            return pg.Rect(horizontal, vertical - hitbox_height + 1, hitbox_width, hitbox_height)
        return None
    
    def check_collision(self, car, hitbox):
        object_hitbox = self.get_hitbox(car)
        car_hitbox = hitbox

        if object_hitbox and car_hitbox and object_hitbox.colliderect(car_hitbox):
            return True
            
        return False


class StaticObject(GameObject):
    def __init__(self, distance):
        super().__init__(distance)
        self.distance = distance
        self.x = self.distance
        self.y = random.randint(500, 1500) * random.choice([-1, 1])
        self.w_scale_factor = 600
        self.h_scale_factor = 600

    def update(self, delta, car):
        if self.x < car.x + 1:
            return True
        return False

class Cactus(StaticObject):
    def __init__(self, distance):
        super().__init__(distance)
        self.sprite = pg.image.load("assets/cactus.png").convert_alpha()
        self.w_scale_factor = 300
        self.h_scale_factor = 300

    def get_hitbox(self, car):
        scale = max(0.0001, 1 / (self.x - car.x))
        y = calc_y(self.x) - (self.y + car.y)
        z = calc_z(self.x) - car.z

        vertical = int(60 + 160 * scale + z * scale)
        if vertical >= 1 and vertical < 180:
            horizontal = 160 - (160 - y) * scale + car.angle * (vertical - 150)

            stalk_width = scale * self.w_scale_factor * 0.2
            stalk_height = scale * self.h_scale_factor

            hitbox_x = horizontal + (self.w_scale_factor * scale * 0.4)
            hitbox_y = vertical - stalk_height + 1

            return pg.Rect(hitbox_x, hitbox_y, stalk_width, stalk_height)
        return None

class Snowman(StaticObject):
    def __init__(self, distance):
        super().__init__(distance)

        self.sprite = pg.image.load("assets/snowman.png").convert_alpha()

        self.w_scale_factor = 150
        self.h_scale_factor = 150

class ChristmasTree(StaticObject):
    def __init__(self, distance):
        super().__init__(distance)

        self.sprite = pg.image.load("assets/christmas_tree.png").convert_alpha()

        self.w_scale_factor = 400
        self.h_scale_factor = 400

    def get_hitbox(self, car):
        scale = max(0.0001, 1 / (self.x - car.x))
        y = calc_y(self.x) - (self.y + car.y)
        z = calc_z(self.x) - car.z

        vertical = int(60 + 160 * scale + z * scale)
        if vertical >= 1 and vertical < 180:
            horizontal = 160 - (160 - y) * scale + car.angle * (vertical - 150)

            trunk_width = scale * self.w_scale_factor * 0.2
            trunk_height = scale * self.h_scale_factor

            hitbox_x = horizontal + (self.w_scale_factor * scale * 0.4)
            hitbox_y = vertical - trunk_height + 1

            return pg.Rect(hitbox_x, hitbox_y, trunk_width, trunk_height)
        return None

class Tree(StaticObject):
    def __init__(self, distance):
        super().__init__(distance)

        self.sprite = pg.image.load("assets/tree.png").convert_alpha()

        self.w_scale_factor = 400
        self.h_scale_factor = 400

    def get_hitbox(self, car):
        scale = max(0.0001, 1 / (self.x - car.x))
        y = calc_y(self.x) - (self.y + car.y)
        z = calc_z(self.x) - car.z

        vertical = int(60 + 160 * scale + z * scale)
        if vertical >= 1 and vertical < 180:
            horizontal = 160 - (160 - y) * scale + car.angle * (vertical - 150)

            trunk_width = scale * self.w_scale_factor * 0.2
            trunk_height = scale * self.h_scale_factor

            hitbox_x = horizontal + (self.w_scale_factor * scale * 0.4)
            hitbox_y = vertical - trunk_height + 1

            return pg.Rect(hitbox_x, hitbox_y, trunk_width, trunk_height)
        return None

class Helicopter(GameObject):
    def __init__(self, distance):
        super().__init__(distance)

        self.sprite = pg.image.load("assets/helicopter.png").convert_alpha()

        self.x = distance
        self.y = -70

        self.w_scale_factor = 2000
        self.h_scale_factor = 1000

    def update(self, delta, car):
        self.z = 350
        self.x = car.x + 20
        self.y = car.y + 450

    def render(self, screen, car, z_buffer):
        scale = max(0.0001, 1 / (self.x - car.x))
        render_element(screen, self.sprite, scale * self.w_scale_factor, scale * self.h_scale_factor, scale, self.x, car, self.y, -self.z, z_buffer)

    def get_hitbox(self, car):
        scale = max(0.0001, 1 / (self.x - car.x))
        y = calc_y(self.x) - (self.y + car.y)
        z = calc_z(self.x) - car.z - self.z

        vertical = int(60 + 160 * scale + z * scale)
        if vertical >= 1 and vertical < 180:
            horizontal = 160 - (160 - y) * scale + car.angle * (vertical - 150)

            hitbox_width = scale * self.w_scale_factor
            hitbox_height = scale * self.h_scale_factor

            return pg.Rect(horizontal, vertical - hitbox_height + 1, hitbox_width, hitbox_height)
        return None

        
    

class OncomingCar(GameObject):
    def __init__(self, distance):
        super().__init__(distance)

        self.sprite = random.choice([
            pg.image.load("assets/soul.png").convert_alpha(),
            pg.image.load("assets/civic.png").convert_alpha()
        ])

        self.x = distance
        self.y = -70

        self.w_scale_factor = 150
        self.h_scale_factor = 120

    def update(self, delta, car):
        self.x -= 5*delta
        if self.x < car.x + 1:
            return True
        return False

        

        