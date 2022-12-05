"""
The cube.py file contains the cube class used in the racing test
"""
import pygame

class Cube(pygame.sprite.Sprite):
    "The cube class is used for the delta time racing demo"
    def __init__(self, game, speed, coords):
        self.speed = speed
        self.image = pygame.Surface([50, 50])
        self.image.fill(game.colour['marble'])
        self.coord_x = coords[0]
        self.coord_y = coords[1]

    def update(self, game):
        "Move the cube to the right at the speed provided, multiplied by delta time"
        self.coord_x += self.speed * game.delta_time

    def draw(self, game):
        "Draw the cube to the surface provided"
        game.surface.blit(self.image, [self.coord_x, self.coord_y])
