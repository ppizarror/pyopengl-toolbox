# coding=utf-8
"""
UTILS
Funciones utilitarias generales.

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

# Importación de liberías
from OpenGL.GLUT import *
from utils_geometry import *

# Definicion de constantes
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [1, 1, 1]
_ERRS = [False]


def printGLError(err_msg):
    """Imprime un error en consola"""
    print "[GL-ERROR] {0}".format(err_msg)


def isWindows():
    """Retorna true/false si el sistema operativo cliente es windows"""
    if os.name == "nt":
        return True
    return False


# noinspection PyUnresolvedReferences
def createAxes(s, both=False, text=True):
    """Dibuja los ejes en pantalla"""
    # Se convierte la distancia a un entero positivo
    s = abs(s)

    if s > 0:  # Si es una distancia valida

        # Vectores de dibujo
        x = Point3(s, 0, 0)
        y = Point3(0, s, 0)
        z = Point3(0, 0, s)
        o = Point3()

        # Se crea nueva lista
        lista = glGenLists(1)
        glNewList(lista, GL_COMPILE)

        # Se agregan los vectores al dibujo
        glBegin(GL_LINES)

        glColor4fv([1, 0, 0, 1])
        drawVertexList([o, x])
        glColor4fv([0, 1, 0, 1])
        drawVertexList([o, y])
        glColor4fv([0, 0, 1, 1])
        drawVertexList([o, z])

        if both:  # Se dibujan los ejes en ambos sentidos
            x = Point3(-s, 0, 0)
            y = Point3(0, -s, 0)
            z = Point3(0, 0, -s)

            glColor4fv([1, 0, 0, 1])
            drawVertexList([o, x])
            glColor4fv([0, 1, 0, 1])
            drawVertexList([o, y])
            glColor4fv([0, 0, 1, 1])
            drawVertexList([o, z])

        glEnd()

        if text:  # Se dibujan los nombres de los ejes
            drawText("x", Point3(s + 60, 0, -15), [1, 0, 0], GLUT_BITMAP_HELVETICA_18)
            drawText("y", Point3(0, s + 50, -15), [0, 1, 0], GLUT_BITMAP_HELVETICA_18)
            drawText("z", Point3(+0, +0, s + 50), [0, 0, 1], GLUT_BITMAP_HELVETICA_18)

            if both:
                drawText("-x", Point3(-s - 60, 0, -15), [1, 0, 0], GLUT_BITMAP_HELVETICA_18)
                drawText("-y", Point3(0, -s - 70, -15), [0, 1, 0], GLUT_BITMAP_HELVETICA_18)
                drawText("-z", Point3(+0, +0, -s - 80), [0, 0, 1], GLUT_BITMAP_HELVETICA_18)

        # Se retorna la lista
        glEndList()
        return lista

    else:
        raise Exception("la dimension de los ejes debe ser mayor a cero")


# noinspection PyBroadException
def drawText(text, pos, color=COLOR_WHITE, font=GLUT_BITMAP_TIMES_ROMAN_24, linespace=20):
    """Dibuja un texto en una posicon dada por un punto point3"""
    glColor3fv(color)
    if isinstance(pos, Point3):
        x = pos.getX()
        y = pos.getY()
        z = pos.getZ()
        glRasterPos3f(x, y, z)
        for char in text:
            if char == "\n":
                y += linespace
                glRasterPos3f(x, y, z)
            else:
                try:
                    glutBitmapCharacter(font, ord(char))
                except:
                    if not _ERRS[0]:
                        printGLError("la version actual de OpenGL no posee la funcion glutBitmapCharacter")
                    _ERRS[0] = True
    else:
        raise Exception("el punto debe ser del tipo point3")


def getRGBNormalized(r, g, b, a=1.0):
    """Retorna una lista con el color rgb normalizado"""
    return r / 255.0, g / 255.0, b / 255.0, a


def setRGBColor(r, g, b, a=1.0):
    """Define el color de dibujado RGB"""
    glColor4fv(getRGBNormalized(r, g, b, a))
