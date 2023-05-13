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
        self.walking_speed = speed
        self.running_speed = speed * 2
        self.running = False
        self.stamina = 200
        self.movement = {"left": False, "right": False, "up": False, "down": False}

        # - Inventory attributes
        self.inventory_open = False
        self.inventory_slots = [
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
            "empty",
        ]

        # - Stores the X and Y values of the player
        self.coord_x = coords[0]
        self.coord_y = coords[1]


    def events(self, event):
        "events n suchlike"

        match event.type:
            case 768:
                match event.key:
                    case 1073742049:
                        self.running = True
                    case 97:
                        self.movement["left"] = True
                    case 100:
                        self.movement["right"] = True
                    case 119:
                        self.movement["up"] = True
                    case 115:
                        self.movement["down"] = True
                    case 9:
                        self.toggle_inventory()
            case 769:
                match event.key:
                    case 1073742049:
                        self.running = False
                    case 97:
                        self.movement["left"] = False
                    case 100:
                        self.movement["right"] = False
                    case 119:
                        self.movement["up"] = False
                    case 115:
                        self.movement["down"] = False


    def update(self, game):
        "Placeholder"

        if not self.inventory_open and not self.running:
            if self.movement["left"] and not self.movement["right"]:
                self.coord_x -= self.walking_speed * game.delta_time
            if self.movement["right"] and not self.movement["left"]:
                self.coord_x += self.walking_speed * game.delta_time
            if self.movement["up"] and not self.movement["down"]:
                self.coord_y -= self.walking_speed / 2 * game.delta_time
            if self.movement["down"] and not self.movement["up"]:
                self.coord_y += self.walking_speed / 2 * game.delta_time

        if not self.inventory_open and self.running and self.stamina > 0:
            if self.movement["left"] and not self.movement["right"]:
                self.coord_x -= self.running_speed * game.delta_time
            if self.movement["right"] and not self.movement["left"]:
                self.coord_x += self.running_speed * game.delta_time
            if self.movement["up"] and not self.movement["down"]:
                self.coord_y -= self.running_speed / 2 * game.delta_time
            if self.movement["down"] and not self.movement["up"]:
                self.coord_y += self.running_speed / 2 * game.delta_time

        if not self.running:
            if self.stamina < 200:
                self.stamina += 10 * game.delta_time
        else:
            if self.stamina > 0:
                self.stamina -= 50 * game.delta_time


    def draw(self, game):
        "Draw the cube to the surface provided"
        game.surface.blit(self.image, [self.coord_x, self.coord_y])


    def toggle_inventory(self):
        "placeholder"
        self.inventory_open = False if self.inventory_open else True
        if self.inventory_open:
            pygame.draw.rect(self.image, [155, 0, 0], [0, 0, 20, 20])
        else:
            self.image.fill([200, 0, 0])



class Gui(pygame.sprite.Sprite):
    "Temporary placeholder"

    def __init__(self):
        self.image = pygame.Surface([200, 4])
        self.image.fill([155, 155, 155])
        pygame.draw.rect(self.image, [0, 255, 0], [0, 0, 200, 4])
        self.coord_x = 8
        self.coord_y = 704

    def update(self, player):
        "Test"
        if player.running or player.stamina < 201:
            self.image.fill([155, 155, 155])
            pygame.draw.rect(self.image, [255, 255, 0], [0, 0, player.stamina, 4])

    def draw(self, window):
        "Draw the cube to the surface provided"
        window.surface.blit(self.image, [self.coord_x, self.coord_y])
