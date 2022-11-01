# - Import all necessary modules
import pygame
from OpenGL.GL import *
from pygame.locals import *

# - Initialise modules
pygame.init()
pygame.display.init()

# - Create the OpenGL window
window_width = 1280
window_height = 720
pygame.display.set_mode((window_width, window_height), OPENGL | DOUBLEBUF, vsync=1)
pygame.display.set_caption('Stone heart')
info = pygame.display.Info()

# - Game library
game = {
        'running': True, 'FPS': 60,
        'paused': False, 'loop': 'splashscreen',
        'aspect ratio': '16:9', 'clock': 'standard',
        'volume': {
                   'master': 100, 'music': 100,
                   'sound effects': 100, 'voices': 100
                  }
       }

# - Create colour tuples
MIDNIGHT = (  15,   0, 100 )
BUTTER   = ( 255, 245, 100 )

# - Define OpenGL configuration settings
glViewport(0, 0, info.current_w, info.current_h)
glDepthRange(0, 1)
glMatrixMode(GL_PROJECTION)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glShadeModel(GL_SMOOTH)
glClearColor(0.0, 0.0, 0.0, 0.0)
glClearDepth(1.0)
glDisable(GL_DEPTH_TEST)
glDisable(GL_LIGHTING)
glDepthFunc(GL_LEQUAL)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
glEnable(GL_BLEND)

# - Function to convert a PyGame Surface to an OpenGL Texture
# - TODO: Optimise this? Not all these operations might be necessary
texID = glGenTextures(1)
def SurfaceToTexture( pygame_surface ):
    global texID
    rgb_surface = pygame.image.tostring( pygame_surface, 'RGB')
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    surface_rect = pygame_surface.get_rect()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface_rect.width, surface_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE, rgb_surface)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

# - Create the pygame clock object
clock = pygame.time.Clock()

# - Make the 'offscreen_surface' for Pygame blits
offscreen_surface = pygame.Surface((info.current_w / 2, info.current_h / 2))
text_font = pygame.font.Font( None, 30 )

while game['running']:
    for event in pygame.event.get():
        if event.type == QUIT:
            game['running'] = False

    # - Apply all normal pygame functions to the offscreen_surface
    offscreen_surface.fill( MIDNIGHT )
    words = text_font.render( 'FPS: ' + str( clock.get_fps() ), True, BUTTER )
    offscreen_surface.blit( words, (10, 10) )
    pygame.draw.rect( offscreen_surface, BUTTER, [50, 50, 10, 10] )

    # - Prepare to render the texture-mapped rectangle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)

    # - Turn the 'offscreen_surface' into a OpenGL Texture
    SurfaceToTexture( offscreen_surface )
    glBindTexture(GL_TEXTURE_2D, texID)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-1, 1)
    glTexCoord2f(0, 1); glVertex2f(-1, -1)
    glTexCoord2f(1, 1); glVertex2f(1, -1)
    glTexCoord2f(1, 0); glVertex2f(1, 1)
    glEnd()

    # - Update the new surface at the framerate included
    pygame.display.flip()

    if (game['clock'] == 'busy'):
        clock.tick_busy_loop(game['FPS'])
    else:
        clock.tick(game['FPS'])

pygame.quit()