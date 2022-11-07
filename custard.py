# - Required modules for custard.py
import pygame
from OpenGL.GL import *
from pygame.locals import *

def Custard_Set_Clock(clock, offscreen_surface, Custard_OpenGL_Blit, texID):
    setting_clock = True
    tick_list = []
    while setting_clock:

        tick_list.append(clock.get_fps())

        if (len(tick_list) == 50):
            tick_list.sort()
            fps = round(tick_list[25], 0)
            setting_clock = False
        else:
            print(clock.get_fps())
            offscreen_surface.fill([55,  55,  55])
            Custard_OpenGL_Blit(offscreen_surface, texID)
            pygame.display.flip()
            clock.tick()

    return fps


def Custard_OpenGL_Configuration(info):
    # - Configure the OpenGL window
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


# - TODO: Optimise this? Not all these operations might be necessary
def Custard_Surface_To_Texture(pygame_surface, texID):
    # - Function to convert a Pygame Surface to an OpenGL Texture
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



def Custard_OpenGL_Blit(pygame_surface, texID):
    # - Prepare to render the texture-mapped rectangle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)

    # - Turn the 'offscreen_surface' into a OpenGL Texture
    Custard_Surface_To_Texture(pygame_surface, texID)
    glBindTexture(GL_TEXTURE_2D, texID)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-1, 1)
    glTexCoord2f(0, 1); glVertex2f(-1, -1)
    glTexCoord2f(1, 1); glVertex2f(1, -1)
    glTexCoord2f(1, 0); glVertex2f(1, 1)
    glEnd()