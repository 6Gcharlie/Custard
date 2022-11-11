# - Import all necessary modules
import pygame
import os
from OpenGL.GL import *
from assets.scripts.custard import *
from assets.scripts.window_test import *

# - Initialise modules
pygame.init()
pygame.display.init()
clock = pygame.time.Clock()




# - Game dictionary
game = {
        'running': True, 'FPS': 60,
        'paused': False, 'loop': 'get clock',
        'clock type': 'busy', 'dev console': False,
        'clock': clock, 'window': None,
        'path': 'assets/original/', 'texID': None,
        'display': {
                    'aspect ratio': '16:9', 'width': 1280,
                    'height': 720, 'type': 'OpenGL',
                    'vsync': True, 'flags': pygame.DOUBLEBUF | pygame.HWSURFACE
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
    pygame.display.set_mode((game['display']['width'], game['display']['height']), pygame.OPENGL | game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()
    Custard_OpenGL_Configuration(info)
    game['texID'] = glGenTextures(1)
    offscreen_surface = pygame.Surface((info.current_w, info.current_h))
    window = "NA"
else:
    # - Create a window using SDL
    window = pygame.display.set_mode((game['display']['width'], game['display']['height']), game['display']['flags'], game['display']['vsync'])
    info = pygame.display.Info()
    offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))

# - Set window caption & create clock
pygame.display.set_caption('Stone heart')




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
                game['FPS'] = Custard_Set_Clock(clock, offscreen_surface, Custard_OpenGL_Blit, game['texID'])
                game['loop'] = 'window test'
            case 'window test':
                WindowTestEnvironment(game, gravity, movement_speed, circle_y, circle_x, circle_loop, box_x, offscreen_surface)
    
    pygame.quit()