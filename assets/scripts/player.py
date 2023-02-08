"""
The cube.py file contains the cube class used in the racing test
"""
import pygame

class Player(pygame.sprite.Sprite):
    "The cube class is used for the delta time racing demo"
    def __init__(self, speed, coords):
        # - Player placeholder
        self.image = pygame.Surface([60, 80])
        self.image.fill([200, 0, 0])

        # - Stores which direction the player is moving in
        self.speed = speed
        self.movement = {
            'left'  : False,
            'right' : False,
            'up'    : False,
            'down'  : False
        }

        # - Inventory attributes
        self.inventory_open = False
        self.inventory_slots = [
            'empty', 'empty', 'empty', 'empty',
            'empty', 'empty', 'empty', 'empty',
            'empty', 'empty', 'empty', 'empty',
            'empty', 'empty', 'empty', 'empty'
        ]

        # - Stores the X and Y values of the player
        self.coord_x = coords[0]
        self.coord_y = coords[1]

    def events(self, event):
        "events n suchlike"
        match event.type:
            case 768:
                match event.key:
                    case 97:
                        self.movement['left'] = True
                    case 100:
                        self.movement['right'] = True
                    case 119:
                        self.movement['up'] = True
                    case 115:
                        self.movement['down'] = True
                    case 9:
                        self.open_inventory()
            case 769:
                match event.key:
                    case 97:
                        self.movement['left'] = False
                    case 100:
                        self.movement['right'] = False
                    case 119:
                        self.movement['up'] = False
                    case 115:
                        self.movement['down'] = False

    def update(self, game):
        "Placeholder"
        if not self.inventory_open:
            if self.movement['left'] and not self.movement['right']:
                self.coord_x -= self.speed * game.delta_time
            if self.movement['right'] and not self.movement['left']:
                self.coord_x += self.speed * game.delta_time
            if self.movement['up'] and not self.movement['down']:
                self.coord_y -= self.speed / 2 * game.delta_time
            if self.movement['down'] and not self.movement['up']:
                self.coord_y += self.speed / 2 * game.delta_time

    def draw(self, game):
        "Draw the cube to the surface provided"
        game.surface.blit(self.image, [self.coord_x, self.coord_y])

    def open_inventory(self):
        "placeholder"
        self.inventory_open = False if self.inventory_open else True
        if self.inventory_open:
            pygame.draw.rect(self.image, [155, 0, 0], [0, 0, 20, 20])
        else:
            self.image.fill([200, 0, 0])
