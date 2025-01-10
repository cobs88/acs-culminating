import pygame as pg
import random

class Theme:
    def __init__(self, road_texture, car_sprites, obstacle_sprites, color_scheme):
        self.road_texture = road_texture
        self.car_sprites = car_sprites
        self.obstacle_sprites = obstacle_sprites
        self.color_scheme = color_scheme

    def get_obstacle(self, obstacle_type=None):
        if obstacle_type:
            pass
        else:
            obstacle_type = self.current_theme.get_random_obstacle()

        sprite = random.choice(self.obstacle_sprites[obstacle_type])

        return Obstacle(sprite, obstacle_type)

def load_themes():
    desert_theme = Theme(
        road_texture=pg.image.load("assets/road.png").convert(),
        car_sprites=[
            pg.image.load("assets/civic.png").convert_alpha(),
            pg.image.load("assets/soul.png").convert_alpha()
        ],
        obstacle_sprites = [
            pg.image.load("assets/cactus.png").convert_alpha(),
        ],
        color_scheme=(180, 140, 80),  # Desert color
    )
    
    # Load snowy theme assets
    snowy_theme = Theme(
        road_texture=pg.image.load("assets/road.png").convert(),
        car_sprites=[
            pg.image.load("assets/civic.png").convert_alpha(),
            pg.image.load("assets/soul.png").convert_alpha()
        ],
        obstacle_sprites = [
            pg.image.load("assets/tree.png").convert_alpha(),
            pg.image.load("assets/tree.png").convert_alpha(),
            pg.image.load("assets/tree.png").convert_alpha(),
            pg.image.load("assets/tree.png").convert_alpha()
        ],
        color_scheme=(230, 230, 230)  # Snowy color
    )
    
    # Load normal theme assets
    forest_theme = Theme(
        road_texture=pg.image.load("assets/road.png").convert(),
        car_sprites=[
            pg.image.load("assets/civic.png").convert_alpha(),
            pg.image.load("assets/soul.png").convert_alpha()
        ],
        obstacle_sprites = [
            pg.image.load("assets/tree.png").convert_alpha(),
            pg.image.load("assets/tree.png").convert_alpha()
        ],
        color_scheme=(100, 180, 100)  # Forest/normal colors
    )

    return {
        "DESERT": desert_theme,
        "SNOWY": snowy_theme,
        "FOREST": forest_theme
    }

def set_theme(theme_name, themes):
    current_theme = themes[theme_name]

    road_texture = current_theme.road_texture
    car_sprites = current_theme.car_sprites
    obstacle_sprites = current_theme.obstacle_sprites
    color_scheme = current_theme.color_scheme

    return road_texture, car_sprites, obstacle_sprites, color_scheme