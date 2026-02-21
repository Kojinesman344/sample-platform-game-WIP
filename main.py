import pygame
import random
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GRAVITY = 0.6
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)

class PlayerState(Enum):
    IDLE = 1
    RUNNING = 2
    JUMPING = 3
    FALLING = 4

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.state = PlayerState.IDLE
        self.on_ground = False
        self.facing_right = True
        
    def handle_input(self, keys):
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
            
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -PLAYER_JUMP_POWER
            self.on_ground = False
            self.state = PlayerState.JUMPING
    
def update(self, platforms, enemies, collectibles):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Collision with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.state = PlayerState.IDLE if self.vel_x == 0 else PlayerState.RUNNING
                elif self.vel_y < 0:  # Jumping into platform
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        # Check collectibles
        for collectible in collectibles:
            if self.rect.colliderect(collectible.rect):
                collectible.kill()
                global score
                score += 10
        
        # Check enemy collision
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return False  # Game over
        
        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > SCREEN_HEIGHT:
            return False  # Fell off screen
        
        return True  # Still alive
    
def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(surface, BLUE, draw_rect)
        # Draw eyes
        pygame.draw.circle(surface, WHITE, (draw_rect.x + 10, draw_rect.y + 10), 3)
        pygame.draw.circle(surface, WHITE, (draw_rect.x + 22, draw_rect.y + 10), 3)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="normal"):
        super().__init__()
        self.platform_type = platform_type
        self.image = pygame.Surface((width, height))
        
        if platform_type == "normal":
            self.image.fill(GREEN)
        elif platform_type == "spike":
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        if draw_rect.right > 0 and draw_rect.left < SCREEN_WIDTH:
            pygame.draw.rect(surface, GREEN if self.platform_type == "normal" else RED, draw_rect)
            pygame.draw.rect(surface, WHITE, draw_rect, 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = direction
        self.move_range = 100
        self.start_x = x
    
def update(self):
        self.rect.x += self.speed * self.direction
        
        # Change direction at range limit
        if abs(self.rect.x - self.start_x) > self.move_range:
            self.direction *= -1
    
def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        if draw_rect.right > 0 and draw_rect.left < SCREEN_WIDTH:
            pygame.draw.rect(surface, RED, draw_rect)
            # Draw eyes
            eye_offset = 8 if self.direction > 0 else 24
            pygame.draw.circle(surface, WHITE, (draw_rect.x + eye_offset, draw_rect.y + 8), 2)

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bob_offset = 0
        self.bob_speed = 0.1
    
def update(self):
        self.bob_offset += self.bob_speed
        self.rect.y += pygame.math.Vector2(0, 2).y * 0.5 * (0.5 + 0.5 * pygame.math.sin(self.bob_offset))
    def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        if draw_rect.right > 0 and draw_rect.left < SCREEN_WIDTH:
            pygame.draw.rect(surface, YELLOW, draw_rect)
            pygame.draw.circle(surface, WHITE, (draw_rect.centerx, draw_rect.centery), 8, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Side-Scroller Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.camera_x = 0
        
        # Sprite groups
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        
        self.setup_level()
        self.player = Player(50, 300)
    
def setup_level(self):
        """Create the level layout"""
        # Ground platforms
        self.platforms.add(Platform(0, 600, 1280, 50, "normal"))
        
        # Platform sequence
        platforms_data = [
            (300, 520, 150, 20),
            (550, 480, 150, 20),
            (800, 440, 150, 20),
            (1050, 480, 150, 20),
            (1300, 520, 150, 20),
            (1550, 560, 150, 20),
            (1800, 500, 200, 20),
            (2100, 450, 150, 20),
            (2350, 500, 150, 20),
            (2600, 550, 150, 20),
            (2850, 450, 200, 20),
            (3150, 500, 150, 20),
        ]
        
        for x, y, w, h in platforms_data:
            self.platforms.add(Platform(x, y, w, h, "normal"))
        
        # Add enemies
        self.enemies.add(Enemy(400, 470, 2, 1))
        self.enemies.add(Enemy(900, 390, 2, -1))
        self.enemies.add(Enemy(1400, 470, 2, 1))
        self.enemies.add(Enemy(2200, 400, 2, -1))
        self.enemies.add(Enemy(2900, 400, 2, 1))
        
        # Add collectibles
        collectible_positions = [
            (400, 450), (550, 460), (800, 420), (1050, 460),
            (1300, 500), (1800, 480), (2100, 430), (2350, 480),
            (2600, 530), (2850, 430), (3150, 480)
        ]
        
        for x, y in collectible_positions:
            self.collectibles.add(Collectible(x, y))
    
def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over and event.key == pygame.K_SPACE:
                    self.__init__()  # Restart game
    
def update(self):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            
            is_alive = self.player.update(self.platforms, self.enemies, self.collectibles)
            if not is_alive:
                self.game_over = True
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update()
            
            # Update collectibles
            for collectible in self.collectibles:
                collectible.update()
            
            # Update camera to follow player
            self.camera_x = self.player.rect.centerx - SCREEN_WIDTH // 4
            self.camera_x = max(0, self.camera_x)
    
def draw(self):
        self.screen.fill(LIGHT_GRAY)
        
        # Draw background (simple gradient effect)
        for i in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, (180, 220, 255), (0, i), (SCREEN_WIDTH, i), 1)
        
        # Draw game objects
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x)
        
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x)
        
        for collectible in self.collectibles:
            collectible.draw(self.screen, self.camera_x)
        
        self.player.draw(self.screen, self.camera_x)
        
        # Draw HUD
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        distance_text = font.render(f"Distance: {int(self.player.rect.x // 10)}", True, BLACK)
        self.screen.blit(distance_text, (10, 50))
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
def draw_game_over(self):
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        restart_text = font_small.render("Press SPACE to restart or ESC to quit", True, BLACK)
        final_score = font_small.render(f"Final Score: {score}", True, BLACK)
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(final_score, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 + 100))
    
def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

# Global score
score = 0

if __name__ == "__main__":
    game = Game()
    game.run()