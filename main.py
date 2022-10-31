# - Import all necessary modules
import pygame
from OpenGL.GL import *
from pygame.locals import *
from custard import *

# - Initialise modules
pygame.init()
pygame.display.init()

# - Create the OpenGL window
window_width = 1280
window_height = 720
pygame.display.set_mode((window_width, window_height), OPENGL | DOUBLEBUF, vsync=1)
pygame.display.set_caption('Stone heart')
info = pygame.display.Info()

# - Create colour tuples
MIDNIGHT = (  15,   0, 100 )
BUTTER   = ( 255, 245, 100 )

# - Define OpenGL configuration settings
ConfigureOpenGLSettings(info)
texID = glGenTextures(1)

# - Create the pygame clock object
clock = pygame.time.Clock()

# - Make the 'offscreen_surface' for Pygame blits
offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))
text_font = pygame.font.Font( None, 30 )

# - Game loop
game_running = False
while not game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = True

    # - Apply all normal pygame functions to the offscreen_surface
    offscreen_surface.fill( MIDNIGHT )
    words = text_font.render( 'FPS: ' + str( clock.get_fps() ), True, BUTTER )
    offscreen_surface.blit( words, (10, 10) )
    pygame.draw.rect( offscreen_surface, BUTTER, [50, 50, 10, 10] )

    # - Convert everything to OpenGL textures for blitting
    OpenGLDrawToScreen(offscreen_surface, texID)

    # - Update the new surface at the framerate provided
    pygame.display.flip()
    clock.tick_busy_loop(60)

pygame.quit()