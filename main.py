"""
main.py is the executable file for the game being created, run this to run the game
"""
import pygame
from assets import Application, test_environment

# - Initialise modules
pygame.font.init()
pygame.display.init()



# - Set dynamic attributes for the 'Application' class
application_attributes = {
                            'running': True, 'paused': False,
                            'clock': pygame.time.Clock(), 'surface': None,
                            'fullscreen': False, 'fps': 60, 'loop': 'window test',
                            'tick': 'loose', 'path': 'assets/original/', 'tex_id': None,
                            'vsync': False, 'dimensions': [1280, 720],
                            'type': 'OpenGL', 'flags': 1073741824 | 1,
                            'volume': {
                                        'master' : 100, 'music'  : 100,
                                        'sound'  : 100, 'voices' : 100
                                      },
                            'colour': {
                                        'midnight' : [ 48,  44,  46], 'slate'  : [ 90,  83,  83],
                                        'marble'   : [125, 113, 122], 'butter' : [255, 245, 100]
                                      }
                         }

# - Create game object
game = Application(application_attributes)
game.set_game_surface('Window test')



# - Main game loop
if __name__ == '__main__':
    while game.running:
        match game.loop:
            case 'window test':
                test_environment(game)
            case 'restart':
                game.set_loop('window test')

    pygame.display.quit()
