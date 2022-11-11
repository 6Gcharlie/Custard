# - Modules necessary for testing operation
import pygame
import time
from OpenGL.GL import *
from assets.scripts.custard import *
from assets.scripts.develop_module import *

# - This loop is used for testing the responsiveness of the game window
def WindowTestEnvironment(game, gravity, movement_speed, circle_y, circle_x, circle_loop, box_x, offscreen_surface):
    
    # - Create a variable for time keeping
    prev_time = time.time()

    developer_obj = developer_info(game)

    while game['running']:

        dt, prev_time = DeltaTime(prev_time)

        # - Allow the screen to be updated
        if (game['clock type'] == 'busy'):
            game['clock'].tick_busy_loop(game['FPS'])
        else:
            game['clock'].tick(game['FPS'])

        # - Events are caught and processed here
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    game['running'] = False
                case pygame.KEYDOWN:
                    match event.key:
                        case 27:
                            game['running'] = False
                        case _:
                            print('Key pressed: ' + str(event.key))

            developer_obj.events(event)

        developer_obj.update(game['clock'])

        # - Game logic is processed here
        if (gravity >= 26):
            circle_loop = 'up'
            gravity -= movement_speed * dt
        
        if (gravity <= 0):
            circle_loop = 'down'

        if (circle_loop == 'down'):
            circle_y += gravity
            gravity += movement_speed * dt
        else:
            circle_y -= gravity
            gravity -= movement_speed * dt

        box_x += movement_speed * dt



        # - Apply all normal pygame functions to the offscreen_surface
        offscreen_surface.fill(game['colours']['slate'])
        pygame.draw.circle(offscreen_surface, game['colours']['marble'], [circle_x, circle_y], 30)
        pygame.draw.rect(offscreen_surface, game['colours']['marble'], [box_x, 640, 50, 50])

        # - Draw the developer overlay
        developer_obj.draw(offscreen_surface)

        # - Prepare and draw the surface using OpenGL if necessary
        if (game['display']['type'] == 'OpenGL'):
            Custard_OpenGL_Blit(offscreen_surface, game['texID'])
            pygame.display.flip()
        else:
            offscreen_surface = pygame.transform.scale(offscreen_surface, [game['display']['width'], game['display']['height']])
            game['window'].blit(offscreen_surface, [0, 0])
            pygame.display.update()