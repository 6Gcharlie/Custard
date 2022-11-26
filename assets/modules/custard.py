"""
The custard module is used to manage all game related functions and data.
"""
# - Standard module imports should be placed before new import installs
import os
import time
import pygame
import OpenGL.GL



class Application(pygame.sprite.Sprite):
    "The Application class is used for general window data/functionality"
    # - Initialise the object
    def __init__(self, dimensions):
        # - Define static attribute
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.surface = None

        # - Define dynamic attributes
        self.fps = 60
        self.loop = 'window test'
        self.tick = 'loose'
        self.path = 'assets/original/'
        self.tex_id = None
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
        "The events method is resposible for the event listeners for the application class"
        match event.type:
            case pygame.QUIT:
                self.SetLoop('NA')
                self.SetRunning(False)
            case pygame.KEYDOWN:
                match event.key:
                    case 27:
                        self.paused = False if self.paused else True
                    case 48:
                        self.SetDynamicFPS()
                    case _:
                        print('Key pressed: ' + str(event.key))



    def draw(self):
        "This method draws the application surface to the window"
        if (self.type == 'OpenGL'):
            Custard_OpenGL_Blit(self.surface, self.tex_id)
            pygame.display.flip()



    # - Restart the application
    def restart(self):
        "This method resets all application variables back to default"
        self.paused = False
        self.fps = 60
        self.loop = 'restart'
        self.tick = 'loose'



    # - Exit the application
    def exit(self):
        "This method ends the game and closes the window"
        self.running = False
        self.loop = False



    # - Method to create a surface
    def set_game_surface(self, caption):
        "This method creates the window & window surface for graphics to be drawn onto"
        if (self.type == 'OpenGL'):
            pygame.display.set_mode([self.width, self.height], pygame.OPENGL | self.flags, self.vsync)
            info = pygame.display.Info()
            Custard_OpenGL_Configuration(info)
            self.tex_id = OpenGL.GL.glGenTextures(1)
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
                    Custard_OpenGL_Blit(self.surface, self.tex_id)
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



    # - Set the tex_id method
    def Settex_id(self, tex_id):
        self.tex_id = tex_id

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



# - This function is used to configure a surface for OpenGL
def Custard_OpenGL_Configuration(info):
    # - Configure the OpenGL window
    OpenGL.GL.glViewport(0, 0, info.current_w, info.current_h)
    OpenGL.GL.glDepthRange(0, 1)
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
    OpenGL.GL.glLoadIdentity()
    OpenGL.GL.glShadeModel(OpenGL.GL.GL_SMOOTH)
    OpenGL.GL.glClearColor(0.0, 0.0, 0.0, 0.0)
    OpenGL.GL.glClearDepth(1.0)
    OpenGL.GL.glDisable(OpenGL.GL.GL_DEPTH_TEST)
    OpenGL.GL.glDisable(OpenGL.GL.GL_LIGHTING)
    OpenGL.GL.glDepthFunc(OpenGL.GL.GL_LEQUAL)
    OpenGL.GL.glHint(OpenGL.GL.GL_PERSPECTIVE_CORRECTION_HINT, OpenGL.GL.GL_NICEST)
    OpenGL.GL.glEnable(OpenGL.GL.GL_BLEND)



# - TODO: Optimise this? Not all these operations might be necessary
def Custard_Surface_To_Texture(pygame_surface, tex_id):
    # - Function to convert a Pygame Surface to an OpenGL Texture
    rgb_surface = pygame.image.tostring( pygame_surface, 'RGB')
    OpenGL.GL.glBindTexture(OpenGL.GL.GL_TEXTURE_2D, tex_id)
    OpenGL.GL.glTexParameteri(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_MAG_FILTER, OpenGL.GL.GL_NEAREST)
    OpenGL.GL.glTexParameteri(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_MIN_FILTER, OpenGL.GL.GL_NEAREST)
    OpenGL.GL.glTexParameteri(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_WRAP_S, OpenGL.GL.GL_CLAMP)
    OpenGL.GL.glTexParameteri(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_WRAP_T, OpenGL.GL.GL_CLAMP)
    surface_rect = pygame_surface.get_rect()
    OpenGL.GL.glTexImage2D(OpenGL.GL.GL_TEXTURE_2D, 0, OpenGL.GL.GL_RGB, surface_rect.width, surface_rect.height, 0, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE, rgb_surface)
    OpenGL.GL.glGenerateMipmap(OpenGL.GL.GL_TEXTURE_2D)
    OpenGL.GL.glBindTexture(OpenGL.GL.GL_TEXTURE_2D, 0)



# - Convert SDL surface to OpenGL texture
def Custard_OpenGL_Blit(pygame_surface, tex_id):
    # - Prepare to render the texture-mapped rectangle
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT)
    OpenGL.GL.glLoadIdentity()
    OpenGL.GL.glDisable(OpenGL.GL.GL_LIGHTING)
    OpenGL.GL.glEnable(OpenGL.GL.GL_TEXTURE_2D)

    # - Turn the 'offscreen_surface' into a OpenGL Texture
    Custard_Surface_To_Texture(pygame_surface, tex_id)
    OpenGL.GL.glBindTexture(OpenGL.GL.GL_TEXTURE_2D, tex_id)
    OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)
    OpenGL.GL.glTexCoord2f(0, 0); OpenGL.GL.glVertex2f(-1, 1)
    OpenGL.GL.glTexCoord2f(0, 1); OpenGL.GL.glVertex2f(-1, -1)
    OpenGL.GL.glTexCoord2f(1, 1); OpenGL.GL.glVertex2f(1, -1)
    OpenGL.GL.glTexCoord2f(1, 0); OpenGL.GL.glVertex2f(1, 1)
    OpenGL.GL.glEnd()