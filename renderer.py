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

def draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, time, color_scheme, offset):
    time_of_day = (time % 240)
    SKY_COLOR = (48, 25, 10)
    #0 - 15
    if time_of_day < 15:
        t = (time_of_day % 15) / 15
        SKY_COLOR = (
            int(15 + t * (255 - 15)),
            int(78 + t * (102 - 78)),
            int(128 + t * (0 - 128))
        )
    #15 - 30
    elif time_of_day < 30:
        t = (time_of_day % 15) / 15
        SKY_COLOR = (
            int(255 + t * (135 - 255)),
            int(102 + t * (206 - 102)),
            int(0 + t * (235 - 0))
        )
    # 30 - 90
    elif time_of_day < 90:
        SKY_COLOR = (135, 206, 235)

    # 90 - 105
    elif time_of_day < 105:
        t = (time_of_day % 15) / 15
        SKY_COLOR = (
            int(135 + t * (255 - 135)),
            int(206 + t * (69 - 206)),
            int(235 + t * (0 - 235))
        )
    #105 - 120
    elif time_of_day < 120:
        t = (time_of_day % 15) / 15
        SKY_COLOR = (
            int(255 + t * (155 - 255)),
            int(69 + t * (14 - 69)),
            int(0 + t * (42 - 0))
        )
    #120 -150
    elif time_of_day < 150:
        t = (time_of_day % 30) / 30
        SKY_COLOR = (
            int(155 + t * (0 - 155)),
            int(14 + t * (31 - 14)),
            int(42 + t * (61 - 42))
        )
    # 150 - 210
    elif time_of_day < 210:
        SKY_COLOR = (0, 31, 61)
    #210 - 240
    else:
        t = (time_of_day % 30) / 30
        SKY_COLOR = (
            int(0 + t * (15 - 0)),
            int(31 + t * (78 - 31)),
            int(61 + t * (128 - 61))
        )
    MOUNTAIN_COLOR = tuple(x - 30 for x in color_scheme)

    screen.fill(SKY_COLOR)

    draw_sun(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day)
    draw_moon(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day)


    # Draw mountains at varying layers based on the offset
    draw_mountain(screen, 0 - offset, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, MOUNTAIN_COLOR)  # Left large mountain
    draw_mountain(screen, SCREEN_WIDTH - SCREEN_WIDTH // 3 - offset, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, MOUNTAIN_COLOR)  # Right large mountain
    
    draw_mountain(screen, SCREEN_WIDTH // 4 - offset, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, MOUNTAIN_COLOR)  # Left middle mountain
    draw_mountain(screen, SCREEN_WIDTH // 1.5 - offset, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, MOUNTAIN_COLOR)  # Right middle mountain
    
    draw_mountain(screen, SCREEN_WIDTH // 3 - offset, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 60, MOUNTAIN_COLOR)  # Mid smaller mountain
    draw_mountain(screen, SCREEN_WIDTH // 1.75 - offset, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 + 60, MOUNTAIN_COLOR)  # Mid smaller mountain (other side)

def draw_sun(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day):
    #sun rise 0-30
    if time_of_day < 30:
        t = (time_of_day % 30) / 30
        sun_pos = int(SCREEN_HEIGHT// 2 + t * (SCREEN_HEIGHT // 4 - SCREEN_HEIGHT//2))
    #daytime 30 - 90
    elif time_of_day < 90:
        sun_pos = SCREEN_HEIGHT // 4
    #sunset 90 - 120
    elif time_of_day < 120:
        t = (time_of_day - 90) / 30
        sun_pos = int(SCREEN_HEIGHT// 4 + t * (SCREEN_HEIGHT // 2 - SCREEN_HEIGHT//4))
    else:
        sun_pos = SCREEN_HEIGHT // 2
    pg.draw.circle(screen, (255, 223, 0), (SCREEN_WIDTH // 2 - offset*1.05, sun_pos), 30)

def draw_moon(screen, SCREEN_WIDTH, SCREEN_HEIGHT, offset, time_of_day):
    if time_of_day < 120:
        moon_pos = SCREEN_HEIGHT // 2
    #moonrise 120-150
    elif time_of_day < 150:
        t = (time_of_day - 120) / 30
        moon_pos = int(SCREEN_HEIGHT// 2 + t * (SCREEN_HEIGHT // 4 - SCREEN_HEIGHT//2))
    #nighttime 150-210
    elif time_of_day < 210:
        moon_pos = SCREEN_HEIGHT//4
    #moonset 210-240
    elif time_of_day < 240:
        t = (time_of_day - 210) / 30
        moon_pos = int(SCREEN_HEIGHT// 4 + t * (SCREEN_HEIGHT // 2 - SCREEN_HEIGHT//4))

    pg.draw.circle(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - offset, moon_pos), 25)
    pg.draw.circle(screen, (200, 200, 200), (SCREEN_WIDTH // 2 + 5 - offset, moon_pos - 5), 20)  # Shadow effect

def draw_mountain(screen, x_offset, width, height, color):
    points = [
        (x_offset, height), 
        (x_offset + width // 2, height - height),  
        (x_offset + width, height) 
    ]
    pg.draw.polygon(screen, color, points)

def render_explosion(screen, path, frame_counter, x, y, scale=1.0, tile_count=16):
    frame = frame_counter % tile_count

    tile_path = f"{path}/tile{frame:03}.png"
    tile = pg.image.load(tile_path).convert_alpha()

    width, height = tile.get_size()
    scaled_tile = pg.transform.scale(tile, (int(width * scale), int(height * scale)))

    screen.blit(scaled_tile, (x - width // 2, y - height // 2))
