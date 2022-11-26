# - Import all necessary modules
import pygame
from assets.modules.custard import Application
from assets.loops.window_test import WindowTestEnvironment

# - Initialise modules
pygame.init()
pygame.display.init()



# - Create game object
game = Application([1280, 720])
game.set_game_surface('Stone Heart')



# - Main game loop
if (__name__ == '__main__'):
    while game.running:
        match game.loop:
            case 'window test':
                WindowTestEnvironment(game)
            case 'restart':
                game.SetLoop('window test')
    
    pygame.quit()