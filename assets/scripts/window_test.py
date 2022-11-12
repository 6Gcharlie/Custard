# - Modules necessary for testing operation
import pygame
import time
from OpenGL.GL import *
from assets.modules.custard import *
from assets.scripts.develop_module import *

# - This loop is used for testing the responsiveness of the game window
def WindowTestEnvironment(game, gravity, movement_speed, circle_y, circle_x, circle_loop, box_x):
    
    # - Create a variable for time keeping
    game.GetPrevTime()
    developer_obj = developer_info(game)

    while game.loop == 'window test':
        # - Delta time ticker
        game.DeltaClock()



        # - Events are caught and processed here
        for event in pygame.event.get():
            game.events(event)
            developer_obj.events(event)



        # - Game logic is processed here
        developer_obj.update(game.clock)

        if (game.paused == False):
            if (gravity >= 26):
                circle_loop = 'up'
                gravity -= movement_speed * game.delta_time
            
            if (gravity <= 0):
                circle_loop = 'down'

            if (circle_loop == 'down'):
                circle_y += gravity
                gravity += movement_speed * game.delta_time
            else:
                circle_y -= gravity
                gravity -= movement_speed * game.delta_time

            box_x += movement_speed * game.delta_time



        # - Apply all normal pygame functions to the offscreen_surface
        game.surface.fill(game.slate_colour)
        pygame.draw.circle(game.surface, game.marble_colour, [circle_x, circle_y], 30)
        pygame.draw.rect(game.surface, game.marble_colour, [box_x, 640, 50, 50])

        # - Draw the screen
        developer_obj.draw(game.surface)
        game.draw()