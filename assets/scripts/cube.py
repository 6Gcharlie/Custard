import pygame

class Cube(pygame.sprite.Sprite):
    def __init__(self, game, speed, coords):
        self.speed = speed
        self.image = pygame.Surface([50, 50])
        self.image.fill(game.marble_colour)
        self.x = coords[0]
        self.y = coords[1]

    def update(self, game):
        self.x += self.speed * game.delta_time

    def draw(self, game):
        game.surface.blit(self.image, [self.x, self.y])