import random
from renderer import render_element
import pygame as pg

class GameObject:
    def __init__(self, distance):
        self.sprite = None
        self.w_scale_factor = 200
        self.h_scale_factor = 200
        self.x = distance
        self.y = None

    def render(self, screen, car, z_buffer):
        scale = max(0.0001, 1 / (self.x - car.x))
        render_element(screen, self.sprite, scale * self.w_scale_factor, scale * self.h_scale_factor, scale, self.x, car, self.y + car.y, z_buffer)

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

        

        