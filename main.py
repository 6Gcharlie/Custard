# - Import all necessary modules
import pygame
import os
from OpenGL.GL import *
from pygame.locals import *
from custard import *

# - Initialise modules
pygame.init()
pygame.display.init()



# - Game library
game = {
        'running': True, 'FPS': 60,
        'paused': False, 'loop': 'splashscreen',
        'clock': 'busy', 'dev console': False,
        'display': {
                    'aspect ratio': '16:9', 'width': 1280,
                    'height': 720, 'type': 'OpenGL',
                    'vsync': True, 'flags': DOUBLEBUF
                   },
        'volume': {
                   'master': 100, 'music': 100,
                   'sound effects': 100, 'voices': 100
                  }
       }



# - Create an SDL/OpenGL window
if (game['display']['type'] == 'OpenGL'):
    pygame.display.set_mode((game['display']['width'], game['display']['height']), OPENGL | game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()
    Custard_OpenGL_Configuration(info)
    texID = glGenTextures(1)
    offscreen_surface = pygame.Surface((info.current_w, info.current_h))
else:
    window = pygame.display.set_mode((game['display']['width'], game['display']['height']), game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()
    offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))

# - Set window caption & create clock
pygame.display.set_caption('Stone heart')
clock = pygame.time.Clock()



# - Basic file path
file_path = 'data/original/'



# - Create colour RGB values
MIDNIGHT = [ 48,  44,  46]
SLATE    = [ 90,  83,  83]
MARBLE   = [125, 113, 122]
BUTTER   = [255, 245, 100]



# - Create basic font class and font object
text_font = pygame.font.Font(os.path.join(file_path + 'fonts/pcsenior.ttf'), 16)

stats = []
stats.append(text_font.render('Developer Stats', True, MARBLE))
stats.append(text_font.render('---------------', True, MARBLE))
stats.append(text_font.render('Surface:      ' + game['display']['type'], True, MARBLE))
stats.append(text_font.render('Clock:        ' + game['clock'], True, MARBLE))
stats.append(text_font.render('Aspect ratio: ' + game['display']['aspect ratio'], True, MARBLE))
stats.append(text_font.render('Vsync :       ' + str(game['display']['vsync']), True, MARBLE))
stats.append(text_font.render('Width:        ' + str(game['display']['width']), True, MARBLE))
stats.append(text_font.render('Height:       ' + str(game['display']['height']), True, MARBLE))

box_x = 100

circle_x = info.current_w / 2
circle_y = info.current_h / 2
circle_loop = 'down'
gravity = 1

# - Main game loop
if (__name__ == '__main__'):

    """ =-=-= Events =-=-= """

    while game['running']:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    game['running'] = False
                case pygame.KEYDOWN:
                    match event.key:
                        case 27:
                            game['running'] = False
                        case 96:
                            if (game['dev console']):
                                game['dev console'] = False
                            else:
                                game['dev console'] = True
                        case _:
                            print(event.key)




        """ =-=-= Logic =-=-= """

        if (gravity == 12):
            circle_loop = 'up'
            gravity -= 1
        
        if (gravity == 0):
            circle_loop = 'down'

        if (circle_loop == 'down'):
            circle_y += gravity
            gravity += 1
        else:
            circle_y -= gravity
            gravity -= 1




        """ =-=-= Draw =-=-= """

        # - Apply all normal pygame functions to the offscreen_surface
        offscreen_surface.fill(SLATE)
        pygame.draw.circle(offscreen_surface, MARBLE, [circle_x, circle_y], 30)

        # - Draw dev console stats if active
        if (game['dev console']):
            pygame.draw.rect(offscreen_surface, MIDNIGHT, [0, 0, info.current_w / 4 + 32, info.current_h])
            stats_fps  = text_font.render('FPS:          ' + str(round(clock.get_fps(), 1)), True, MARBLE)
            stats_time = text_font.render('Last tick:    ' + str(round(clock.get_time(), 4)) + 'ms', True, MARBLE)
            stats_raw  = text_font.render('Raw tick:     ' + str(round(clock.get_rawtime(), 4)) + 'ms', True, MARBLE)

            stat_x = 6
            for stat in stats:
                offscreen_surface.blit(stat, [6, stat_x])
                stat_x += 20
            offscreen_surface.blit(stats_fps, [6, stat_x])
            stat_x += 20
            offscreen_surface.blit(stats_time, [6, stat_x])
            stat_x += 20
            offscreen_surface.blit(stats_raw, [6, stat_x])



        """ =-=-= Refresh =-=-= """

        # - Prepare and draw the surface using OpenGL if necessary
        if (game['display']['type'] == 'OpenGL'):
            Custard_OpenGL_Blit(offscreen_surface, texID)
            pygame.display.flip()
        else:
            offscreen_surface = pygame.transform.scale(offscreen_surface, [game['display']['width'], game['display']['height']])
            window.blit(offscreen_surface, [0, 0])
            pygame.display.update()

        # - Allow the screen to be updated
        if (game['clock'] == 'busy'):
            clock.tick_busy_loop(game['FPS'])
        else:
            clock.tick(game['FPS'])

    pygame.quit()