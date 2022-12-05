"""
The custard module is used to manage all game related functions and data.
"""
# - Standard module imports should be placed before new import installs
import os
import time
import pygame
import OpenGL.GL as gl



class Application(pygame.sprite.Sprite):
    "The Application class is used for general window data/functionality"
    # - Initialise the object
    def __init__(self, attributes):
        # - Define static attribute
        self.running = attributes['running']
        self.paused = attributes['paused']
        self.clock = attributes['clock']
        self.surface = attributes['surface']
        self.fullscreen = attributes['fullscreen']

        # - Define dynamic attributes
        self.fps = attributes['fps']
        self.loop = attributes['loop']
        self.tick = attributes['tick']
        self.path = attributes['path']
        self.tex_id = attributes['tex_id']
        self.vsync = attributes['vsync']
        self.width = attributes['dimensions'][0]
        self.height = attributes['dimensions'][1]
        self.type = attributes['type']

        # - 'DOUBLEBUF' is equal to '1073741824'
        # - 'HWSURFACE' is equal to '1'
        self.flags = attributes['flags']

        # - Game volume dynamic attribute
        self.volume = {
            'master' : attributes['volume']['master'],
            'music'  : attributes['volume']['music'],
            'sound'  : attributes['volume']['sound'],
            'voices' : attributes['volume']['voices']
        }

        # - Game colour tuple attribute
        self.colour = {
            'midnight' : attributes['colour']['midnight'],
            'slate'    : attributes['colour']['slate'],
            'marble'   : attributes['colour']['marble'],
            'butter'   : attributes['colour']['butter']
        }

        # - Delta time attributes
        self.prev_time = time.time()
        self.now = time.time()
        self.delta_time = self.now - self.prev_time



    def events(self, event):
        "The events method is resposible for the event listeners for the application class"
        match event.type:
            # - Event '256' is 'pygame.QUIT'
            case 256:
                self.set_loop('NA')
                self.set_running(False)
            # - Event '768' is 'pygame.KEYDOWN'
            case 768:
                match event.key:
                    case 27:
                        self.paused = False if self.paused else True
                    case 48:
                        self.set_dynamic_fps()
                    case _:
                        print('Key pressed: ' + str(event.key))



    def draw(self):
        "This method draws the application surface to the window"
        if self.type == 'OpenGL':
            custard_opengl_blit(self.surface, self.tex_id)
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
        if self.type == 'OpenGL':
            # - 'pygame.OPENL' is equal to '2' as a flag
            pygame.display.set_mode([self.width, self.height], 2 | self.flags, self.vsync)
            info = pygame.display.Info()
            custard_opengl_configuration(info)
            self.tex_id = gl.glGenTextures(1)
            self.surface = pygame.Surface([self.width, self.height])
            pygame.display.set_caption(caption)



    def set_dynamic_fps(self):
        "Counts to 200 rapidly; Then it will take the mean average speed and set it as an FPS cap"
        setting_clock = True
        dynamic_font_size = int(round(self.width / 80, 0))
        font = pygame.font.Font(os.path.join(self.path + 'fonts/pcsenior.ttf'), dynamic_font_size)
        tick_list = []
        while setting_clock:
            if self.clock.get_fps != 0.0:
                tick_list.append(self.clock.get_fps())
                if len(tick_list) == 200:
                    tick_list.sort()
                    self.fps = int(round(tick_list[25], 0) - 30)
                    setting_clock = False
                else:
                    self.surface.fill([55,  55,  55])
                    tick_length = str(len(tick_list))
                    text = font.render('Get FPS: ' + tick_length + '/200', True, self.slate_colour)
                    text_w, text_h = text.get_size()
                    screen_center = [self.width / 2 - text_w / 2, self.height / 2 - text_h / 2]
                    self.surface.blit(text, screen_center)
                    custard_opengl_blit(self.surface, self.tex_id)
                    pygame.display.flip()
                    self.clock.tick()



    def set_fullscreen(self, fullscreen):
        "Toggles fullscreen for the game"
        if fullscreen:
            self.fullscreen = True
            self.flags = -2147483648 | 1073741824 | 1
        else:
            self.fullscreen = False
            self.flags = 1073741824 | 1

        self.set_game_surface('Stone heart')



    # - Method to update the screen with delta time
    def custard_clock(self):
        "Custard clock uses delta time to update the game window"
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
    def set_tex_id(self, tex_id):
        "Set the 'tex_id' for OpenGL so it can blit correctly"
        self.tex_id = tex_id

    # - Set the game loop method
    def set_loop(self, loop):
        "Pass a string of the desired loop to play into this method"
        self.loop = loop

    # - Set the 'running' attribute, method
    def set_running(self, running):
        "Pass a 'False' boolean into this method to end the game loop"
        self.running = running

    # - Set if the game is paused method
    def set_paused(self, paused):
        "Pass a boolean into this method to pause/unpause the game"
        self.paused = paused

    # - Set the FPS to a number passed into the method
    def set_fps(self, fps):
        "Pass an integer into this method to set it as the desired FPS"
        self.fps = fps

    def set_tick(self, tick):
        "Set the tick type: ('Loose', 'Busy', or 'NA')"
        self.tick = tick

    # - Get the previous delta time
    def get_prev_time(self):
        "Get the current time in delta time"
        self.prev_time = time.time()



# - This function is used to configure a surface for OpenGL
def custard_opengl_configuration(info):
    "Configure the game window for OpenGL operations"
    # - Configure the OpenGL window
    gl.glViewport(0, 0, info.current_w, info.current_h)
    gl.glDepthRange(0, 1)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glClearDepth(1.0)
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LIGHTING)
    gl.glDepthFunc(gl.GL_LEQUAL)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)
    gl.glEnable(gl.GL_BLEND)



# - TODO: Optimise this? Not all these operations might be necessary
def custard_surface_to_texture(pygame_surface, tex_id):
    "Converts an SDL2 surface into an OpenGL texture for faster blits & filter support"
    # - Function to convert a Pygame Surface to an OpenGL Texture
    rgb = pygame.image.tostring( pygame_surface, 'RGB')
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)

    surf = pygame_surface.get_rect()
    unsigned = gl.GL_UNSIGNED_BYTE
    texture = gl.GL_TEXTURE_2D
    gl.glTexImage2D(texture, 0, gl.GL_RGB, surf.width, surf.height, 0, gl.GL_RGB, unsigned, rgb)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)



# - Convert SDL surface to OpenGL texture
def custard_opengl_blit(pygame_surface, tex_id):
    "Draws the OpenGL texture to the screen by texturing it"
    # - Prepare to render the texture-mapped rectangle
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()
    gl.glDisable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_TEXTURE_2D)

    # - Turn the 'offscreen_surface' into a OpenGL Texture
    custard_surface_to_texture(pygame_surface, tex_id)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)
    gl.glBegin(gl.GL_QUADS)
    gl.glTexCoord2f(0, 0)
    gl.glVertex2f(-1, 1)
    gl.glTexCoord2f(0, 1)
    gl.glVertex2f(-1, -1)
    gl.glTexCoord2f(1, 1)
    gl.glVertex2f(1, -1)
    gl.glTexCoord2f(1, 0)
    gl.glVertex2f(1, 1)
    gl.glEnd()
