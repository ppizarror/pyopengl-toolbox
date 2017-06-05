# coding=utf-8
"""
EJEMPLO 3.
Se dibujan los ejes, una cámara y una partícula en el centro con textura que rota.
"""

# Importación de librerías
from pygltoolbox.glpython import *
from pygltoolbox.opengl_lib import *
from pygltoolbox.camera import *
from pygltoolbox.particles import *
from pygltoolbox.figures import *
from pygltoolbox.materials import *
from pygltoolbox.textures import *
from pygltoolbox.shader import *

# Constantes
AXES_LENGTH = 700
CAMERA_PHI = 45
CAMERA_RAD = 1700.0
CAMERA_ROT_VEL = 2.5
CAMERA_THETA = 56
FPS = 60
WINDOW_SIZE = [800, 600]

# Se inicia ventana
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], "Ejemplo Ejes", centered=True)
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True, numlights=1,
       perspectivecorr=True, antialiasing=True, depth=True, smooth=True, texture=True, verbose=False)
reshape(*WINDOW_SIZE)
initLight(GL_LIGHT0)
clock = pygame.time.Clock()

# Se cargan texturas
textures = [
    loadTexture('metal-texture.jpg', False),
    loadTexture('metal-normal.jpg', False),
    loadTexture('metal-bump.jpg', False)
]

# Se carga el shader
program = loadShader('', 'normalMap', [1], [3, 1])
program.setName('Normal Map')

# Se crean objetos
axis = createAxes(AXES_LENGTH)  # Ejes
camera = CameraR(CAMERA_RAD, CAMERA_PHI, CAMERA_THETA)  # Camara del tipo esférica

cubo = Particle()
cubo.addProperty('GLLIST', create_cube_textured(textures))
cubo.addProperty('SIZE', [400, 400, 400])
cubo.addProperty('MATERIAL', material_silver)
cubo.setName('Cubo')

luz = Particle(1000, 1000, 100)
luz.setName('Luz')
luz.addProperty('GLLIST', create_cube())
luz.addProperty('SIZE', [15, 15, 15])
luz.addProperty('MATERIAL', material_gold)

# Bucle principal
while True:
    clock.tick(FPS)
    clearBuffer()
    camera.place()
    luz.rotateX(1)
    luz.rotateY(-1)
    luz.rotateZ(0.5)
    if islightEnabled():
        glDisable(GL_LIGHTING)
        glCallList(axis)
        glEnable(GL_LIGHTING)
    else:
        glCallList(axis)

    # Se actualizan modelos
    luz.update()
    cubo.update()

    # Se comprueban eventos
    for event in pygame.event.get():
        if event.type == QUIT:  # Cierra la aplicacion
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Cierra la aplicacion
                exit()

    # Dibuja luces
    luz.getProperty('MATERIAL')()
    glLightfv(GL_LIGHT0, GL_POSITION, luz.getPositionList())
    drawList(luz.getProperty('GLLIST'), luz.getPositionList(), 0, None, luz.getProperty('SIZE'), None)

    # Dibuja modelos
    program.start()
    program.uniformi('toggletexture', True)
    program.uniformi('togglebump', True)
    program.uniformi('toggleparallax', True)
    cubo.getProperty('MATERIAL')()
    for i in range(3):
        program.uniformi('texture[{0}]'.format(i), i)
    drawList(cubo.getProperty('GLLIST'), cubo.getPositionList(), 0, None, cubo.getProperty('SIZE'), None)
    program.stop()

    # Comprueba las teclas presionadas
    keys = pygame.key.get_pressed()

    if keys[K_w]:
        camera.rotateX(CAMERA_ROT_VEL)
    elif keys[K_s]:
        camera.rotateX(-CAMERA_ROT_VEL)

    # Rotar la camara en el eje Y
    if keys[K_a]:
        camera.rotateY(-CAMERA_ROT_VEL)
    elif keys[K_d]:
        camera.rotateY(CAMERA_ROT_VEL)

    # Rotar la camara en el eje Z
    if keys[K_q]:
        camera.rotateZ(-CAMERA_ROT_VEL)
    elif keys[K_e]:
        camera.rotateZ(CAMERA_ROT_VEL)

    # Acerca / aleja la camara
    if keys[K_n]:
        camera.close()
    elif keys[K_m]:
        camera.far()

    pygame.display.flip()
