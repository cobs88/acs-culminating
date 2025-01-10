import asyncio 
import pygame as pg
import sys, platform, math, random

from player import Player
from themes import load_themes, set_theme

async def main():
    SCREEN_WIDTH = 320
    SCREEN_HEIGHT = 180

    FPS = 60

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SCALED)

    clock = pg.time.Clock()
    clock.tick(FPS)

    road_texture = pg.image.load("assets/road.png").convert()
    car_sprite = pg.image.load("assets/m4.png").convert_alpha()
    
    car_sprite.set_colorkey((255, 0, 255))
    car_sprite = pg.transform.scale(car_sprite, (int(car_sprite.get_size()[0]/3), int(car_sprite.get_size()[1]/3)))

    themes = load_themes()

    current_theme = "DESERT"

    road_texture, oncoming_car_sprites, obstacle_sprites, color_scheme = set_theme(current_theme, themes)

    for sprite in oncoming_car_sprites:
        sprite.set_colorkey((255, 0, 255))

    car = Player()
    cars = [OncomingCar(-50, oncoming_car_sprites), OncomingCar(-17, oncoming_car_sprites), OncomingCar(7, oncoming_car_sprites)]
    obstacles = [Obstacle(-67, obstacle_sprites), Obstacle(-55, obstacle_sprites), Obstacle(-43, obstacle_sprites), Obstacle(-33, obstacle_sprites), Obstacle(-25, obstacle_sprites), Obstacle(-13, obstacle_sprites), Obstacle(-3, obstacle_sprites)]

    running = 1

    while running:
        delta = clock.tick(FPS)/1000
        car.controls(delta)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 0

        screen.fill((100, 150, 200))

        vertical = 180
        x = car.x
        car.z = calc_z(car.x)
        z_buffer = [999 for element in range(180)]
        draw_distance = 1

        while draw_distance < 120:
            last_vertical = vertical
            while vertical >= last_vertical and draw_distance < 120:
                draw_distance += draw_distance/150
                x = car.x + draw_distance
                scale = 1/draw_distance
                z = calc_z(x) - car.z
                vertical = int(60+160*scale + z*scale)

            if draw_distance < 120:
                z_buffer[int(vertical)] = draw_distance
                road_slice = road_texture.subsurface((0, 10*x%225, 225, 1))

                color = (
                    int(color_scheme[0] - draw_distance / 3),
                    int(color_scheme[1] - draw_distance / 2),
                    int(color_scheme[2] + 10*math.sin(x))
                )

                pg.draw.rect(screen, color, (0, vertical, SCREEN_WIDTH, 1))
                render_element(screen, road_slice, 500*scale, 1, scale, x, car, car.y, z_buffer)
        
        for index in reversed(range(len(cars)-1)):
            scale = max(0.0001, 1/(cars[index].x - car.x))
            render_element(screen, cars[index].sprite, 150*scale, 120*scale, scale, cars[index].x, car, -70+car.y, z_buffer)
            cars[index].x -= 10*delta
        
        ## makes new cars spawn once one leaves the screen
        if cars[0].x < car.x+1:
            cars.pop(0)
            cars.append(OncomingCar(car.x, oncoming_car_sprites))

        for index in reversed(range(len(obstacles) - 1)):
            scale = max(0.0001, 1/(obstacles[index].x - car.x))
            render_element(screen, obstacles[index].sprite, 200*scale, 300*scale, scale, obstacles[index].x, car, obstacles[index].y+car.y, z_buffer)

        if obstacles[0].x < car.x+1:
            obstacles.pop(0)
            obstacles.append(Obstacle(obstacles[-1].x, obstacle_sprites))

        screen.blit(car_sprite, (SCREEN_WIDTH/2 - 43.5 - car.sprite_offset, SCREEN_HEIGHT/2))
        pg.display.update()
        await asyncio.sleep(0)

def calc_y(x):
    return 200*math.sin(x/17) + 170*math.sin(x/8)

def calc_z(x):
    return 200+80*math.sin(x/13) - 120*math.sin(x/7)

def render_element(screen, sprite, width, height, scale, x, car, y, z_buffer):
    y = calc_y(x) - y
    z = calc_z(x) - car.z

    vertical = int(60+160*scale + z*scale)
    if vertical >= 1 and vertical < 180 and z_buffer[vertical-1] > 1/scale - 10:
        horizontal = 160-(160-y)*scale + car.angle*(vertical-150)

        scaled_sprite = pg.transform.scale(sprite, (width, height))
        screen.blit(scaled_sprite, (horizontal, vertical - height+1))

class Obstacle():
    def __init__(self, distance, obstacle_sprites):
        self.sprite = random.choice(obstacle_sprites)
        self.x = distance + random.randint(10, 20) + 0.5
        self.y = random.randint(500, 1500) * random.choice([-1, 1])

class OncomingCar():
    def __init__(self, distance, car_sprites):
        self.sprite = random.choice(car_sprites)
        self.x = distance + random.randint(90, 110)

if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()