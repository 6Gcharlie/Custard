# - Import all necessary modules
import pygame
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
        'aspect ratio': '16:9', 'clock': 'busy',
        'window width': 1280, 'window height': 720,
        'vsync': True, 'display type': 'OpenGL',
        'display flags': DOUBLEBUF, 'dev console': False,
        'volume': {
                   'master': 100, 'music': 100,
                   'sound effects': 100, 'voices': 100
                  }
       }


# - Create an SDL or OpenGL window
if (game['display type'] == 'OpenGL'):
    pygame.display.set_mode((game['window width'], game['window height']), OPENGL | game['display flags'], game['vsync'])
else:
    window = pygame.display.set_mode((game['window width'], game['window height']), game['display flags'], game['vsync'])

pygame.display.set_caption('Stone heart')
info = pygame.display.Info()


# - Create colour tuples
MIDNIGHT = (  15,   0, 100 )
BUTTER   = ( 255, 245, 100 )


# - Define OpenGL configuration settings
if (game['display type'] == 'OpenGL'):
    Custard_OpenGL_Configuration(info)
    texID = glGenTextures(1)


# - Create the pygame clock object
clock = pygame.time.Clock()

# - Make the 'offscreen_surface' for Pygame blits
offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))
text_font = pygame.font.Font( None, 30 )

while game['running']:
    for event in pygame.event.get():
        if event.type == QUIT:
            game['running'] = False


    # - Apply all normal pygame functions to the offscreen_surface
    offscreen_surface.fill(MIDNIGHT)
    words = text_font.render('FPS: ' + str(clock.get_fps()), True, BUTTER)
    offscreen_surface.blit(words, (10, 10) )
    pygame.draw.rect(offscreen_surface, BUTTER, [50, 50, 10, 10])


    # - Prepare and draw the surface using OpenGL if necessary
    if (game['display type'] == 'OpenGL'):
        Custard_OpenGL_Blit(offscreen_surface, texID)
        pygame.display.flip()
    else:
        offscreen_surface = pygame.transform.scale(offscreen_surface, [game['window width'], game['window height']])
        window.blit(offscreen_surface, [0, 0])
        pygame.display.update()


    # - Allow the screen to be updated
    if (game['clock'] == 'busy'):
        clock.tick_busy_loop(game['FPS'])
    else:
        clock.tick(game['FPS'])

pygame.quit()