"""
The window test is a game loop for testing development features coming to the custard class
"""
# - Modules necessary for testing operation
import pygame
from assets import Pause, Developer, Cube

# - This loop is used for testing the responsiveness of the game window
def test_environment(game):
    "This game loop stores tests for me to trial frame rate and other features"
    # - Create a variable for time keeping
    game.get_prev_time()
    developer_obj = Developer(game)
    pause_obj = Pause(game, [4, 4])

    line_coords = [game.width - 150, 590], [game.width - 150, 690]

    # - Race variables
    cube_one = Cube(game, 100, [100, 640])
    cube_two = Cube(game, 125, [100, 590])
    racing = False
    timer = 0
    font_size = int(round(game.width / 80, 0))
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    text_1 = font.render('Press [Enter] to start the race', True, game.colour[2])
    text_2 = font.render('!!!', True, game.colour[2])

    while game.loop == 'window test':
        # - Delta time clock
        game.delta_clock()

        # - Events are caught and processed here
        for event in pygame.event.get():
            game.events(event)
            developer_obj.events(event)
            pause_obj.events(event, game)

            if not game.paused and not racing:
                # - Event '768' is 'pygame.KEYDOWN'
                if event.type == 768 and event.key == 13:
                    racing = True



        # - Game logic is processed here
        developer_obj.update(game)
        pause_obj.update(game)

        # - All movement goes in here
        if not game.paused and racing:
            timer += game.delta_time
            if cube_one.coord_x < game.width - 150:
                cube_one.update(game)
                text_2 = font.render('Cube 2: ' + str(round(timer, 2)), True, game.colour[2])
            if cube_two.coord_x < game.width - 150:
                cube_two.update(game)
                text_1 = font.render('Cube 1: ' + str(round(timer, 2)), True, game.colour[2])



        # - Apply all normal pygame functions to the offscreen_surface
        game.surface.fill(game.colour[1])
        game.surface.blit(text_2, [50, game.height / 4 * 3])
        game.surface.blit(text_1, [50, game.height / 4 * 3 - 20])
        cube_one.draw(game)
        cube_two.draw(game)
        pygame.draw.line(game.surface, game.colour[0], line_coords[0], line_coords[1], 2)

        # - Draw the screen
        developer_obj.draw(game.surface)
        pause_obj.draw(game.surface)
        game.draw()
