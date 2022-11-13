# - Import all necessary modules
import pygame
from OpenGL.GL import *
from assets.modules.custard import *
from assets.scripts.window_test import *

# - Initialise modules
pygame.init()
pygame.display.init()



# - Create game object
game = Game(1280, 720)
game.SetGameSurface('Stone Heart')



# - Main game loop
if (__name__ == '__main__'):
    while game.running:
        match game.loop:
            case 'get clock':
                game.SetFPS(Custard_Set_Clock(game.clock, game.surface, Custard_OpenGL_Blit, game.texID))
                game.SetLoop('window test')
            case 'window test':
                WindowTestEnvironment(game)
    
    pygame.quit()