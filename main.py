"""
main.py is the executable file for the game being created, run this to run the game
"""
# - Import all necessary modules
import pygame
from assets.modules.custard import Application
from assets.loops.window_test import WindowTestEnvironment

# - Initialise modules
pygame.font.init()
pygame.display.init()



# - Set dynamic attributes for the 'Application' class
application_attributes = {
                            'running': True, 'paused': False,
                            'clock': pygame.time.Clock(), 'surface': None,
                            'fps': 60, 'loop': 'window test', 'tick': 'loose',
                            'path': 'assets/original/', 'tex_id': None,
                            'vsync': False, 'dimensions': [1280, 720],
                            'type': 'OpenGL'
                         }

# - Create game object
game = Application(application_attributes)
game.set_game_surface('Stone Heart')



# - Main game loop
if __name__ == '__main__':
    while game.running:
        match game.loop:
            case 'window test':
                WindowTestEnvironment(game)
            case 'restart':
                game.set_loop('window test')

    pygame.display.quit()
