import pygame as pg
import random
from objects import *

class Theme:
    def __init__(self, theme, road_texture, color_scheme):
        self.road_texture = road_texture
        self.color_scheme = color_scheme
        self.theme = theme


    def spawn_obstacle(self, distance):
        if self.theme == "DESERT":
            return Cactus(distance)
        else:
            return StaticObject(distance)

def load_themes():
    desert_theme = Theme(
        "DESERT",
        road_texture=pg.image.load("assets/road.png").convert(),
        color_scheme=(180, 140, 80),  # Desert color
    )
    
    # Load snowy theme assets
    snowy_theme = Theme(
        "SNOWY",
        road_texture=pg.image.load("assets/road.png").convert(),
        color_scheme=(230, 230, 230)  # Snowy color
    )
    
    # Load normal theme assets
    forest_theme = Theme(
        "FOREST",
        road_texture=pg.image.load("assets/road.png").convert(),
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
    color_scheme = current_theme.color_scheme

    return road_texture, color_scheme