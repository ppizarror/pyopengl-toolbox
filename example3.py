# coding=utf-8
"""
EXAMPLE 3
Draw axis, camera and a textured object.

MIT License
Copyright (c) 2018 Pablo Pizarro R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Library imports
from PyOpenGLtoolbox import *

# Constants
AXES_LENGTH = 700
CAMERA_PHI = 45
CAMERA_RAD = 1700.0
CAMERA_ROT_VEL = 2.5
CAMERA_THETA = 56
FPS = 60
NUM_LIGHTS = 2
WINDOW_SIZE = [800, 600]

# Init window
init_pygame(WINDOW_SIZE[0], WINDOW_SIZE[1], 'Example 3')
init_gl(materialcolor=False, lighting=True, numlights=NUM_LIGHTS, perspectivecorr=True, textures=True)
reshape_window_perspective(WINDOW_SIZE[0], WINDOW_SIZE[1], near=10, far=10000)
init_light(GL_LIGHT0)
init_light(GL_LIGHT1, ambient=[0.403, 0.0, 0.0, 1.0], diffuse=[0.556, 0.0, 0.0, 1.0],
           specular=[0.858, 0.0, 0.0, 1.0])
clock = pygame.time.Clock()

# Display help on console
print('Spherical camera')
print('Rotate PHI angle with W/S keys')
print('Rotate THETA angle with A/D keys')
print('Decrease radial distance with N/M keys')

# Load textures
textures = [
    load_texture('example_data/metal-texture.jpg'),
    load_texture('example_data/metal-normal.jpg'),
    load_texture('example_data/metal-bump.jpg')
]

# Creates shader
program = load_shader('example_data/', 'normalMapShader', [NUM_LIGHTS], [3, NUM_LIGHTS])
program.set_name('NormalMap Shader')

# Create objects
axis = create_axes(AXES_LENGTH)  # Axis
camera = CameraR(CAMERA_RAD, CAMERA_PHI, CAMERA_THETA)  # Spheric camera

cube = Particle()
cube.add_property('GLLIST', create_cube_textured(textures))
cube.add_property('SIZE', [400, 400, 400])
cube.add_property('MATERIAL', material_silver)
cube.set_name('Cube')

light = Particle(1000, 1000, 100)
light.set_name('Dynamic light (1)')
light.add_property('GLLIST', create_cube())
light.add_property('SIZE', [15, 15, 15])
light.add_property('MATERIAL', material_gold)

static_light = Particle(1000, -1000, 1000)
static_light.set_name('Light fixed (2)')
static_light.add_property('GLLIST', create_cube())
static_light.add_property('SIZE', [15, 15, 15])
static_light.add_property('MATERIAL', material_ruby)

# Main loop
while True:

    # Creatos counter, clears buffer
    clock.tick(FPS)
    clear_buffer()
    camera.place()

    # Rotate light
    light.rotate_x(0.5)
    light.rotate_y(-0.5)
    light.rotate_z(0.5)
    if is_light_enabled():
        glDisable(GL_LIGHTING)
        glCallList(axis)
        glEnable(GL_LIGHTING)
    else:
        glCallList(axis)

    # Update model
    light.update()
    static_light.update()
    cube.update()

    # Check events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # Close app
            exit()

    # Check pressed keys
    keys = pygame.key.get_pressed()

    # Draw lights
    light.exec_property_func('MATERIAL')
    glLightfv(GL_LIGHT0, GL_POSITION, light.get_position_list())
    # noinspection PyArgumentEqualDefault
    draw_list(light.get_property('GLLIST'), light.get_position_list(), 0, None,
              light.get_property('SIZE'), None)

    static_light.exec_property_func('MATERIAL')
    glLightfv(GL_LIGHT1, GL_POSITION, static_light.get_position_list())
    # noinspection PyArgumentEqualDefault
    draw_list(static_light.get_property('GLLIST'), static_light.get_position_list(), 0,
              None, static_light.get_property('SIZE'), None)

    # Draw model
    program.start()
    program.uniformi('toggletexture', True)
    program.uniformi('togglebump', True)
    program.uniformi('toggleparallax', True)
    cube.get_property('MATERIAL')()
    for i in range(3):
        program.uniformi('texture[{0}]'.format(i), i)
    # noinspection PyArgumentEqualDefault
    draw_list(cube.get_property('GLLIST'), cube.get_position_list(), 0, None,
              cube.get_property('SIZE'), None)
    program.stop()

    # Rotate camera theta angle
    if keys[K_w]:
        camera.rotate_theta(CAMERA_ROT_VEL)
    elif keys[K_s]:
        camera.rotate_theta(-CAMERA_ROT_VEL)

    # Rotate camera phi angle
    if keys[K_a]:
        camera.rotate_phi(-CAMERA_ROT_VEL)
    elif keys[K_d]:
        camera.rotate_phi(CAMERA_ROT_VEL)

    # Close / Far camera
    if keys[K_n]:
        camera.close()
    elif keys[K_m]:
        camera.far()

    pygame.display.flip()
