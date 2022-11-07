# - Import all necessary modules
import pygame
import os
import time
from OpenGL.GL import *
from pygame.locals import *
from custard import *
from loops import *

# - Initialise modules
pygame.init()
pygame.display.init()



# - Game library
game = {
        'running': True, 'FPS': 60,
        'paused': False, 'loop': 'splashscreen',
        'clock': 'not', 'dev console': False,
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
    window = "NA"
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
colours = {
           'midnight' : [ 48,  44,  46], 'slate'  : [ 90,  83,  83],
           'marble'   : [125, 113, 122], 'butter' : [255, 245, 100] 
          }



# - Create a variable for time keeping
prev_time = time.time()



# - Create basic font class and font object
text_font = pygame.font.Font(os.path.join(file_path + 'fonts/pcsenior.ttf'), 16)

stats = []
stats.append(text_font.render('Developer Stats', True, colours['marble']))
stats.append(text_font.render('---------------', True, colours['marble']))
stats.append(text_font.render('Surface:      ' + game['display']['type'], True, colours['marble']))
stats.append(text_font.render('Clock:        ' + game['clock'], True, colours['marble']))
stats.append(text_font.render('Aspect ratio: ' + game['display']['aspect ratio'], True, colours['marble']))
stats.append(text_font.render('Vsync :       ' + str(game['display']['vsync']), True, colours['marble']))
stats.append(text_font.render('Width:        ' + str(game['display']['width']), True, colours['marble']))
stats.append(text_font.render('Height:       ' + str(game['display']['height']), True, colours['marble']))

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
                stats.append(text_font.render('Set FPS:      ' + str(game['FPS']), True, colours['marble']))
                movement_speed = 60 / game['FPS']
                print(movement_speed)
                game['loop'] = 'splashscreen'
            case 'splashscreen':
                GraphicsTestLoop(prev_time, game, clock, gravity, movement_speed, colours, text_font, circle_y, circle_x, info, window, texID, Custard_OpenGL_Blit, stats, circle_loop, box_x, offscreen_surface)
    
    pygame.quit()