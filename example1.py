# coding=utf-8
"""
Example 1
Draw axis and camera.

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
FPS = 60
WINDOW_SIZE = [800, 600]

# Init window
init_pygame(WINDOW_SIZE[0], WINDOW_SIZE[1], 'Example 1')
init_gl(lighting=True, numlights=1, perspectivecorr=True, textures=True, verbose=True, version=True)
reshape_window_perspective(WINDOW_SIZE[0], WINDOW_SIZE[1], near=1, far=10000)
init_light(GL_LIGHT0)
clock = pygame.time.Clock()

# Display help on console
print('Cartesian XYZ camera')
print('Rotate X axis with W/S keys')
print('Rotate Y axis with A/D keys')
print('Rotate Z axis with Q/E keys')
print('Zoom in/out with N/M keys')

# Create objects
axis = create_axes(AXES_LENGTH)  # Axis
camera = CameraXYZ(Point3(1000, 1000, 1000))  # Camera aligned with z axis in position (x,y,z)
camera.set_radial_vel(100)

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

    # Check events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # Close app
            exit()

    # Check pressed keys
    keys = pygame.key.get_pressed()

    # Rotate camera around X axis
    if keys[K_w]:
        camera.rotate_x(2.5)
    elif keys[K_s]:
        camera.rotate_x(-2.5)

    # Rotate camera around Y axis
    if keys[K_a]:
        camera.rotate_y(-2.5)
    elif keys[K_d]:
        camera.rotate_y(2.5)

    # Rotate camera around Z axis
    if keys[K_q]:
        camera.rotate_z(-2.5)
    elif keys[K_e]:
        camera.rotate_z(2.5)

    # Close / Far camera
    if keys[K_n]:
        camera.close()
    elif keys[K_m]:
        camera.far()

    pygame.display.flip()
