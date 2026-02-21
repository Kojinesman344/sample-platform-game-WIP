# Complete code for sample platform game

import pygame
import random

# Load the configuration from config.txt
with open('config.txt', 'r') as f:
    settings = f.read().splitlines()

# Game settings
screen_width = int(settings[0])
screen_height = int(settings[1])

# Initialize pygame
pygame.init()

# Setup the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Load themed backgrounds
backgrounds = {
    'sky': pygame.image.load('assets/sky.png'),
    'forest': pygame.image.load('assets/forest.png'),
    'castle': pygame.image.load('assets/castle.png'),
    'lava': pygame.image.load('assets/lava.png'),
    'ice': pygame.image.load('assets/ice.png')
}

# Load themed foregrounds
foregrounds = {
    'clouds': pygame.image.load('assets/clouds.png'),
    'trees': pygame.image.load('assets/trees.png'),
    'rocks': pygame.image.load('assets/rocks.png')
}

# Parallax scrolling effects
class Background:
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        self.x1 = 0
        self.x2 = self.image.get_width()

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -self.image.get_width():
            self.x1 = self.x2 + self.image.get_width()

        if self.x2 <= -self.image.get_width():
            self.x2 = self.x1 + self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))

# Stage system to switch between different themed levels
class GameStage:
    def __init__(self, name):
        self.name = name
        self.background = backgrounds[name]
        self.foreground = random.choice(list(foregrounds.values()))
        self.bg_layer = Background(self.background, 3)

    def update(self):
        self.bg_layer.update()

    def draw(self, screen):
        self.bg_layer.draw(screen)
        screen.blit(self.foreground, (0, 0))

# Main game loop
running = True
current_stage = GameStage('sky')  # Start with the sky stage

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_stage.update()
    screen.fill((0, 0, 0))  # Clear screen
    current_stage.draw(screen)
    pygame.display.flip()

pygame.quit()