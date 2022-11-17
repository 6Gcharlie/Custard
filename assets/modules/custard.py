# - Required modules for custard.py
import pygame
import time
import os
from OpenGL.GL import *



# - The Application class is used for general window data/functionality
class Application(pygame.sprite.Sprite):
    # - Initialise the object
    def __init__(self, dimensions):
        # - Define static attribute
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.surface = None

        # - Define general dynamic attribute
        self.fps = 60
        self.loop = 'window test'
        self.tick = 'loose'
        self.path = 'assets/original/'
        self.texID = None

        # - Window related dynamic attribute
        self.vsync = False
        self.aspect_ratio = '16:9'
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.type = 'OpenGL'
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE

        # - Game volume dynamic attribute
        self.master_volume = 100
        self.music_volume = 100
        self.sound_volume = 100
        self.voices_volume = 100

        # - Game colour tuple attribute
        self.midnight_colour = [ 48,  44,  46]
        self.slate_colour    = [ 90,  83,  83]
        self.marble_colour   = [125, 113, 122]
        self.butter_colour   = [255, 245, 100]

        # - Delta time attributes
        self.prev_time = time.time()
        self.now = time.time()
        self.delta_time = self.now - self.prev_time



    def events(self, event):
        match event.type:
            case pygame.QUIT:
                self.SetLoop('NA')
                self.SetRunning(False)
            case pygame.KEYDOWN:
                match event.key:
                    case 27:
                        if (self.paused):
                            self.paused = False
                        else:
                            self.paused = True
                    case 48:
                        self.SetDynamicFPS()
                    case _:
                        print('Key pressed: ' + str(event.key))



    # - Draw screen
    def draw(self):
        if (self.type == 'OpenGL'):
            Custard_OpenGL_Blit(self.surface, self.texID)
            pygame.display.flip()



    # - Method to create a surface
    def SetGameSurface(self, caption):
        if (self.type == 'OpenGL'):
            pygame.display.set_mode([self.width, self.height], pygame.OPENGL | self.flags, self.vsync)
            info = pygame.display.Info()
            Custard_OpenGL_Configuration(info)
            self.texID = glGenTextures(1)
            self.surface = pygame.Surface([self.width, self.height])
            pygame.display.set_caption(caption)



    def SetDynamicFPS(self):
        setting_clock = True
        font = pygame.font.Font(os.path.join(self.path + 'fonts/pcsenior.ttf'), int(round(self.width / 80, 0)))
        tick_list = []
        while setting_clock:
            if (self.clock.get_fps != 0.0):
                tick_list.append(self.clock.get_fps())
                if (len(tick_list) == 200):
                    tick_list.sort()
                    self.fps = int(round(tick_list[25], 0) - 30)
                    setting_clock = False
                else:
                    self.surface.fill([55,  55,  55])
                    text = font.render('Getting Dynamic FPS: ' + str(len(tick_list)), True, self.slate_colour)
                    text_w, text_h = text.get_size()
                    self.surface.blit(text, [self.width / 2 - text_w / 2, self.height / 2 - text_h / 2])
                    Custard_OpenGL_Blit(self.surface, self.texID)
                    pygame.display.flip()
                    self.clock.tick()



    # - Method to update the screen with delta time
    def CustardClock(self):
        # - Do delta time calculations
        self.now = time.time()
        self.delta_time = self.now - self.prev_time
        self.prev_time = self.now

        # - Update with frame rate cap if one is set
        match self.tick:
            case 'busy':
                self.clock.tick_busy_loop(self.fps)
            case 'loose':
                 self.clock.tick(self.fps)



    # - Set the TexID method
    def SetTexID(self, texID):
        self.texID = texID

    # - Set the fps method
    def SetFPS(self, FPS):
        self.fps = FPS

    # - Set the game loop method
    def SetLoop(self, loop):
        self.loop = loop

    # - Set the 'running' attribute, method
    def SetRunning(self, running):
        self.running = running

    # - Set if the game is paused method
    def SetPaused(self, paused):
        self.paused = paused

    # - Set the FPS to a number passed into the method
    def SetFPS(self, FPS):
        self.fps = FPS

    def SetTick(self, tick):
        self.tick = tick

    # - Get the previous delta time
    def GetPrevTime(self):
        self.prev_time = time.time()



# - This function is used to get a dynamic FPS value
def Custard_Set_Clock(clock, offscreen_surface, Custard_OpenGL_Blit, texID):
    setting_clock = True
    tick_list = []
    while setting_clock:

        if (clock.get_fps != 0.0):

            tick_list.append(clock.get_fps())

            if (len(tick_list) == 100):
                tick_list.sort()
                fps = int(round(tick_list[25], 0) - 30)
                setting_clock = False
            else:
                print(clock.get_fps())
                offscreen_surface.fill([55,  55,  55])
                Custard_OpenGL_Blit(offscreen_surface, texID)
                pygame.display.flip()
                clock.tick()

    return fps



# - This function is used to configure a surface for OpenGL
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



# - Convert SDL surface to OpenGL texture
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