# coding=utf-8
"""
EJEMPLO 3.
Se dibujan los ejes, una cámara y una partícula en el centro con textura que rota.
"""

# Importación de librerías
from pyOpenglToolbox.glpython import *
from pyOpenglToolbox.opengl_lib import *
from pyOpenglToolbox.camera import *
from pyOpenglToolbox.particles import *
from pyOpenglToolbox.figures import *
from pyOpenglToolbox.materials import *
from pyOpenglToolbox.textures import *
from pyOpenglToolbox.shader import *

# Constantes
AXES_LENGTH = 700
CAMERA_PHI = 45
CAMERA_RAD = 1700.0
CAMERA_ROT_VEL = 2.5
CAMERA_THETA = 56
FPS = 60
NUM_LIGHTS = 2
WINDOW_SIZE = [800, 600]

# Se inicia ventana
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], 'Ejemplo Ejes mas Cubo',
           centered=True)
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True,
       numlights=NUM_LIGHTS,
       perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
       texture=True, verbose=False)
reshape(*WINDOW_SIZE)
# noinspection PyArgumentEqualDefault
initLight(GL_LIGHT0)
initLight(GL_LIGHT1, ambient=AMBIENT_COLOR_RED, diffuse=DIFFUSE_COLOR_RED,
          specular=SPECULAR_COLOR_RED)
clock = pygame.time.Clock()

# Se cargan texturas
textures = [
    load_texture('ejemplo_data/metal-texture.jpg'),
    load_texture('ejemplo_data/metal-normal.jpg'),
    load_texture('ejemplo_data/metal-bump.jpg')
]

# Se carga el shader
program = load_shader('ejemplo_data/', 'normalMapShader', [NUM_LIGHTS],
                      [3, NUM_LIGHTS])
program.set_name('NormalMap Shader')

# Se crean objetos
axis = create_axes(AXES_LENGTH)  # Ejes
camera = CameraR(CAMERA_RAD, CAMERA_PHI,
                 CAMERA_THETA)  # Cámara del tipo esférica

cubo = Particle()
cubo.add_property('GLLIST', create_cube_textured(textures))
cubo.add_property('SIZE', [400, 400, 400])
cubo.add_property('MATERIAL', material_silver)
cubo.set_name('Cubo')

luz = Particle(1000, 1000, 100)
luz.set_name('Luz móvil (1)')
luz.add_property('GLLIST', create_cube())
luz.add_property('SIZE', [15, 15, 15])
luz.add_property('MATERIAL', material_gold)

luz_fija = Particle(1000, -1000, 1000)
luz_fija.set_name('Luz fija (2)')
luz_fija.add_property('GLLIST', create_cube())
luz_fija.add_property('SIZE', [15, 15, 15])
luz_fija.add_property('MATERIAL', material_ruby)

# Bucle principal
while True:

    # Crea contador, limpia ventana, establece cámara
    clock.tick(FPS)
    clearBuffer()
    camera.place()

    # Rota luz
    luz.rotate_x(1)
    luz.rotate_y(-1)
    luz.rotate_z(0.5)
    if islightEnabled():
        glDisable(GL_LIGHTING)
        glCallList(axis)
        glEnable(GL_LIGHTING)
    else:
        glCallList(axis)

    # Se actualizan modelos
    luz.update()
    luz_fija.update()
    cubo.update()

    # Se comprueban eventos
    for event in pygame.event.get():
        if event.type == QUIT:  # Cierra la aplicación
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Cierra la aplicación
                exit()

    # Dibuja luces
    luz.exec_property_func('MATERIAL')
    glLightfv(GL_LIGHT0, GL_POSITION, luz.get_position_list())
    # noinspection PyArgumentEqualDefault
    draw_list(luz.get_property('GLLIST'), luz.get_position_list(), 0, None,
              luz.get_property('SIZE'), None)

    luz_fija.exec_property_func('MATERIAL')
    glLightfv(GL_LIGHT1, GL_POSITION, luz_fija.get_position_list())
    # noinspection PyArgumentEqualDefault
    draw_list(luz_fija.get_property('GLLIST'), luz_fija.get_position_list(), 0,
              None, luz_fija.get_property('SIZE'),
              None)

    # Dibuja modelos
    program.start()
    program.uniformi('toggletexture', True)
    program.uniformi('togglebump', True)
    program.uniformi('toggleparallax', True)
    cubo.get_property('MATERIAL')()
    for i in range(3):
        program.uniformi('texture[{0}]'.format(i), i)
    # noinspection PyArgumentEqualDefault
    draw_list(cubo.get_property('GLLIST'), cubo.get_position_list(), 0, None,
              cubo.get_property('SIZE'), None)
    program.stop()

    # Comprueba las teclas presionadas
    keys = pygame.key.get_pressed()

    if keys[K_w]:
        camera.rotateX(CAMERA_ROT_VEL)
    elif keys[K_s]:
        camera.rotateX(-CAMERA_ROT_VEL)

    # Rotar la cámara en el eje Y
    if keys[K_a]:
        camera.rotateY(-CAMERA_ROT_VEL)
    elif keys[K_d]:
        camera.rotateY(CAMERA_ROT_VEL)

    # Rotar la cámara en el eje Z
    if keys[K_q]:
        camera.rotateZ(-CAMERA_ROT_VEL)
    elif keys[K_e]:
        camera.rotateZ(CAMERA_ROT_VEL)

    # Acerca / aleja la cámara
    if keys[K_n]:
        camera.close()
    elif keys[K_m]:
        camera.far()

    pygame.display.flip()
