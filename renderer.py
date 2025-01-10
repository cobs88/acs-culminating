import math
import pygame as pg

def render_element(screen, sprite, width, height, scale, x, car, y, z_buffer):
    y = calc_y(x) - y
    z = calc_z(x) - car.z

    vertical = int(60+160*scale + z*scale)
    if vertical >= 1 and vertical < 180 and z_buffer[vertical-1] > 1/scale - 10:
        horizontal = 160-(160-y)*scale + car.angle*(vertical-150)

        scaled_sprite = pg.transform.scale(sprite, (width, height))
        screen.blit(scaled_sprite, (horizontal, vertical - height+1))

def calc_y(x):
    return 200*math.sin(x/17) + 170*math.sin(x/8)

def calc_z(x):
    return 200+80*math.sin(x/13) - 120*math.sin(x/7)