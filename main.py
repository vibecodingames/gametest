import pygame
import sys
import os
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platform Game")
clock = pygame.time.Clock()

# Load images
def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Temporary rectangle for the player
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300
        self.velocity_y = 0
        self.jumping = False
        self.on_ground = False

    def update(self, platforms):
        # Gravity
        self.velocity_y += 0.5
        if self.velocity_y > 10:
            self.velocity_y = 10
        
        # Move the player
        self.rect.y += self.velocity_y
        
        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumping = False
                elif self.velocity_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
    def jump(self):
        if self.on_ground and not self.jumping:
            self.jumping = True
            self.velocity_y = -12
            self.on_ground = False

    def move_left(self):
        self.rect.x -= 5
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += 5
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        # Add player to sprites
        self.all_sprites.add(self.player)
        
        # Create platforms
        self.create_platforms()
    
    def create_platforms(self):
        # Ground
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        
        # Platforms
        platform_positions = [
            (100, 400, 100, 20),
            (300, 350, 100, 20),
            (150, 300, 100, 20),
            (400, 250, 100, 20),
            (200, 200, 100, 20)
        ]
        
        for x, y, width, height in platform_positions:
            platform = Platform(x, y, width, height)
            self.all_sprites.add(platform)
            self.platforms.add(platform)
    
    def run(self):
        running = True
        while running:
            # Keep loop running at the right speed
            clock.tick(FPS)
            
            # Process input (events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
            
            # Check keys pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()
            
            # Update
            self.player.update(self.platforms)
            
            # Draw / render
            screen.fill(BLACK)
            self.all_sprites.draw(screen)
            
            # Flip the display
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

# Create and run the game
if __name__ == "__main__":
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
        
    game = Game()
    game.run()