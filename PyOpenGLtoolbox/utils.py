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
from PyOpenGLtoolbox.geometry import draw_vertex_list
from PyOpenGLtoolbox.mathlib import Point3
import sys as _sys

# noinspection PyPep8Naming
import OpenGL.GL as _gl

# noinspection PyPep8Naming
import OpenGL.GLUT as _glut

# Constants
_UTILS_COLOR_BLACK = [0, 0, 0]
_UTILS_COLOR_WHITE = [1, 1, 1]
_UTILS_ERRS = [False]


def print_gl_error(err_msg):
    """
    Prints an OpenGL error to console.

    :param err_msg: Error message
    :type err_msg: basestring
    """
    if len(err_msg) == 0:
        return
    print('[GL-ERROR] {0}'.format(err_msg), file=_sys.stderr)


# noinspection PyUnresolvedReferences
def create_axes(length, both=False, text=False, font=_glut.GLUT_BITMAP_HELVETICA_18):
    """
    Create axes system.

    :param length: Axes length
    :param both: Both axes
    :param text: Show axes names (x,y,z)
    :param font: Font
    :type length: float, int
    :type both: bool
    :type text: bool
    :type font: int
    :return: OpenGL list
    """
    if length > 0:  # Valid length

        # Crate points
        x = Point3(length, 0, 0)
        y = Point3(0, length, 0)
        z = Point3(0, 0, length)
        o = Point3()

        # Create list
        lista = _gl.glGenLists(1)
        _gl.glNewList(lista, _gl.GL_COMPILE)

        # Init primitve
        _gl.glBegin(_gl.GL_LINES)
        _gl.glColor4fv([1, 0, 0, 1])
        draw_vertex_list([o, x])
        _gl.glColor4fv([0, 1, 0, 1])
        draw_vertex_list([o, y])
        _gl.glColor4fv([0, 0, 1, 1])
        draw_vertex_list([o, z])

        if both:  # Draw axes in both directions
            x = Point3(-length, 0, 0)
            y = Point3(0, -length, 0)
            z = Point3(0, 0, -length)
            _gl.glColor4fv([1, 0, 0, 1])
            draw_vertex_list([o, x])
            _gl.glColor4fv([0, 1, 0, 1])
            draw_vertex_list([o, y])
            _gl.glColor4fv([0, 0, 1, 1])
            draw_vertex_list([o, z])

        # End primitive
        _gl.glEnd()

        if text:  # Draw axes names
            draw_text('x', Point3(length + 60, 0, -15), [1, 0, 0], font)
            draw_text('y', Point3(0, length + 50, -15), [0, 1, 0], font)
            draw_text('z', Point3(+0, +0, length + 50), [0, 0, 1], font)

            if both:
                draw_text('-x', Point3(-length - 60, 0, -15), [1, 0, 0], font)
                draw_text('-y', Point3(0, -length - 70, -15), [0, 1, 0], font)
                draw_text('-z', Point3(+0, +0, -length - 80), [0, 0, 1], font)

        # Returns list
        _gl.glEndList()
        return lista

    else:
        raise Exception('Axes length must be positive, greater than zero')


# noinspection PyUnresolvedReferences
def draw_text(text, pos, color=None, font=_glut.GLUT_BITMAP_TIMES_ROMAN_24, linespace=20):
    """Dibuja un texto en una posicon dada por un punto point3"""
    if color is None:
        color = _UTILS_COLOR_WHITE
    _gl.glColor3fv(color)
    if isinstance(pos, Point3):
        x = pos.get_x()
        y = pos.get_y()
        z = pos.get_z()
        _gl.glRasterPos3f(x, y, z)
        for char in text:
            if char == "\n":
                y += linespace
                _gl.glRasterPos3f(x, y, z)
            else:
                # noinspection PyBroadException
                try:
                    glutBitmapCharacter(font, ord(char))
                except:
                    if not _UTILS_ERRS[0]:
                        print_gl_error('Actual OpenGL version doest not support glutBitmapCharacter function')
                    _UTILS_ERRS[0] = True
    else:
        raise Exception('Point must be Point3 type')


def get_rgb_normalized(r, g, b, a=1.0):
    """
    Return rgb color normalized (from 0 to 1).

    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :param a: Alpha
    :type r: float, int
    :type g: float, int
    :type b: float, int
    :type a: float
    :return: RGBA tuple
    :rtype: tuple
    """
    if r <= 1 and g <= 1 and b <= 1:
        return r, g, b, a
    return r / 255.0, g / 255.0, b / 255.0, a
