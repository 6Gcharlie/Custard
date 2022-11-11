# - Import all necessary modules
import pygame
import os
from OpenGL.GL import *
from pygame.locals import *
from assets.scripts.custard import *
from assets.scripts.window_test import *

# - Initialise modules
pygame.init()
pygame.display.init()
clock = pygame.time.Clock()

# - Basic file path
file_path = 'assets/original/'




# - Game dictionary
game = {
        'running': True, 'FPS': 60,
        'paused': False, 'loop': 'window test',
        'clock type': 'busy', 'dev console': False,
        'clock': clock, 'window': 'NA',
        'display': {
                    'aspect ratio': '16:9', 'width': 1280,
                    'height': 720, 'type': 'OpenGL',
                    'vsync': True, 'flags': DOUBLEBUF | HWSURFACE
                   },
        'volume': {
                   'master': 100, 'music': 100,
                   'sound effects': 100, 'voices': 100
                  },
        'colours': {
                    'midnight' : [ 48,  44,  46], 'slate'  : [ 90,  83,  83],
                    'marble'   : [125, 113, 122], 'butter' : [255, 245, 100] 
                   }
       }



# - Create an SDL/OpenGL window
if (game['display']['type'] == 'OpenGL'):

    # - Create a window using OpenGL
    pygame.display.set_mode((game['display']['width'], game['display']['height']), OPENGL | game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()
    Custard_OpenGL_Configuration(info)
    texID = glGenTextures(1)
    offscreen_surface = pygame.Surface((info.current_w, info.current_h))
    window = "NA"

else:

    # - Create a window using SDL
    window = pygame.display.set_mode((game['display']['width'], game['display']['height']), game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()
    offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))

# - Set window caption & create clock
pygame.display.set_caption('Stone heart')




# - Create basic font class and font object
text_font = pygame.font.Font(os.path.join(file_path + 'fonts/pcsenior.ttf'), 16)

stats = []
stats.append(text_font.render('Developer Stats',                                      True, game['colours']['marble']))
stats.append(text_font.render('---------------',                                      True, game['colours']['marble']))
stats.append(text_font.render('Surface:      ' +     game['display']['type'],         True, game['colours']['marble']))
stats.append(text_font.render('Clock:        ' +     game['clock type'],              True, game['colours']['marble']))
stats.append(text_font.render('Aspect ratio: ' +     game['display']['aspect ratio'], True, game['colours']['marble']))
stats.append(text_font.render('Vsync:        ' + str(game['display']['vsync']),       True, game['colours']['marble']))
stats.append(text_font.render('Width:        ' + str(game['display']['width']),       True, game['colours']['marble']))
stats.append(text_font.render('Height:       ' + str(game['display']['height']),      True, game['colours']['marble']))

box_x = 100

circle_x = info.current_w / 2
circle_y = info.current_h / 2
circle_loop = 'down'
gravity = 1

movement_speed = 100

# - Main game loop
if (__name__ == '__main__'):
    while game['running']:
        match game['loop']:
            case 'get clock':
                game['FPS'] = Custard_Set_Clock(clock, offscreen_surface, Custard_OpenGL_Blit, texID)
                stats.append(text_font.render('Set FPS:      ' + str(game['FPS']), True, game['colours']['marble']))
                game['loop'] = 'splashscreen'
            case 'window test':
                WindowTestEnvironment(game, clock, gravity, movement_speed, text_font, circle_y, circle_x, info, window, texID, stats, circle_loop, box_x, offscreen_surface)
    
    pygame.quit()