# coding=utf-8
"""
EJEMPLO 1.
Se dibujan los ejes y una cámara.
"""

# Importación de librerías
from pyOpenglToolbox.glpython import *
from pyOpenglToolbox.opengl_lib import *
from pyOpenglToolbox.camera import *
from pyOpenglToolbox.particles import *

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
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True,
       numlights=1,
       perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
       texture=True, verbose=False)
reshape(*WINDOW_SIZE)
# noinspection PyArgumentEqualDefault
initLight(GL_LIGHT0)
clock = pygame.time.Clock()

# Se crean objetos
axis = create_axes(AXES_LENGTH)  # Ejes
camera = CameraR(CAMERA_RAD, CAMERA_PHI,
                 CAMERA_THETA)  # Cámara del tipo esférica

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

    # Se comprueban eventos
    for event in pygame.event.get():
        if event.type == QUIT:  # Cierra la aplicación
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Cierra la aplicación
                exit()

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
