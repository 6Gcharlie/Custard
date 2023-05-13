"""
The developer module tracks crutial game stats and presents them visually for debugging purposes
"""
import pygame


class Developer(pygame.sprite.Sprite):
    "The developer class is used to visually display live and static game stats"

    def __init__(self, game):
        # - Developer info settings
        self.visible = False
        self.window_width = game.width
        self.window_height = game.height
        self.text_colour = game.colour[1]
        self.background_colour = game.colour[0]
        font_size = int(round(game.width / 128, 0))
        self.font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        self.image = pygame.Surface([game.width / 4, game.height / 2])
        self.row_height = int(round(game.height / 18, 0))

        # - Time to populated the developer console with valuable statistics
        self.update_all_stats(game)

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
        "Tracks events specific to the Developer class"

        match event.type:
            # - Event '768' is 'pygame.KEYDOWN'
            case 768:
                match event.key:
                    case 96:
                        self.visible = False if self.visible else True

    def update(self, game):
        "Updates live statistics and draws them to the surface"

        # - Update fields
        live_fps = "Live FPS:     " + str(round(game.clock.get_fps(), 1))
        tick_time = "Tick time:    " + str(round(game.clock.get_time(), 4)) + "ms"
        raw_tick = "Raw tick:     " + str(round(game.clock.get_rawtime(), 4)) + "ms"

        self.dynamic_stats[0] = self.font.render(live_fps, True, self.text_colour)
        self.dynamic_stats[1] = self.font.render(tick_time, True, self.text_colour)
        self.dynamic_stats[2] = self.font.render(raw_tick, True, self.text_colour)

        pygame.draw.rect(
            self.image, self.background_colour, [0, self.dynamic_height, 300, 150]
        )
        for stat in self.dynamic_stats:
            self.image.blit(stat, [2, self.row_height])
            self.row_height += int(round(self.window_width / 80, 0))

        self.row_height = self.dynamic_height

    def draw(self, surface):
        "Draw the developer surface to the provided surface"

        if self.visible:
            surface.blit(self.image, [self.window_width / 4 * 3 + 2, 0])

    def update_all_stats(self, game):
        "Refreshes all statistics including static ones"

        # - Rendered information
        self.title = self.font.render("Developer Stats", True, self.text_colour)

        surface = "Surface:      " + game.renderer
        clock = "Clock:        " + game.tick
        vsync = "Vsync:        " + str(game.vsync)
        width = "Width:        " + str(game.width)
        height = "Height:       " + str(game.height)

        self.static_stats = []
        self.static_stats.append(self.font.render(surface, True, self.text_colour))
        self.static_stats.append(self.font.render(clock, True, self.text_colour))
        self.static_stats.append(self.font.render(vsync, True, self.text_colour))
        self.static_stats.append(self.font.render(width, True, self.text_colour))
        self.static_stats.append(self.font.render(height, True, self.text_colour))

        self.dynamic_stats = []
        self.dynamic_stats.append(
            self.font.render("Live FPS:     " + "0", True, self.text_colour)
        )
        self.dynamic_stats.append(
            self.font.render("Tick time:    " + "0", True, self.text_colour)
        )
        self.dynamic_stats.append(
            self.font.render("Raw tick:     " + "0", True, self.text_colour)
        )
