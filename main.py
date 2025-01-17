import asyncio
import pygame as pg
import sys, platform, math, random
import subprocess  # Import subprocess module
import time

from player import Player
from themes import load_themes, set_theme
from objects import OncomingCar, StaticObject, Helicopter, Target
from renderer import render_element, draw_background, render_explosion

async def main():
    SCREEN_WIDTH = 320
    SCREEN_HEIGHT = 180

    boss_spawned = False

    FPS = 60

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SCALED)

    clock = pg.time.Clock()
    clock.tick(FPS)

    road_texture = pg.image.load("assets/road.png").convert()
    car_sprite = pg.image.load("assets/m4.png").convert_alpha()
    crashed_car_sprite = pg.image.load("assets/crashed_m4.png").convert_alpha()
    font_settings = pg.font.Font('assets/racing_font.ttf', 30)  # For settings menu
    
    car_sprite.set_colorkey((255, 0, 255))
    car_sprite = pg.transform.scale(car_sprite, (int(car_sprite.get_size()[0]/3), int(car_sprite.get_size()[1]/3)))
    crashed_car_sprite = pg.transform.scale(crashed_car_sprite, (int(crashed_car_sprite.get_size()[0]/4), int(crashed_car_sprite.get_size()[1]/4)))

    # Load themes and home icon (Saif 29 - 33)
    themes = load_themes()
    home_icon = pg.image.load("assets/home.png").convert_alpha()
    home_icon = pg.transform.scale(home_icon, (25, 25))  # Resize gear icon
    home_rect = home_icon.get_rect(topleft=(1, 1))  # Position at the top-left corner

    current_theme = "SNOWY"

    road_texture, color_scheme = set_theme(current_theme, themes)

    car = Player()

    explosions = []

    game_objects = []

    game_over = False

    for i in range(3):
        distance = car.x + i * 50 + random.randint(-10, 10)
        game_objects.append(OncomingCar(distance))

    for i in range(20):
        distance = car.x + i * 7 + random.randint(-10, 10)
        obstacle = themes[current_theme].spawn_obstacle(distance)
        game_objects.append(obstacle)

    running = True
    time_of_day = 0  # Track time of day, 0 for sunrise, 60 for sunset

    while running:
        delta = clock.tick(FPS) / 1000
        if not game_over:
            car.controls(delta)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: #Saif 65 - 70
                if home_rect.collidepoint(event.pos):
                    pg.quit()
                    subprocess.run(["python", "PyGameProject/index.py"])
                    sys.exit()
                    running = False

        # Update time of day
        time_of_day += delta * 3

        if boss_spawned == False and time_of_day >= 150:
            game_objects.append(Helicopter(car.x + 20))
            boss_spawned = True


        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, time_of_day, color_scheme, car.angle * 82)

        vertical = 180
        x = car.x
        car.z = calc_z(car.x)
        z_buffer = [999 for _ in range(180)]
        draw_distance = 1

        while draw_distance < 120:
            last_vertical = vertical
            while vertical >= last_vertical and draw_distance < 120:
                draw_distance += draw_distance / 150
                x = car.x + draw_distance
                scale = 1 / draw_distance
                z = calc_z(x) - car.z
                vertical = int(60 + 160 * scale + z * scale)

            if draw_distance < 120:
                z_buffer[int(vertical)] = draw_distance
                road_slice = road_texture.subsurface((0, 10 * x % 225, 225, 1))

                color = (
                    int(color_scheme[0] - draw_distance / 3),
                    int(color_scheme[1] - draw_distance / 2),
                    int(color_scheme[2] + 10 * math.sin(x))
                )

                pg.draw.rect(screen, color, (0, vertical, SCREEN_WIDTH, 1))
                render_element(screen, road_slice, 500*scale, 1, scale, x, car, car.y, 0, z_buffer)
        
        for obj in game_objects:
            if isinstance(obj, Helicopter) and obj.timer >= 5:
                target = Target(car.x + 20, car)
                game_objects.append(target)
                obj.timer = 0
                
        for i in range(len(game_objects) - 1, -1, -1):
            obj = game_objects[i]
            isbehindcar = obj.update(delta, car)
            if isbehindcar == "DESTROY":
                game_objects.pop(i)
            elif isbehindcar:
                new_object = obj.__class__(car.x + 130 + random.randint(-10, 10))
                game_objects.append(new_object)
                game_objects.pop(i)

        game_objects = sorted(game_objects, key=lambda obj: obj.x)

        car_hitbox = car.get_hitbox((SCREEN_WIDTH/2 - 43.5 - car.sprite_offset, SCREEN_HEIGHT/2))
        #pg.draw.rect(screen, (255, 0, 0), car_hitbox, 2)

        for obj in game_objects:
            obj.update(delta, car)

        for obj in reversed(game_objects):
            obj.render(screen, car, z_buffer)

            if not game_over and abs(obj.x - car.x) <= 2:
                hitbox = obj.get_hitbox(car)
                if hitbox is not None:
                    collision = obj.check_collision(car, car_hitbox)
                    if collision:
                        explosions.append({"x": SCREEN_WIDTH//3 + 25, "y": 100, "frame": 0, "timer": 0})
                        print("started explosion")
                        car.destroyed = True
                        game_over = True
                        break

        if not car.destroyed:
            screen.blit(car_sprite, (SCREEN_WIDTH/2 - 43.5 - car.sprite_offset, SCREEN_HEIGHT/2))
        else:
            screen.blit(crashed_car_sprite, (SCREEN_WIDTH/2 - 80 - car.sprite_offset, SCREEN_HEIGHT/2))

        if car.destroyed:
            for explosion in explosions[:]:
                explosion["timer"] += delta
                
                if explosion["timer"] >= 0.1:
                    explosion["timer"] = 0
                    explosion["frame"] += 1
                render_explosion(screen, "assets/explosion", explosion["frame"], explosion["x"], explosion["y"], scale = 2.0)

                if explosion["frame"] >= 16:
                    explosions.remove(explosion)

            print(len(explosions))
            if len(explosions) == 0:
                pg.quit()
                try:
                    subprocess.run(["python", "PyGameProject/gameover.py"])
                except Exception as e:
                    print(f"Error launching game: {e}")
                sys.exit()



        if not car.destroyed:
            for explosion in explosions[:]:
                explosion["timer"] += delta
                
                if explosion["timer"] >= 0.1:
                    explosion["timer"] = 0
                    explosion["frame"] += 1
                render_explosion(screen, "assets/explosion", explosion["frame"], explosion["x"], explosion["y"])

                if explosion["frame"] >= 16:
                    explosions.remove(explosion)


        # Draw gear icon
        screen.blit(home_icon, home_rect.topleft)

        pg.display.update()
        await asyncio.sleep(0)

def calc_y(x):
    return 200 * math.sin(x / 17) + 170 * math.sin(x / 8)

def calc_z(x):
    return 200 + 80 * math.sin(x / 13) - 120 * math.sin(x / 7)

if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()
