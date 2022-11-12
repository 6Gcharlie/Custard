# - Import all necessary modules
import pygame
from OpenGL.GL import *
from assets.modules.custard import *
from assets.scripts.window_test import *

# - Initialise modules
pygame.init()
pygame.display.init()



# - Create game object
game = Game()
game.SetGameSurface('Stone Heart')



# - Temporary variables
box_x = 100

circle_x = game.width / 2
circle_y = game.height / 2
circle_loop = 'down'
gravity = 1

movement_speed = 100



# - Main game loop
if (__name__ == '__main__'):
    while game.running:
        match game.loop:
            case 'get clock':
                game.SetFPS(Custard_Set_Clock(game.clock, game.surface, Custard_OpenGL_Blit, game.texID))
                game.SetLoop('window test')
            case 'window test':
                WindowTestEnvironment(game, gravity, movement_speed, circle_y, circle_x, circle_loop, box_x)
    
    pygame.quit()