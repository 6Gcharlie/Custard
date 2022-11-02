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



# - Create an SDL or OpenGL window
if (game['display']['type'] == 'OpenGL'):
    pygame.display.set_mode((game['display']['width'], game['display']['height']), OPENGL | game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()
    Custard_OpenGL_Configuration(info)
    texID = glGenTextures(1)
else:
    window = pygame.display.set_mode((game['display']['width'], game['display']['height']), game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()

# - Set window caption
pygame.display.set_caption('Stone heart')



# - Create colour RGB values
MIDNIGHT = [ 15,   0, 100]
BUTTER   = [255, 245, 100]



# - Create the pygame clock object
clock = pygame.time.Clock()



# - Make the 'offscreen_surface' for Pygame blits
offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))

if (game['display']['type'] == 'OpenGL'):
    text_font = pygame.font.Font(None, 30)
else:
    text_font = pygame.font.Font(None, 60)



if (__name__ == '__main__'):

    while game['running']:
        for event in pygame.event.get():
            if event.type == QUIT:
                game['running'] = False



        # - Apply all normal pygame functions to the offscreen_surface
        offscreen_surface.fill(MIDNIGHT)
        words = text_font.render('FPS: ' + str(clock.get_fps()), True, BUTTER)

        if (game['display']['type'] == 'OpenGL'):
            offscreen_surface.blit(words, (10, 10) )
            pygame.draw.rect(offscreen_surface, BUTTER, [50, 50, 10, 10])
        else:
            offscreen_surface.blit(words, (20, 20) )
            pygame.draw.rect(offscreen_surface, BUTTER, [100, 100, 20, 20])



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