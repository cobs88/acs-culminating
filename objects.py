import random
from renderer import render_element

class GameObject:
    def __init__(self, distance, sprite_list):
        self.sprite = random.choice(sprite_list)
        self.sprite_list = sprite_list
        self.w_scale_factor = 200
        self.h_scale_factor = 200
        self.x = distance
        self.y = None

    def render(self, screen, car, z_buffer):
        scale = max(0.0001, 1 / (self.x - car.x))
        render_element(screen, self.sprite, scale * self.w_scale_factor, scale * self.h_scale_factor, scale, self.x, car, self.y + car.y, z_buffer)

class StaticObject(GameObject):
    def __init__(self, distance, sprite_list):
        super().__init__(distance, sprite_list)
        self.distance = distance
        self.x = self.distance + random.randint(90, 110) + 0.5
        self.y = random.randint(500, 1500) * random.choice([-1, 1])
        self.w_scale_factor = 600
        self.h_scale_factor = 600

    def reset(self, distance, sprite_list):
        self.x = distance + 100
        self.y = random.randint(500, 1500) * random.choice([-1, 1])
        self.sprite = random.choice(sprite_list)
        self.w_scale_factor = 600
        self.h_scale_factor = 600


    def update(self, delta, car):
        if self.x < car.x + 1:
            self.reset(car.x, self.sprite_list)

class OncomingCar(GameObject):
    def __init__(self, distance, sprite_list):
        super().__init__(distance, sprite_list)

        self.x = distance + random.randint(90, 110)
        self.y = -70
        self.w_scale_factor = 150
        self.h_scale_factor = 120

    def reset(self, distance, sprite_list):
        # Randomize position and sprites
        self.x = distance + random.randint(90, 110)
        self.y = -70
        self.sprite = random.choice(sprite_list)
        self.w_scale_factor = 150
        self.h_scale_factor = 120


    def update(self, delta, car):
        self.x -= 10*delta
        if self.x < car.x + 1:
            self.reset(car.x, self.sprite_list)

        

        