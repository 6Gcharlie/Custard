import pygame
import os

# - Create the pause menu object
class pause_menu(pygame.sprite.Sprite):
    def __init__(self, game):
        # - Statis pause menu attributes
        self.visible = False
        self.menu = 'main'
        self.option_selected = 0
        self.flag = False
        self.counter = 0

        # - Dynamic attributes for the pause menu
        self.font = pygame.font.Font(os.path.join(game.path + 'fonts/pcsenior.ttf'), int(round(game.width / 80, 0)))
        self.image = pygame.Surface([game.width / 4, game.height / 2])
        self.row_height = int(round(game.height / 18, 0))

        # - Create information to be rendered
        self.title = self.font.render('Game paused', True, game.slate_colour)
        
        # WARNING : resume must always be the FIRST item, and exit must be the LAST
        self.names = []
        self.names.append('Resume')
        self.names.append('Restart')
        self.names.append('30 FPS')
        self.names.append('60 FPS')
        self.names.append('Dynamic FPS')
        self.names.append('No FPS cap')
        self.names.append('Reinstate cap')
        self.names.append('Exit')
        
        self.exit_num = len(self.names) - 1

        # - Render the information provided above
        self.options = []
        for name in self.names:
            if (self.counter == 0):
                self.options.append(self.font.render(' > ' + name, True, game.butter_colour))
            else:
                self.options.append(self.font.render('   ' + name, True, game.slate_colour))
            self.counter += 1

        # - Reset counter to 0
        self.counter = 0

        # - Draw details
        self.image.fill(game.marble_colour)
        self.image.blit(self.title, [2, 2])

        for option in self.options:
            self.image.blit(option, [2, self.row_height])
            self.row_height += int(round(game.height / 36, 0))

        self.row_height = int(round(game.height / 18, 0))

    

    def events(self, event, game):
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case 13:
                        if (self.visible):
                            match self.option_selected:
                                case self.exit_num:
                                    game.SetLoop('NA')
                                    game.SetRunning(False)
                                case 0:
                                    self.ClosePauseMenu()
                                case 1:
                                    game.SetLoop('restart')
                                    game.SetPaused(False)
                                case 2:
                                    game.SetFPS(30)
                                case 3:
                                    game.SetFPS(60)
                                case 4:
                                    game.SetDynamicFPS()
                                case 5:
                                    game.SetTick('NA')
                                case 6:
                                    game.SetTick('loose')
                    case 27:
                        if (self.visible):
                            self.ClosePauseMenu()
                        else:
                            self.visible = True
                    case 119:
                        if (self.visible and self.option_selected > 0): 
                            self.option_selected -= 1
                            self.flag = True
                    case 115:
                        if (self.visible and self.option_selected < self.exit_num):
                            self.option_selected += 1
                            self.flag = True
    


    def update(self, game):
        if (self.flag and self.visible):
            self.image.fill(game.marble_colour)
            self.image.blit(self.title, [2, 2])

            for option in self.options:
                if (self.counter == self.option_selected):
                    option = self.font.render(' > ' + self.names[self.counter], True, game.butter_colour)
                else:
                    option = self.font.render('   ' + self.names[self.counter], True, game.slate_colour)

                self.image.blit(option, [2, self.row_height])
                self.row_height += int(round(game.height / 36, 0))
                self.counter += 1

            self.row_height = int(round(game.height / 18, 0))
            self.counter = 0

            self.flag = False



    def draw(self, surface):
        if (self.visible):
            surface.blit(self.image, [0, 0])

    def ClosePauseMenu(self):
        self.visible = False
        self.option_selected = 0
        self.menu = 'main'
        self.flag = True