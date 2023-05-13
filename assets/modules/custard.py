"""
The custard module is used to manage all game related functions and data.
"""
# - Standard module imports should be placed before new import installs
import time
import pygame
import OpenGL.GL as gl



class Window(pygame.sprite.Sprite):
    "The Window class contains window generation data and functionality"
    def __init__(self, attributes, volumes, colours):
        # - Default attributes
        self.default = attributes

        # - Create window attribute in case of SDL 2 renderer
        self.surface = None

        # - Define attributes that rarely change
        self.running    = self.default['running']
        self.paused     = self.default['paused']
        self.clock      = self.default['clock']
        self.fullscreen = self.default['fullscreen']

        # - Define attributes the user has more influence over
        self.fps        = self.default['fps']
        self.loop       = self.default['loop']
        self.tick       = self.default['tick']
        self.path       = self.default['path']
        self.tex_id     = self.default['tex_id']
        self.vsync      = self.default['vsync']
        self.width      = self.default['dimensions'][0]
        self.height     = self.default['dimensions'][1]
        self.renderer   = self.default['renderer']

        # - 'DOUBLEBUF' flag is equal to '1073741824'
        # - 'HWSURFACE' flag is equal to '1'
        # - 'RESIZE'    flag is equal to '512'
        self.flags = self.default['flags']

        # - Game volume attributes if any are set
        if volumes:
            self.volume = {
                'master' : volumes['master'],
                'music'  : volumes['music'],
                'sound'  : volumes['sound'],
                'voices' : volumes['voices']
            }
        else:
            self.volume = {
                'master' : 100,
                'music'  : 100,
                'sound'  : 100,
                'voices' : 100
            }

        # - Game colour attribute if any are set
        if colours:
            self.colour = [
                colours[0], colours[1],
                colours[2], colours[3]
            ]
        else:
            self.colour = [
                [ 48,  44,  46], [ 90,  83,  83],
                [125, 113, 122], [255, 245, 100]
            ]

        # - Delta time attributes
        self.prev_time  = time.time()
        self.now = time.time()
        self.delta_time = self.now - self.prev_time



    def events(self, event):
        "The events method contains event listeners for the Window class"
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
                    case 1073741892:
                        if self.fullscreen:
                            self.set_fullscreen(False)
                        else:
                            self.set_fullscreen(True)
                    case _:
                        print('Key pressed: ' + str(event.key))



    def draw(self):
        "This method draws the Window surface to the window"
        if self.renderer == 'OpenGL':
            custard_opengl_blit(self.surface, self.tex_id)
            pygame.display.flip()
        else:
            pygame.display.update()



    # - Restart the Window
    def reset(self):
        "Set default attributes"
        # - Define static attribute
        self.running    = self.default['running']
        self.paused     = self.default['paused']
        self.clock      = self.default['clock']
        self.fullscreen = self.default['fullscreen']

        # - Define dynamic attributes
        self.fps        = self.default['fps']
        self.loop       = self.default['loop']
        self.tick       = self.default['tick']
        self.path       = self.default['path']
        self.vsync      = self.default['vsync']
        self.width      = self.default['dimensions'][0]
        self.height     = self.default['dimensions'][1]
        self.renderer   = self.default['renderer']

        # - 'DOUBLEBUF' is equal to '1073741824'
        # - 'HWSURFACE' is equal to '1'
        # - 'RESIZE'    flag is equal to '512'
        self.flags = self.default['flags']

        # - Restart the loop
        self.loop = "restart"



    # - Exit the Window
    def exit(self):
        "This method ends the game and closes the window"
        self.running = False
        self.loop = False



    # - Method to create a surface
    def set_game_surface(self, caption):
        "This method creates the window & window surface for graphics to be drawn onto"
        if self.renderer == 'OpenGL':
            # - 'pygame.OPENL' is equal to '2' as a flag
            pygame.display.set_mode([self.width, self.height], 2 | self.flags, self.vsync)
            info = pygame.display.Info()
            custard_opengl_configuration(info)
            self.tex_id = gl.glGenTextures(1)
            self.surface = pygame.Surface([self.width, self.height])
            pygame.display.set_caption(caption)
        else:
            surface = pygame.display.set_mode([self.width, self.height], self.flags, self.vsync)
            self.surface = surface
            pygame.display.set_caption(caption)



    def set_fullscreen(self, fullscreen):
        "Toggles fullscreen for the game"
        if fullscreen:
            self.fullscreen = True
            self.flags = -2147483648 | self.default['flags']
        else:
            self.fullscreen = False
            self.flags = self.default['flags']

        self.set_game_surface('Stone heart')



    # - Method to update the screen with delta time
    def delta_clock(self):
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
