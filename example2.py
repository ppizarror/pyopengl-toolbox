# coding=utf-8
"""
EXAMPLE 2
Draw axis and a object centered.

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
from pyOpenGLtoolbox.glpython import *
from pyOpenGLtoolbox.opengl_lib import *
from pyOpenGLtoolbox.camera import *
from pyOpenGLtoolbox.particles import *
from pyOpenGLtoolbox.figures import *
from pyOpenGLtoolbox.materials import *
from pyOpenGLtoolbox import create_axes

# Constants
AXES_LENGTH = 700
CAMERA_PHI = 45
CAMERA_RAD = 2000.0
CAMERA_ROT_VEL = 2.5
CAMERA_THETA = 56
FPS = 60
WINDOW_SIZE = [800, 600]

# Init window
init_pygame(WINDOW_SIZE[0], WINDOW_SIZE[1], 'Example 2', centered_window=True)
init_gl(transparency=False, materialcolor=False, normalized=True, lighting=True,
        numlights=1, perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
        texture=True, verbose=False)
reshape(*WINDOW_SIZE)
init_light(GL_LIGHT0)
clock = pygame.time.Clock()

# Display help on console
print('Rotate X axis with W/S keys')
print('Rotate Y axis with A/D keys')
print('Rotate Z axis with Q/E keys')
print('Zoom in/out with N/M keys')

# Create objects
axis = create_axes(AXES_LENGTH)  # Axis
camera = CameraR(CAMERA_RAD, CAMERA_PHI, CAMERA_THETA)  # Spheric camera

cube = Particle()
cube.add_property('GLLIST', create_cube())
cube.add_property('SIZE', [400, 400, 400])
cube.add_property('MATERIAL', material_gold)
cube.set_name('Cube')

light = Particle(1000, 1000, 100)
light.set_name('Light')
light.add_property('GLLIST', create_cube())
light.add_property('SIZE', [15, 15, 15])
light.add_property('MATERIAL', material_silver)

# Main loop
while True:
    clock.tick(FPS)
    clear_buffer()
    camera.place()
    if is_light_enabled():
        glDisable(GL_LIGHTING)
        glCallList(axis)
        glEnable(GL_LIGHTING)
    else:
        glCallList(axis)

    # Se actualizan modelos
    light.update()
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
              light.get_property('SIZE'))

    # Draw models
    cube.exec_property_func('MATERIAL')
    # noinspection PyArgumentEqualDefault
    draw_list(cube.get_property('GLLIST'), cube.get_position_list(), 0, None,
              cube.get_property('SIZE'), None)

    # Rotate camera around X axis
    if keys[K_w]:
        camera.rotate_x(CAMERA_ROT_VEL)
    elif keys[K_s]:
        camera.rotate_x(-CAMERA_ROT_VEL)

    # Rotate camera around Y axis
    if keys[K_a]:
        camera.rotate_y(-CAMERA_ROT_VEL)
    elif keys[K_d]:
        camera.rotate_y(CAMERA_ROT_VEL)

    # Rotate camera around Z axis
    if keys[K_q]:
        camera.rotate_z(-CAMERA_ROT_VEL)
    elif keys[K_e]:
        camera.rotate_z(CAMERA_ROT_VEL)

    # Close / Far camera
    if keys[K_n]:
        camera.close()
    elif keys[K_m]:
        camera.far()

    pygame.display.flip()
