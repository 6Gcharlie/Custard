# - Modules necessary for testing operation
import pygame
from OpenGL.GL import *
from assets.modules.custard import *
from assets.modules.developer import *
from assets.scripts.cube import *
from assets.modules.pause import *

# - This loop is used for testing the responsiveness of the game window
def WindowTestEnvironment(game):
    # - Create a variable for time keeping
    game.GetPrevTime()
    developer_obj = developer_info(game)
    pause_obj = pause_menu(game)

    # - Race variables
    cube_one = Cube(game, 100, [100, 640])
    cube_two = Cube(game, 125, [100, 590])
    racing = False
    timer = 0
    font = pygame.font.Font(os.path.join(game.path + 'fonts/pcsenior.ttf'), int(round(game.width / 80, 0)))
    text_1 = font.render('Press [Enter] to start the race', True, game.marble_colour)
    text_2 = font.render('!!!', True, game.marble_colour)

    while game.loop == 'window test':
        # - Delta time ticker
        game.CustardClock()

        # - Events are caught and processed here
        for event in pygame.event.get():
            game.events(event)
            developer_obj.events(event)
            pause_obj.events(event, game)

            if (not game.paused and not racing):
                if (event.type == pygame.KEYDOWN and event.key == 13):
                    racing = True



        # - Game logic is processed here
        developer_obj.update(game)
        pause_obj.update(game)

        # - All movement goes in here
        if (not game.paused and racing):
            timer += game.delta_time
            if (cube_one.x < game.width - 150):
                cube_one.update(game)
                text_2 = font.render('Cube 2: ' + str(round(timer, 2)), True, game.marble_colour)
            if (cube_two.x < game.width - 150):
                cube_two.update(game)
                text_1 = font.render('Cube 1: ' + str(round(timer, 2)), True, game.marble_colour)



        # - Apply all normal pygame functions to the offscreen_surface
        game.surface.fill(game.slate_colour)
        game.surface.blit(text_2, [50, game.height / 4 * 3])
        game.surface.blit(text_1, [50, game.height / 4 * 3 - 20])
        cube_one.draw(game)
        cube_two.draw(game)
        pygame.draw.line(game.surface, game.midnight_colour, [game.width - 150, 590], [game.width - 150, 690], 2)

        # - Draw the screen
        developer_obj.draw(game.surface)
        pause_obj.draw(game.surface)
        game.draw()