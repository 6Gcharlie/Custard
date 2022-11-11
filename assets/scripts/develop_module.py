import pygame
import os

class developer_info(pygame.sprite.Sprite):
    def __init__(self, game):
        # - Developer info settings
        self.visible = False
        self.text_colour = game['colours']['slate']
        self.background_colour = game['colours']['midnight']
        self.font = pygame.font.Font(os.path.join(game['path'] + 'fonts/pcsenior.ttf'), 12)
        self.image = pygame.Surface([game['display']['width'] / 4, game['display']['height']])
        self.row_height = 40

        # - Rendered information
        self.title = self.font.render('Developer Stats', True, self.text_colour)

        self.static_stats = []
        self.static_stats.append(self.font.render('Surface:      ' + game['display']['type'], True, self.text_colour))
        self.static_stats.append(self.font.render('Clock:        ' + game['clock type'], True, self.text_colour))
        self.static_stats.append(self.font.render('Aspect:       ' + game['display']['aspect ratio'], True, self.text_colour))
        self.static_stats.append(self.font.render('Vsync:        ' + str(game['display']['vsync']), True, self.text_colour))
        self.static_stats.append(self.font.render('Width:        ' + str(game['display']['width']), True, self.text_colour))
        self.static_stats.append(self.font.render('Height:       ' + str(game['display']['height']), True, self.text_colour))

        self.dynamic_stats = []
        self.dynamic_stats.append(self.font.render('FPS:          ' + '0', True, self.text_colour))
        self.dynamic_stats.append(self.font.render('Tick:         ' + '0', True, self.text_colour))
        self.dynamic_stats.append(self.font.render('Raw tick:     ' + '0', True, self.text_colour))

        # - Draw details
        self.image.fill(self.background_colour)
        self.image.blit(self.title, [6, 6])

        for stat in self.static_stats:
            self.image.blit(stat, [6, self.row_height])
            self.row_height += 16

        self.row_height += 16
        self.dynamic_height = self.row_height

        for stat in self.dynamic_stats:
            self.image.blit(stat, [6, self.row_height])
            self.row_height += 16

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



    def update(self, clock):
        # - Update fields
        self.dynamic_stats[0] = self.font.render('FPS:          ' + str(round(clock.get_fps(), 1)), True, self.text_colour)
        self.dynamic_stats[1] = self.font.render('Tick:         ' + str(round(clock.get_time(), 4)) + 'ms', True, self.text_colour)
        self.dynamic_stats[2] = self.font.render('Raw tick:     ' + str(round(clock.get_rawtime(), 4)) + 'ms', True, self.text_colour)

        pygame.draw.rect(self.image, self.background_colour, [0, self.dynamic_height, 300, 150])
        for stat in self.dynamic_stats:
            self.image.blit(stat, [6, self.row_height])
            self.row_height += 16

        self.row_height = self.dynamic_height



    def draw(self, surface):
        if (self.visible):
            surface.blit(self.image, [0, 0])