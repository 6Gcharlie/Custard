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
MIDNIGHT = [ 48,  44,  46]
SLATE    = [ 90,  83,  83]
MARBLE   = [125, 113, 122]
BUTTER   = [255, 245, 100]



# - Create the pygame clock object
clock = pygame.time.Clock()



# - Create basic font object
text_font = pygame.font.Font(os.path.join('data/fonts/pcsenior.ttf'), 16)
stats_title = text_font.render('Developer Stats', True, MARBLE)
stats_break = text_font.render('---------------', True, MARBLE)

# - Make the 'offscreen_surface' for Pygame blits
if (game['display']['type'] == 'OpenGL'):
    offscreen_surface = pygame.Surface((info.current_w, info.current_h))
else:
    offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))



if (__name__ == '__main__'):

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



        # - Apply all normal pygame functions to the offscreen_surface
        offscreen_surface.fill(SLATE)
        pygame.draw.rect(offscreen_surface, MARBLE, [100, 100, 20, 20])

        if (game['dev console']):
            pygame.draw.rect(offscreen_surface, MIDNIGHT, [0, 0, info.current_w / 4, info.current_h])
            frames_surface = text_font.render('FPS: ' + str(round(clock.get_fps(), 1)), True, MARBLE)
            offscreen_surface.blit(stats_title, (4, 4))
            offscreen_surface.blit(stats_break, (4, 24))
            offscreen_surface.blit(frames_surface, (4, 44))



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