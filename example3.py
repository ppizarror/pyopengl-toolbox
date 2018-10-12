# coding=utf-8
"""
EXAMPLE 3
Draw axis, camera and a textured object.
"""

# Library imports
from pyOpenglToolbox.camera import *
from pyOpenglToolbox.figures import *
from pyOpenglToolbox.glpython import *
from pyOpenglToolbox.materials import *
from pyOpenglToolbox.opengl_lib import *
from pyOpenglToolbox.particles import *
from pyOpenglToolbox.shader import *
from pyOpenglToolbox.textures import *

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
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], 'Example 3', centered=True)
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True,
       numlights=NUM_LIGHTS, perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
       texture=True, verbose=False)
reshape(*WINDOW_SIZE)
initLight(GL_LIGHT0)
initLight(GL_LIGHT1, ambient=AMBIENT_COLOR_RED, diffuse=DIFFUSE_COLOR_RED,
          specular=SPECULAR_COLOR_RED)
clock = pygame.time.Clock()

# Display help on console
print('Rotate X axis with W/S keys')
print('Rotate Y axis with A/D keys')
print('Rotate Z axis with Q/E keys')
print('Zoom in/out with N/M keys')

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
    clearBuffer()
    camera.place()

    # Rotate light
    light.rotate_x(1)
    light.rotate_y(-1)
    light.rotate_z(0.5)
    if islightEnabled():
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
    draw_list(light.get_property('GLLIST'), light.get_position_list(), 0, None,
              light.get_property('SIZE'), None)

    static_light.exec_property_func('MATERIAL')
    glLightfv(GL_LIGHT1, GL_POSITION, static_light.get_position_list())
    draw_list(static_light.get_property('GLLIST'), static_light.get_position_list(), 0,
              None, static_light.get_property('SIZE'),
              None)

    # Draw model
    program.start()
    program.uniformi('toggletexture', True)
    program.uniformi('togglebump', True)
    program.uniformi('toggleparallax', True)
    cube.get_property('MATERIAL')()
    for i in range(3):
        program.uniformi('texture[{0}]'.format(i), i)
    draw_list(cube.get_property('GLLIST'), cube.get_position_list(), 0, None,
              cube.get_property('SIZE'), None)
    program.stop()

    # Rotate camera around X axis
    if keys[K_w]:
        camera.rotateX(CAMERA_ROT_VEL)
    elif keys[K_s]:
        camera.rotateX(-CAMERA_ROT_VEL)

    # Rotate camera around Y axis
    if keys[K_a]:
        camera.rotateY(-CAMERA_ROT_VEL)
    elif keys[K_d]:
        camera.rotateY(CAMERA_ROT_VEL)

    # Rotate camera around Z axis
    if keys[K_q]:
        camera.rotateZ(-CAMERA_ROT_VEL)
    elif keys[K_e]:
        camera.rotateZ(CAMERA_ROT_VEL)

    # Close / Far camera
    if keys[K_n]:
        camera.close()
    elif keys[K_m]:
        camera.far()

    pygame.display.flip()
