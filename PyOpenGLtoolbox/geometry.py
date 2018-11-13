# coding=utf-8
"""
PYOPENGL-TOOLBOX GEOMETRY
Utilitary geometry functions.

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
from PyOpenGLtoolbox.mathlib import _UTILS_MATH_POINT_2, _UTILS_MATH_POINT_3, Vector3, _normal_3_points

# noinspection PyPep8Naming
import OpenGL.GL as _gl


def draw_vertex_list(vertex_list):
    """
    Draw a list of Point2/Point3.

    :param vertex_list: Vertex list
    :type vertex_list: list
    """
    if len(vertex_list) >= 1:
        if vertex_list[0].get_type() == _UTILS_MATH_POINT_2:
            for vertex in vertex_list:
                _gl.glVertex2fv(vertex.export_to_list())
        elif vertex_list[0].get_type() == _UTILS_MATH_POINT_3:
            for vertex in vertex_list:
                _gl.glVertex3fv(vertex.export_to_list())
    else:
        raise Exception('Empty list')


def draw_vertex_list_normal(normal, vertex_list):
    """
    Draw Point2/Point3 list with an normal.

    :param normal: Normal
    :param vertex_list: Vertex list
    :type normal: Vector3
    :type vertex_list: list
    """
    if len(vertex_list) >= 3:
        if isinstance(normal, Vector3):
            _gl.glNormal3fv(normal.export_to_list())
            draw_vertex_list(vertex_list)
        else:
            raise Exception('normal must be Vector3 type')
    else:
        raise Exception('Not enough vertex, list must contain at least 3 vertex')


def draw_vertex_list_create_normal(vertex_list):
    """
    Draw a list of points, function create a normal automatically.

    :param vertex_list: Vertex list
    :type vertex_list: list
    """
    if len(vertex_list) >= 3:
        normal = _normal_3_points(vertex_list[0], vertex_list[1], vertex_list[2])
        draw_vertex_list_normal(normal, vertex_list)
    else:
        raise Exception('Not enough vertex, list must contain at least 3 vertex')


def draw_vertex_list_textured(vertex_list, tvertex_list):
    """
    Draw a Point2/Point3 list with an Poin2 list of edges for textured models.

    :param vertex_list: Vertex list
    :param tvertex_list: Point2 vertex list
    :type vertex_list: list
    :type tvertex_list: list
    """
    if len(vertex_list) >= 1:
        if vertex_list[0].get_type() == _UTILS_MATH_POINT_2:
            for vertex in range(len(vertex_list)):
                _gl.glTexCoord2fv(tvertex_list[vertex].export_to_list())
                _gl.glVertex2fv(vertex_list[vertex].export_to_list())
        elif vertex_list[0].get_type() == _UTILS_MATH_POINT_3:
            for vertex in range(len(vertex_list)):
                _gl.glTexCoord2fv(tvertex_list[vertex].export_to_list())
                _gl.glVertex3fv(vertex_list[vertex].export_to_list())
        else:
            raise Exception('Type vertex_list must be Point2/Point3')
    else:
        raise Exception('Empty list')


def draw_vertex_list_normal_textured(normal, vertex_list, tvertex_list):
    """
    Draw a Point2/Point3 list with an Poin2 list of edges for textured models with an normal.

    :param normal: Normal
    :param vertex_list: Vertex list
    :param tvertex_list: Point2 vertex list
    :type normal: Vector3
    :type vertex_list: list
    :type tvertex_list: list
    """
    if len(vertex_list) >= 1:
        if len(tvertex_list) >= 3:
            if isinstance(normal, Vector3):
                _gl.glNormal3fv(normal.export_to_list())
                draw_vertex_list_textured(vertex_list, tvertex_list)
            else:
                raise Exception('normal must be Vector3 type')
        else:
            raise Exception('Not enough vertex')
    else:
        raise Exception('Empty vertex list')


def draw_vertex_list_create_normal_textured(vertex_list, tvertex_list):
    """
    Create a list of Point3 points with an list of Point2 edges for textured models, creating
    an normal.

    :param vertex_list: Vertex list
    :param tvertex_list: Texture vertex list
    :type vertex_list: list
    :type tvertex_list: list
    """
    if len(vertex_list) >= 3:
        normal = _normal_3_points(vertex_list[0], vertex_list[1], vertex_list[2])
        draw_vertex_list_normal_textured(normal, vertex_list, tvertex_list)
    else:
        raise Exception('Not enough vertex')


def draw_list(gl_list, pos=None, angle=0.0, rotation_list=None, scale_list=None, color_list=None):
    """
    Draw an opengl list.

    :param gl_list: OpenGL list
    :param pos: Position
    :param angle: Angle
    :param rotation_list: Rotation list
    :param scale_list: Scale list
    :param color_list: Color list
    :type pos: list, None
    :type angle: float, int
    :type rotation_list: list, None
    :type scale_list: list, None
    :type color_list: list, None
    """
    if pos is None:
        pos = [0.0, 0.0, 0.0]
    _gl.glPushMatrix()
    _gl.glTranslate(pos[0], pos[1], pos[2])
    if scale_list is not None:
        _gl.glScale(scale_list[0], scale_list[1], scale_list[2])
    if rotation_list is not None:
        _gl.glRotatef(angle, rotation_list[0], rotation_list[1], rotation_list[2])
    if color_list is not None:
        _gl.glColor4fv(color_list)
    _gl.glCallList(gl_list)
    _gl.glPopMatrix()
