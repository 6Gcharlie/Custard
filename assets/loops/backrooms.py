"""
Temporary placeholder will eventually encompass:
 - Backrooms,
 - Stone heart,
 - Horror game,
 - Mystery flesh pit,
 - Pong.
"""
import pygame
from assets import Pause, Developer, Player, Gui

def backrooms(game):
    "Temporary placeholder"
    # - Create a variable for time keeping
    game.get_prev_time()

    # - Create objects for pause & developer menu
    developer_obj = Developer(game)
    pause_obj = Pause(game, [4, 4])

    pygame.display.set_caption("The backrooms")

    player = Player(100, [game.width / 2 - 30, game.height / 2 - 30])
    gui    = Gui()

    while game.loop == 'backrooms':
        # - Delta time clock
        game.delta_clock()

        # - Events are caught and processed here
        for event in pygame.event.get():
            if not pause_obj.visible:
                player.events(event)

            game.events(event)
            developer_obj.events(event)
            pause_obj.events(event, game)

        # - Game logic is processed here
        if not pause_obj.visible:
            player.update(game)
            gui.update(player)

        developer_obj.update(game)
        pause_obj.update(game)

        # - Apply all normal pygame functions to the offscreen_surface
        game.surface.fill(game.colour[1])
        player.draw(game)
        gui.draw(game)

        # - Draw the screen
        developer_obj.draw(game.surface)
        pause_obj.draw(game.surface)
        game.draw()
