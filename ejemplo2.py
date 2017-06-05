# coding=utf-8
"""
EJEMPLO 2.
Se dibujan los ejes, una cámara y una partícula en el centro.
"""

# Importación de librerías
from pygltoolbox.glpython import *
from pygltoolbox.opengl_lib import *
from pygltoolbox.camera import *
from pygltoolbox.particles import *
from pygltoolbox.figures import *
from pygltoolbox.materials import *

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

# Se crean objetos
axis = createAxes(AXES_LENGTH)  # Ejes
camera = CameraR(CAMERA_RAD, CAMERA_PHI, CAMERA_THETA)  # Camara del tipo esférica

cubo = Particle()
cubo.addProperty('GLLIST', create_cube())
cubo.addProperty('SIZE', [400, 400, 400])
cubo.addProperty('MATERIAL', material_gold)
cubo.setName('Cubo')

luz = Particle(1000, 1000, 100)
luz.setName('Luz')
luz.addProperty('GLLIST', create_cube())
luz.addProperty('SIZE', [15, 15, 15])
luz.addProperty('MATERIAL', material_silver)

# Bucle principal
while True:
    clock.tick(FPS)
    clearBuffer()
    camera.place()
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
    cubo.getProperty('MATERIAL')()
    drawList(cubo.getProperty('GLLIST'), cubo.getPositionList(), 0, None, cubo.getProperty('SIZE'), None)

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
