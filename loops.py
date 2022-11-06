import pygame
from OpenGL.GL import *

def GraphicsTestLoop(game, clock, gravity, movement_speed, colours, text_font, circle_y, circle_x, info, window, texID, Custard_OpenGL_Blit, stats, circle_loop, box_x, offscreen_surface):
    
    """ =-=-= Events =-=-= """

    while game['running']:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    game['running'] = False
                case pygame.KEYDOWN:
                    match event.key:
                        case 27:
                            game['running'] = False
                        case 96:
                            if (game['dev console']):
                                game['dev console'] = False
                            else:
                                game['dev console'] = True
                        case _:
                            print(event.key)




        """ =-=-= Logic =-=-= """

        if (gravity >= 26):
            circle_loop = 'up'
            gravity -= movement_speed
        
        if (gravity <= 0):
            circle_loop = 'down'

        if (circle_loop == 'down'):
            circle_y += gravity
            gravity += movement_speed
        else:
            circle_y -= gravity
            gravity -= movement_speed

        box_x += movement_speed




        """ =-=-= Draw =-=-= """

        # - Apply all normal pygame functions to the offscreen_surface
        offscreen_surface.fill(colours['slate'])
        pygame.draw.circle(offscreen_surface, colours['marble'], [circle_x, circle_y], 30)
        pygame.draw.rect(offscreen_surface, colours['marble'], [box_x, 640, 50, 50])

        # - Draw dev console stats if active
        if (game['dev console']):
            pygame.draw.rect(offscreen_surface, colours['midnight'], [0, 0, info.current_w / 4 + 32, info.current_h])
            stats_fps  = text_font.render('FPS:          ' + str(round(clock.get_fps(), 1)), True, colours['marble'])
            stats_time = text_font.render('Last tick:    ' + str(round(clock.get_time(), 4)) + 'ms', True, colours['marble'])
            stats_raw  = text_font.render('Raw tick:     ' + str(round(clock.get_rawtime(), 4)) + 'ms', True, colours['marble'])

            stat_x = 6
            for stat in stats:
                offscreen_surface.blit(stat, [6, stat_x])
                stat_x += 20
            offscreen_surface.blit(stats_fps, [6, stat_x])
            stat_x += 20
            offscreen_surface.blit(stats_time, [6, stat_x])
            stat_x += 20
            offscreen_surface.blit(stats_raw, [6, stat_x])



        """ =-=-= Refresh =-=-= """

        # - Prepare and draw the surface using OpenGL if necessary
        if (game['display']['type'] == 'OpenGL'):
            Custard_OpenGL_Blit(offscreen_surface, texID)
            pygame.display.flip()
        else:
            offscreen_surface = pygame.transform.scale(offscreen_surface, [game['display']['width'], game['display']['height']])
            window.blit(offscreen_surface, [0, 0])
            pygame.display.update()

        # - Allow the screen to be updated
        if (game['clock'] == 'busy'):
            clock.tick_busy_loop(game['FPS'])
        else:
            clock.tick(game['FPS'])

