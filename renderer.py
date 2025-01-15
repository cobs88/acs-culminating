import math
import pygame as pg

def render_element(screen, sprite, width, height, scale, x, car, y, z, z_buffer):
    y = calc_y(x) - y
    z = calc_z(x) - (car.z - z)

    vertical = int(60+160*scale + z*scale)
    if vertical >= 1 and vertical < 180 and z_buffer[vertical-1] > 1/scale - 10:
        horizontal = 160-(160-y)*scale + car.angle*(vertical-150)

        scaled_sprite = pg.transform.scale(sprite, (width, height))
        screen.blit(scaled_sprite, (horizontal, vertical - height+1))

def calc_y(x):
    return 200*math.sin(x/17) + 170*math.sin(x/8)

def calc_z(x):
    return 200+80*math.sin(x/13) - 120*math.sin(x/7)

def draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, time_of_day, color_scheme, offset):
    if time_of_day < 60:
        SKY_COLOR = (35, 206, 235)
    else:
        SKY_COLOR = (48, 25, 52)

    MOUNTAIN_COLOR = tuple(x - 30 for x in color_scheme)

    screen.fill(SKY_COLOR)

    if time_of_day < 60:
        draw_sun(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset)
    else:
        draw_moon(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset)
    
    draw_mountain(screen, 0 - offset, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, MOUNTAIN_COLOR)  # Left large mountain
    draw_mountain(screen, SCREEN_WIDTH - SCREEN_WIDTH // 3 - offset, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, MOUNTAIN_COLOR)  # Right large mountain
    
    draw_mountain(screen, SCREEN_WIDTH // 4 - offset, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, MOUNTAIN_COLOR)  # Left middle mountain
    draw_mountain(screen, SCREEN_WIDTH // 1.5 - offset, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, MOUNTAIN_COLOR)  # Right middle mountain
    
    draw_mountain(screen, SCREEN_WIDTH // 3 - offset, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 60, MOUNTAIN_COLOR)  # Mid smaller mountain
    draw_mountain(screen, SCREEN_WIDTH // 1.75 - offset, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 60, MOUNTAIN_COLOR)  # Mid smaller mountain (other side)

def draw_mountain(screen, x_offset, width, height, color):
    points = [
        (x_offset, height), 
        (x_offset + width // 2, height - height),  
        (x_offset + width, height) 
    ]
    pg.draw.polygon(screen, color, points)

def draw_sun(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset):
    pg.draw.circle(screen, (255, 223, 0), (SCREEN_WIDTH // 2 - offset*1.05, SCREEN_HEIGHT // 4), 30)

def draw_moon(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset):
    pg.draw.circle(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - offset, SCREEN_HEIGHT // 4), 25)
    pg.draw.circle(screen, (200, 200, 200), (SCREEN_WIDTH // 2 + 5 - offset, SCREEN_HEIGHT // 4 - 5), 20)  # Shadow effect


    