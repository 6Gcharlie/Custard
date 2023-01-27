"""
This module contains the pause class which provides a basic customisable pause menu
"""
#import os
import pygame

# - Create the pause menu object
class Pause(pygame.sprite.Sprite):
    "The class handles all pause related functionality and blitting"
    def __init__(self, game, coords):
        # - Static pause menu attributes
        # - TODO : rename 'self.flag', 'self.option_selected' & 'self.option_selected'
        self.visible = False
        self.option_selected = 0
        self.flag = False
        self.counter = 0
        self.coords = coords

        # - Dynamic attributes for the pause menu
        # - TODO : add a system to pass in a custom font file provided by the user
        font_size = int(round(game.width / 80, 0))
        self.font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        self.image = pygame.Surface([game.width / 4, game.height / 2])
        self.row_height = int(round(game.height / 18, 0))

        # - Create information to be rendered
        self.title = self.font.render('Game paused', True, game.colour[1])

        # WARNING : resume must always be the FIRST item, and exit must be the LAST
        self.names = []
        self.names.append('Resume')
        self.names.append('Restart')
        self.names.append('15 FPS')
        self.names.append('30 FPS')
        self.names.append('60 FPS')
        self.names.append('No FPS cap')
        self.names.append('Reinstate cap')
        self.names.append('Fullscreen')
        self.names.append('Exit')

        self.exit_num = len(self.names) - 1

        # - Render the information provided above
        self.options = []
        for name in self.names:
            if self.counter == 0:
                self.options.append(self.font.render(' > ' + name, True, game.colour[3]))
            else:
                self.options.append(self.font.render('   ' + name, True, game.colour[1]))
            self.counter += 1

        # - Reset counter to 0
        self.counter = 0

        # - Draw details
        self.image.fill(game.colour[2])
        self.image.blit(self.title, [2, 2])

        for option in self.options:
            self.image.blit(option, [2, self.row_height])
            self.row_height += int(round(game.height / 36, 0))

        self.row_height = int(round(game.height / 18, 0))



    def events(self, event, game):
        "This method listens for and handles events specific to this class"
        match event.type:
            # - Event '768' is 'pygame.KEYDOWN'
            case 768:
                match event.key:
                    case 13:
                        if self.visible:
                            match self.option_selected:
                                case 0:
                                    self.close_menu(game)
                                case 1:
                                    game.reset()
                                case 2:
                                    game.set_fps(15)
                                case 3:
                                    game.set_fps(30)
                                case 4:
                                    game.set_fps(60)
                                case 5:
                                    game.set_tick('NA')
                                case 6:
                                    game.set_tick('loose')
                                case 7:
                                    if game.fullscreen:
                                        game.set_fullscreen(False)
                                    else:
                                        game.set_fullscreen(True)
                                case self.exit_num:
                                    game.exit()
                    case 27:
                        if self.visible:
                            self.close_menu(game)
                        else:
                            self.visible = True
                    case 119:
                        if self.visible:
                            if self.option_selected > 0:
                                self.option_selected -= 1
                            else:
                                self.option_selected = self.exit_num
                            self.flag = True
                    case 115:
                        if self.visible:
                            if self.option_selected < self.exit_num:
                                self.option_selected += 1
                            else:
                                self.option_selected = 0
                            self.flag = True



    def update(self, game):
        "This method updates the surface with new information when change is detected"
        if (self.flag and self.visible):
            self.image.fill(game.colour[2])
            self.image.blit(self.title, [2, 2])

            for option in self.options:
                value = self.names[self.counter]
                if self.counter == self.option_selected:
                    option = self.font.render(' > ' + value, True, game.colour[3])
                else:
                    option = self.font.render('   ' + value, True, game.colour[1])

                self.image.blit(option, [2, self.row_height])
                self.row_height += int(round(game.height / 36, 0))
                self.counter += 1

            self.row_height = int(round(game.height / 18, 0))
            self.counter = 0

            self.flag = False



    def draw(self, surface):
        "This method draws the pause menu onto the surface provided"
        if self.visible:
            surface.blit(self.image, self.coords)

    def close_menu(self, game):
        "This method hides the pause menu setting attributes to keep the change"
        game.paused = False
        self.visible = False
        self.option_selected = 0
        self.flag = True
