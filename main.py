"""
main.py is the executable for the game, run this to play the game!
"""
# - Module imports for the game
import pygame
from assets import Application, test_environment, backrooms

# - Initialise modules
pygame.font.init()
pygame.display.init()

# - Renderer and flags to boost speed with each
RENDER = 'SDL 2'
SDL_FLAGS = 512
OPENGL_FLAGS = 1073741824 | 1

# - Set attributes for the 'Application' class
application_attributes = {
    'running':       True,
    'paused':        False,
    'clock':         pygame.time.Clock(),
    'fullscreen':    False,
    'fps':           60,
    'loop':          'backrooms',
    'tick':          'NA',
    'path':          'assets/original/',
    'tex_id':        None,
    'vsync':         False,
    'dimensions':    [1280, 720],
    'renderer':      RENDER,
    'flags':         OPENGL_FLAGS if RENDER == 'OpenGL' else SDL_FLAGS,
}

# - Create game object
game = Application(application_attributes, False, False)
game.set_game_surface('Window test')

# - Main application loop
if __name__ == '__main__':
    while game.running:
        match game.loop:
            case 'backrooms':
                backrooms(game)
            case 'window test':
                test_environment(game)
            case 'restart':
                game.set_loop('window test')

    pygame.display.quit()
