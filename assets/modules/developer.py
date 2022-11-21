import pygame
import os

class developer_info(pygame.sprite.Sprite):
    def __init__(self, game):
        # - Developer info settings
        self.visible = False
        self.window_width = game.width
        self.window_height = game.height
        self.text_colour = game.slate_colour
        self.background_colour = game.midnight_colour
        self.font = pygame.font.Font(os.path.join(game.path + 'fonts/pcsenior.ttf'), int(round(game.width / 128, 0)))
        self.image = pygame.Surface([game.width / 4, game.height / 2])
        self.row_height = int(round(game.height / 18, 0))

        # - Time to populated the developer console with valuable statistics
        self.UpdateAllStats(game)

        # - Draw details
        self.image.fill(self.background_colour)
        self.image.blit(self.title, [2, 2])

        for stat in self.static_stats:
            self.image.blit(stat, [2, self.row_height])
            self.row_height += int(round(game.width / 80, 0))

        self.row_height += int(round(game.width / 80, 0))
        self.dynamic_height = self.row_height

        for stat in self.dynamic_stats:
            self.image.blit(stat, [2, self.row_height])
            self.row_height += int(round(game.width / 80, 0))

        self.row_height = self.dynamic_height



    def events(self, event):
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case 96:
                        if (self.visible):
                            self.visible = False
                        else:
                            self.visible = True



    def update(self, game):
        # - Update fields
        self.dynamic_stats[0] = self.font.render('Live FPS:     ' + str(round(game.clock.get_fps(), 1)), True, self.text_colour)
        self.dynamic_stats[1] = self.font.render('Tick time:    ' + str(round(game.clock.get_time(), 4)) + 'ms', True, self.text_colour)
        self.dynamic_stats[2] = self.font.render('Raw tick:     ' + str(round(game.clock.get_rawtime(), 4)) + 'ms', True, self.text_colour)

        pygame.draw.rect(self.image, self.background_colour, [0, self.dynamic_height, 300, 150])
        for stat in self.dynamic_stats:
            self.image.blit(stat, [2, self.row_height])
            self.row_height += int(round(self.window_width / 80, 0))

        self.row_height = self.dynamic_height



    def draw(self, surface):
        if (self.visible):
            surface.blit(self.image, [self.window_width / 4 * 3 + 2, 0])



    def UpdateAllStats(self, game):
        # - Rendered information
        self.title = self.font.render('Developer Stats', True, self.text_colour)

        self.static_stats = []
        self.static_stats.append(self.font.render('Surface:      ' + game.type, True, self.text_colour))
        self.static_stats.append(self.font.render('Clock:        ' + game.tick, True, self.text_colour))
        self.static_stats.append(self.font.render('Aspect:       ' + game.aspect_ratio, True, self.text_colour))
        self.static_stats.append(self.font.render('Vsync:        ' + str(game.vsync), True, self.text_colour))
        self.static_stats.append(self.font.render('Width:        ' + str(game.width), True, self.text_colour))
        self.static_stats.append(self.font.render('Height:       ' + str(game.height), True, self.text_colour))

        self.dynamic_stats = []
        self.dynamic_stats.append(self.font.render('Live FPS:     ' + '0', True, self.text_colour))
        self.dynamic_stats.append(self.font.render('Tick time:    ' + '0', True, self.text_colour))
        self.dynamic_stats.append(self.font.render('Raw tick:     ' + '0', True, self.text_colour))
