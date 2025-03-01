import pygame as pg
import math

class Player():
    def __init__(self):
        self.x = 0
        self.y = 500
        self.z = 0
        self.target_angle = 0
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0

        self.sprite_offset = 0

        self.prev_angle = 0
        self.angle_change = 0

        self.width = 80
        self.height = 50

        self.destroyed = False

    def controls(self, delta):
        pressed_keys = pg.key.get_pressed()
        self.acceleration += -0.5*self.acceleration*delta
        self.velocity += -0.5*self.velocity*delta
        
        if pressed_keys[pg.K_w] or pressed_keys[pg.K_UP]:
            if self.velocity > -1:
                self.acceleration += 4*delta
            else:
                self.acceleration = 0
                self.velocity += -self.velocity*delta

        elif pressed_keys[pg.K_s] or pressed_keys[pg.K_DOWN]:
            if self.velocity < 1:
                self.acceleration -= delta
            else:
                self.acceleration = 0
                self.velocity += -self.velocity*delta
        if pressed_keys[pg.K_a] or pressed_keys[pg.K_LEFT]:
            self.target_angle -= delta*self.velocity/30
        elif pressed_keys[pg.K_d] or pressed_keys[pg.K_RIGHT]:
            self.target_angle += delta*self.velocity/30

        self.velocity = max(-10, min(self.velocity, 20))
        self.target_angle = max(-0.8, (min(0.8, self.target_angle)))
        self.velocity += self.acceleration*delta
        self.x += self.velocity*delta*math.cos(self.angle)
        self.y += self.velocity*math.sin(self.angle)*delta*100
        self.y = max(-1000, self.y)
        self.y = min(1000, self.y)
        angle_smoothing_factor = 5
        self.angle += (self.target_angle - self.angle) * delta * angle_smoothing_factor

        self.angle_change = self.angle - self.prev_angle


        target_offset = self.angle_change * 6000
        smoothing_factor = 1.2
        self.sprite_offset += (target_offset - self.sprite_offset) * delta * smoothing_factor

        self.prev_angle = self.angle

    def get_hitbox(self, coordinate):
        hitbox_x = coordinate[0] + 3
        hitbox_y = coordinate[1] + 20
        return pg.Rect(hitbox_x, hitbox_y, self.width, self.height)

