import asyncio 
import pygame as pg
import sys, platform, math, random

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

    oncoming_car_sprites = [
        pg.image.load("assets/civic.png").convert_alpha(),
        pg.image.load("assets/soul.png").convert_alpha()
    ]

    for sprite in oncoming_car_sprites:
        sprite.set_colorkey((255, 0, 255))

    
    car = Player()
    cars = [OncomingCar(-50, oncoming_car_sprites), OncomingCar(-17, oncoming_car_sprites), OncomingCar(7, oncoming_car_sprites)]


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
                '''
                ## A desert-like color scheme
                color = (
                    int(180 - draw_distance / 3),
                    int(140 - draw_distance/ 2),
                    int(80+10*math.sin(x))
                )
                '''
                ## A snowy-like color scheme
                color = (
                    int(230 - draw_distance / 3),
                    int(230 - draw_distance / 2),
                    int(230+10*math.sin(x))
                )
                '''
                color = (
                    int(100 - draw_distance / 3),
                    int(180 - draw_distance / 2),
                    int(100 + 10 * math.sin(x))
                )
                '''
                pg.draw.rect(screen, color, (0, vertical, SCREEN_WIDTH, 1))
                render_element(screen, road_slice, 500*scale, 1, scale, x, car, car.y, z_buffer)
        
        for index in reversed(range(len(cars)-1)):
            scale = max(0.0001, 1/(cars[index].x - car.x))
            render_element(screen, cars[index].sprite, 150*scale, 120*scale, scale, cars[index].x, car, -70+car.y, z_buffer)
            cars[index].x -= 10*delta

        if cars[0].x < car.x+1:
            cars.pop(0)
            cars.append(OncomingCar(car.x, oncoming_car_sprites))

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

class OncomingCar():
    def __init__(self, distance, car_sprites):
        self.sprite = random.choice(car_sprites)
        self.x = distance + random.randint(90, 110)

class Player():
    def __init__(self):
        self.x = 0
        self.y = 300
        self.z = 0
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0

        self.sprite_offset = 0

        self.prev_angle = 0
        self.angle_change = 0



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
            self.angle -= delta*self.velocity/30
        elif pressed_keys[pg.K_d] or pressed_keys[pg.K_RIGHT]:
            self.angle += delta*self.velocity/30

        self.velocity = max(-10, min(self.velocity, 20))
        self.angle = max(-0.8, (min(0.8, self.angle)))
        self.velocity += self.acceleration*delta
        self.x += self.velocity*delta*math.cos(self.angle)
        self.y += self.velocity*math.sin(self.angle)*delta*100
        self.y = max(-1000, self.y)
        self.y = min(1000, self.y)

        self.angle_change = self.angle - self.prev_angle


        target_offset = self.angle_change * 5000
        smoothing_factor = 1
        self.sprite_offset += (target_offset - self.sprite_offset) * delta * smoothing_factor

        self.prev_angle = self.angle

if __name__ == "__main__":
    pg.init()
    asyncio.run(main())
    pg.quit()