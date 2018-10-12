# coding=utf-8
"""
PYOPENGL-TOOLBOX UTILS
General purpouse functions.

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
from __future__ import print_function
from OpenGL.GL import glColor3fv, glRasterPos3f, glColor4fv, glGenLists, glNewList, GL_COMPILE, GL_LINES, glBegin, \
    glEnd, glEndList
from OpenGL.GLUT import *
from PyOpenGLtoolbox.utils_math import Point3
from PyOpenGLtoolbox.utils_geometry import draw_vertex_list

# Constants
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [1, 1, 1]
_ERRS = [False]


def print_gl_error(err_msg):
    """Imprime un error en consola"""
    print('[GL-ERROR] {0}'.format(err_msg))


def is_windows():
    """Retorna true/false si el sistema operativo cliente es windows"""
    if os.name == "nt":
        return True
    return False


# noinspection PyUnresolvedReferences
def create_axes(s, both=False, text=True):
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
        draw_vertex_list([o, x])
        glColor4fv([0, 1, 0, 1])
        draw_vertex_list([o, y])
        glColor4fv([0, 0, 1, 1])
        draw_vertex_list([o, z])

        if both:  # Se dibujan los ejes en ambos sentidos
            x = Point3(-s, 0, 0)
            y = Point3(0, -s, 0)
            z = Point3(0, 0, -s)

            glColor4fv([1, 0, 0, 1])
            draw_vertex_list([o, x])
            glColor4fv([0, 1, 0, 1])
            draw_vertex_list([o, y])
            glColor4fv([0, 0, 1, 1])
            draw_vertex_list([o, z])

        glEnd()

        if text:  # Se dibujan los nombres de los ejes
            draw_text("x", Point3(s + 60, 0, -15), [1, 0, 0],
                      GLUT_BITMAP_HELVETICA_18)
            draw_text("y", Point3(0, s + 50, -15), [0, 1, 0],
                      GLUT_BITMAP_HELVETICA_18)
            draw_text("z", Point3(+0, +0, s + 50), [0, 0, 1],
                      GLUT_BITMAP_HELVETICA_18)

            if both:
                draw_text("-x", Point3(-s - 60, 0, -15), [1, 0, 0],
                          GLUT_BITMAP_HELVETICA_18)
                draw_text("-y", Point3(0, -s - 70, -15), [0, 1, 0],
                          GLUT_BITMAP_HELVETICA_18)
                draw_text("-z", Point3(+0, +0, -s - 80), [0, 0, 1],
                          GLUT_BITMAP_HELVETICA_18)

        # Se retorna la lista
        glEndList()
        return lista

    else:
        raise Exception("la dimension de los ejes debe ser mayor a cero")


def draw_text(text, pos, color=None, font='GLUT_BITMAP_TIMES_ROMAN_24',
              linespace=20):
    """Dibuja un texto en una posicon dada por un punto point3"""
    if color is None:
        color = COLOR_WHITE
    glColor3fv(color)
    if isinstance(pos, Point3):
        x = pos.get_x()
        y = pos.get_y()
        z = pos.get_z()
        glRasterPos3f(x, y, z)
        for char in text:
            if char == "\n":
                y += linespace
                glRasterPos3f(x, y, z)
            else:
                # noinspection PyBroadException
                try:
                    glutBitmapCharacter(font, ord(char))
                except:
                    if not _ERRS[0]:
                        print_gl_error('Actual OpenGL version doest not support glutBitmapCharacter function')
                    _ERRS[0] = True
    else:
        raise Exception("el punto debe ser del tipo point3")


def get_rgb_normalized(r, g, b, a=1.0):
    """Retorna una lista con el color rgb normalizado"""
    return r / 255.0, g / 255.0, b / 255.0, a


def set_rgb_color(r, g, b, a=1.0):
    """Define el color de dibujado RGB"""
    glColor4fv(get_rgb_normalized(r, g, b, a))
