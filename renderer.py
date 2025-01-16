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
    # Sky transition from day to night
    if time_of_day < 60:  # Daytime to sunset
        SKY_COLOR = (
            int(35 + (time_of_day / 60) * (48 - 35)),
            int(206 + (time_of_day / 60) * (25 - 206)),
            int(235 + (time_of_day / 60) * (52 - 235))
        )
    else:  # Sunset to night
        SKY_COLOR = (
            int(48 + ((time_of_day - 60) / 60) * (0 - 48)),
            int(25 + ((time_of_day - 60) / 60) * (0 - 25)),
            int(52 + ((time_of_day - 60) / 60) * (10 - 52))
        )

    MOUNTAIN_COLOR = tuple(x - 30 for x in color_scheme)

    screen.fill(SKY_COLOR)

    if time_of_day < 60:
        draw_sun(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day)
    else:
        draw_moon(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day)

    draw_mountain(screen, 0 - offset, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, MOUNTAIN_COLOR)  # Left large mountain
    draw_mountain(screen, SCREEN_WIDTH - SCREEN_WIDTH // 3 - offset, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, MOUNTAIN_COLOR)  # Right large mountain
    
    draw_mountain(screen, SCREEN_WIDTH // 4 - offset, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, MOUNTAIN_COLOR)  # Left middle mountain
    draw_mountain(screen, SCREEN_WIDTH // 1.5 - offset, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, MOUNTAIN_COLOR)  # Right middle mountain
    
    draw_mountain(screen, SCREEN_WIDTH // 3 - offset, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 60, MOUNTAIN_COLOR)  # Mid smaller mountain
    draw_mountain(screen, SCREEN_WIDTH // 1.75 - offset, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 60, MOUNTAIN_COLOR)  # Mid smaller mountain (other side)

def draw_sun(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day):
    sun_pos = int(time_of_day / 60 * SCREEN_HEIGHT)  # Sun moves downward during the day
    pg.draw.circle(screen, (255, 223, 0), (SCREEN_WIDTH // 2 - offset*1.05, sun_pos), 30)

def draw_moon(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day):
    moon_pos = int((time_of_day - 60) / 60 * SCREEN_HEIGHT)  # Moon moves downward from the top during the night
    pg.draw.circle(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - offset, moon_pos), 25)
    pg.draw.circle(screen, (200, 200, 200), (SCREEN_WIDTH // 2 + 5 - offset, moon_pos - 5), 20)  # Shadow effect

def draw_mountain(screen, x_offset, width, height, color):
    points = [
        (x_offset, height), 
        (x_offset + width // 2, height - height),  
        (x_offset + width, height) 
    ]
    pg.draw.polygon(screen, color, points)
