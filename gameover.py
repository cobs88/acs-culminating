import pygame, sys
from pygame.locals import *
from pygame import mixer
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)

# Fonts and Assets
pygame.font.init()
font_title = pygame.font.Font('assets/racing_font.ttf', 100)  # Cool racing font
font_button = pygame.font.Font('assets/racing_font.ttf', 50)  # Adjusted button font size

# Sounds
mixer.init()
click_sound = mixer.Sound('assets/click.wav')
hover_sound = mixer.Sound('assets/hover.wav')
game_over_sound = mixer.Sound('assets/gameoversound.wav')

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Over")

# Load the "bmwcrash.png" background
background_image = pygame.image.load('assets/realbmwcrash.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

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
                hover_sound.play()  # Play hover sound when hovering over the button
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

        # Add glowing effect (blue) when hovered
        if is_hovered:
            pygame.draw.rect(surface, (0, 0, 255), rect, 4, border_radius=20)

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
            click_sound.play()  # Play click sound when button is clicked
            return True
        if not pygame.mouse.get_pressed()[0]:
            self.was_clicked = False
        return False

# Buttons
replay_button = Button(WIDTH // 2 - 200, HEIGHT // 2 - 110, 400, 100, "Replay", GRAY, DARK_GRAY)
quit_button = Button(WIDTH // 2 - 200, HEIGHT // 2 + 90, 400, 100, "Quit", GRAY, DARK_GRAY)

# Main menu loop
running = True
game_over_sound.play()  # Play the game over sound immediately when the game over screen starts

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Fill screen with the new background image
    screen.blit(background_image, (0, 0))

    # Render "Game Over" title
    title_surface = font_title.render("Game Over", True, WHITE)
    title_bg_rect = pygame.Rect(
        (WIDTH // 2 - title_surface.get_width() // 2) - 20,
        160,
        title_surface.get_width() + 40,
        title_surface.get_height() + 40
    )
    pygame.draw.rect(screen, BLACK, title_bg_rect, border_radius=20)
    pygame.draw.rect(screen, WHITE, title_bg_rect, 10, border_radius=20)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 180))

    replay_button.draw(screen)
    quit_button.draw(screen)

    # Check button clicks
    if replay_button.is_clicked():
        pygame.quit()  # Close the current game
        try:
            subprocess.run(["python", "PyGameProject/main.py"])  # Execute main.py in a new process
        except Exception as e:
            print(f"Error launching game: {e}")
        sys.exit()  # Ensure the current script exits

    if quit_button.is_clicked():
        pygame.quit()
        sys.exit()

    # Ensure the screen updates every frame
    pygame.display.update()
