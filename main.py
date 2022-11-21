# - Import all necessary modules
import pygame
from OpenGL.GL import *
from assets.modules.custard import *
from assets.scripts.window_test import *

# - Initialise modules
pygame.init()
pygame.display.init()



# - Create game object
game = Application([1280, 720])
game.SetGameSurface('Stone Heart')



# - Main game loop
if (__name__ == '__main__'):
    while game.running:
        match game.loop:
            case 'window test':
                WindowTestEnvironment(game)
            case 'restart':
                game.SetLoop('window test')
                game.SetTick('loose')
                game.SetFPS(60)
    
    pygame.quit()