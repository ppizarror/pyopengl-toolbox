# coding=utf-8
"""
GLPYTHON
Funciones utilitarias para manejar PyOpenGL.

Copyright (C) 2017 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Importación de librerías
import pygame
from pygame.locals import *


# Constantes
_DEFAULT_CAPTION = "Program title"


def initPygame(w, h, caption=_DEFAULT_CAPTION, center_mouse=False, icon=None):
    """Inicia el modulo de pygame"""
    pygame.init()
    pygame.display.set_mode((w, h), OPENGLBLIT | DOUBLEBUF)
    pygame.display.set_caption(caption)
    if center_mouse:
        pygame.mouse.set_pos(w / 2, h / 2)
    if icon is not None:
        pygame.display.set_icon(icon)


# noinspection PyBroadException,PyUnresolvedReferences
def loadPythonImage(path, convert=False):
    """Carga una imagen en python"""
    try:
        image = pygame.image.load(path)
        if convert:
            image = image.convert_alpha()
        return image
    except:
        print "fail"
        return None


def setCaption(caption):
    """Cambia el titulo de la ventana"""
    pygame.display.set_caption(caption)
