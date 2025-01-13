import pygame, sys
from pygame.locals import *
from pygame import mixer

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 165, 0)
DARK_GRAY = (30, 30, 30)
NAVY_BLUE = (0, 0, 128)
DARK_YELLOW = (204, 153, 0)

# Fonts and Assets
pygame.font.init()
font_title = pygame.font.Font('racing_font.ttf', 100)  # Cool racing font
font_button = pygame.font.Font('racing_font.ttf', 50)  # Adjusted button font size
font_loading = pygame.font.Font('racing_font.ttf', 40)  # Cool racing font
font_settings = pygame.font.Font('racing_font.ttf', 30)  # For settings menu

# Sounds
mixer.init()
click_sound = mixer.Sound('click.wav')
hover_sound = mixer.Sound('hover.wav')
background_sound = mixer.Sound('background.wav')
background_sound.set_volume(0.5)  # Set initial volume to 50%

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Prix")

background_image1 = pygame.image.load('racing_bg.png')
background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))
background_image2 = pygame.image.load('racing2_bg.png')
background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))

# Background panning variables
bg_x = 0
bg_y = 0
bg_speed = 0.5  
current_bg = background_image1
next_bg = background_image2
bg_switch_progress = 0  # To track the blending progress

# Button Images Loading
exitImage = pygame.image.load('redx.png').convert_alpha()

# Button setup
class Button:
    def __init__(self, x, y, width, height, text, base_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.text = text
        self.grow = 0  # For smooth animation
        self.was_clicked = False  # To track individual clicks
        self.was_hovered = False  # To track hover state

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # Smooth size increase on hover
        if is_hovered:
            if not self.was_hovered:
                hover_sound.play()
            self.was_hovered = True
            if self.grow < 10:
                self.grow += 4
            surface_color = self.hover_color
        else:
            self.was_hovered = False
            if self.grow > 0:
                self.grow -= 2
            surface_color = self.base_color

        # Draw button with smooth animation
        rect = pygame.Rect(
            self.rect.x - self.grow // 2,
            self.rect.y - self.grow // 2,
            self.rect.width + self.grow,
            self.rect.height + self.grow
        )
        pygame.draw.rect(surface, surface_color, rect, border_radius=20)

        # Add glowing effect
        if is_hovered:
            pygame.draw.rect(surface, BLUE, rect, 4, border_radius=20)

        # Render text
        text_surface = font_button.render(self.text, True, WHITE)
        surface.blit(
            text_surface, 
            (rect.x + (rect.width - text_surface.get_width()) // 2, 
             rect.y + (rect.height - text_surface.get_height()) // 2)
        )

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        clicked = self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]
        if clicked and not self.was_clicked:
            self.was_clicked = True
            click_sound.play()
            return True
        if not pygame.mouse.get_pressed()[0]:
            self.was_clicked = False
        return False

# Slider class
class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.handle_x = x + int((start_val - min_val) / (max_val - min_val) * width)
        self.dragging = False

    def draw(self, surface, color):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, color, (self.rect.x, self.rect.y, self.handle_x - self.rect.x, self.rect.height))
        pygame.draw.circle(surface, WHITE, (self.handle_x, self.rect.y + self.rect.height // 2), 10)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and pygame.Rect(self.handle_x - 10, self.rect.y, 20, self.rect.height).collidepoint(event.pos):
            self.dragging = True
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.value = self.min_val + (self.handle_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

# Buttons
play_button = Button(WIDTH // 2 - 200, HEIGHT // 2 - 150, 400, 100, "Play", GRAY, DARK_GRAY)
settings_button = Button(WIDTH // 2 - 200, HEIGHT // 2 - 30, 400, 100, "Settings", GRAY, DARK_GRAY)
quit_button = Button(WIDTH // 2 - 200, HEIGHT // 2 + 90, 400, 100, "Quit", GRAY, DARK_GRAY)

# Settings Menu
close_button = Button(WIDTH - 200, 20, 50, 50, "", RED, RED)  # Adjusted position and size
volume_slider = Slider(WIDTH // 2 - 150, HEIGHT // 2, 300, 1, 100, 50)
day_night_toggle = Button(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 50, "Day", DARK_YELLOW, DARK_YELLOW)

# Loading bar
loading_width = 500
loading_height = 20
loading_x = (WIDTH - loading_width) // 2
loading_y = HEIGHT // 2 - 100
car_image = pygame.image.load('car.png')
car_image = pygame.transform.scale(car_image, (240, 120))

# Main loop
loading_progress = 0
loading = True
in_settings = False
is_day = True  # Day/Night state
while loading:
    screen.blit(background_image1, (0, 0))
    title_surface = font_title.render("PyGame Pri><", True, WHITE)

    # Draw title background with blue fire border
    title_bg_rect = pygame.Rect(
        (WIDTH // 2 - title_surface.get_width() // 2) - 20,
        160,
        title_surface.get_width() + 40,
        title_surface.get_height() + 40
    )
    pygame.draw.rect(screen, GRAY, title_bg_rect, border_radius=20)
    pygame.draw.rect(screen, BLUE, title_bg_rect, 10, border_radius=20)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 180))

    # Draw loading bar
    pygame.draw.rect(screen, GRAY, (loading_x, loading_y, loading_width, loading_height), border_radius=10)
    pygame.draw.rect(screen, BLUE, (loading_x, loading_y, loading_progress, loading_height), border_radius=10)

    # Draw moving car
    car_x = loading_x + loading_progress - 60
    screen.blit(car_image, (car_x, loading_y - 60))

    # Pulsating loading text
    loading_color = BLUE
    loading_text = font_loading.render(f"Loading... {loading_progress // 6}%", True, loading_color)
    screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, loading_y - 50))

    pygame.display.update()
    pygame.time.delay(50)
    loading_progress += 10
    if loading_progress >= loading_width:
        loading = False

# Play background sound on loop
background_sound.play(loops=-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if in_settings:
            volume_slider.handle_event(event)

    # Play click sound for general clicks
    if pygame.mouse.get_pressed()[0]:
        click_sound.play()

    # Main menu logic
    if not in_settings:
        # Blend between backgrounds
        bg_switch_progress += bg_speed
        if bg_switch_progress >= WIDTH:
            bg_switch_progress = 0
            current_bg, next_bg = next_bg, current_bg

        # Draw the panning background
        screen.blit(current_bg, (-bg_switch_progress, 0))
        screen.blit(next_bg, (WIDTH - bg_switch_progress, 0))

        # Render title and buttons
        title_surface = font_title.render("PyGame Pri><", True, WHITE)
        title_bg_rect = pygame.Rect(
            (WIDTH // 2 - title_surface.get_width() // 2) - 20,
            160,
            title_surface.get_width() + 40,
            title_surface.get_height() + 40
        )
        pygame.draw.rect(screen, GRAY, title_bg_rect, border_radius=20)
        pygame.draw.rect(screen, BLUE, title_bg_rect, 10, border_radius=20)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 180))

        play_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)

        # Check button clicks
        if play_button.is_clicked():
            print("Play game!")  # Replace with game start logic
        if settings_button.is_clicked():
            in_settings = True
        if quit_button.is_clicked():
            pygame.quit()
            sys.exit()

    # Settings menu logic
    else:
        screen.fill(DARK_GRAY if not is_day else GRAY)

        volume_slider.draw(screen, DARK_YELLOW if is_day else BLUE)
        day_night_toggle.draw(screen)
        close_button.draw(screen)

        # Display volume value
        volume_text = font_settings.render(f"Volume: {int(volume_slider.value)}", True, WHITE)
        screen.blit(volume_text, (WIDTH // 2 - volume_text.get_width() // 2, HEIGHT // 2 - 50))

        # Toggle Day/Night Mode
        if day_night_toggle.is_clicked():
            is_day = not is_day
            day_night_toggle.text = "Day" if is_day else "Night"
            day_night_toggle.base_color = DARK_YELLOW if is_day else NAVY_BLUE
            day_night_toggle.hover_color = DARK_YELLOW if is_day else NAVY_BLUE

        if close_button.is_clicked():
            in_settings = False

        # Adjust volume
        background_sound.set_volume(volume_slider.value / 100)

    pygame.display.update()
