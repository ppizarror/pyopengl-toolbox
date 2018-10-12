# coding=utf-8
"""
PYOPENGL-TOOLBOX UTILS GEOMETRY
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
from OpenGL.GL import glVertex2fv, glVertex3fv, glNormal3fv, glTexCoord2fv, glPushMatrix, glTranslate, glScale, \
    glColor4fv, glRotatef, glCallList, glPopMatrix
from PyOpenGLtoolbox.utils_math import POINT_2, POINT_3, Vector3, normal_3_points


def draw_vertex_list(vertex_list):
    """Dibuja una lista de puntos Point2/Point3"""
    if len(vertex_list) >= 1:
        if vertex_list[0].get_type() == POINT_2:
            for vertex in vertex_list:
                glVertex2fv(vertex.export_to_list())
        elif vertex_list[0].get_type() == POINT_3:
            for vertex in vertex_list:
                glVertex3fv(vertex.export_to_list())
    else:
        raise Exception("lista vacia")


def draw_vertex_list_normal(normal, vertex_list):
    """Dibuja una lista de puntos Point2/Point3 con una normal"""
    if len(vertex_list) >= 3:
        if isinstance(normal, Vector3):
            glNormal3fv(normal.export_to_list())
            draw_vertex_list(vertex_list)
        else:
            raise Exception("la normal debe ser del tipo vector3")
    else:
        raise Exception("vertices insucifientes")


def draw_vertex_list_create_normal(vertex_list):
    """Dibuja una lista de puntos point2/point3 creando una normal"""
    if len(vertex_list) >= 3:
        normal = normal_3_points(vertex_list[0], vertex_list[1], vertex_list[2])
        draw_vertex_list_normal(normal, vertex_list)
    else:
        raise Exception("vertices insucifientes")


def draw_vertex_list_textured(vertex_list, tvertex_list):
    """Dibuja una lista de puntos point2/point3 con una lista Point2 de aristas
    para modelos texturados"""
    if len(vertex_list) >= 1:
        if vertex_list[0].get_type() == POINT_2:
            for vertex in range(len(vertex_list)):
                glTexCoord2fv(tvertex_list[vertex].export_to_list())
                glVertex2fv(vertex_list[vertex].export_to_list())
        elif vertex_list[0].get_type() == POINT_3:
            for vertex in range(len(vertex_list)):
                glTexCoord2fv(tvertex_list[vertex].export_to_list())
                glVertex3fv(vertex_list[vertex].export_to_list())
        else:
            raise Exception("el tipo de vertex_list debe ser POINT2 o POINT3")
    else:
        raise Exception("lista vacia")


def draw_vertex_list_normal_textured(normal, vertex_list, tvertex_list):
    """Dibuja una lista de puntos Point2/Point3 con una lista Point2 de aristas
    para modelos texturados con una normal"""
    if len(vertex_list) >= 1:
        if len(tvertex_list) >= 3:
            if isinstance(normal, Vector3):
                glNormal3fv(normal.export_to_list())
                draw_vertex_list_textured(vertex_list, tvertex_list)
            else:
                raise Exception("la normal debe ser del tipo vector3")
        else:
            raise Exception("vertices insuficientes")
    else:
        raise Exception("lista vacia")


def draw_vertex_list_create_normal_textured(vertex_list, tvertex_list):
    """Dibuja una lista de puntos point3 con una lista Point2 de aristas para modelos
    texturados creando una normal"""
    if len(vertex_list) >= 3:
        normal = normal_3_points(vertex_list[0], vertex_list[1], vertex_list[2])
        draw_vertex_list_normal_textured(normal, vertex_list, tvertex_list)
    else:
        raise Exception("vertices insuficientes")


def draw_list(lista, pos=None, angle=0.0, rot=None, sz=None, rgb=None):
    """
    Dibuja una lista de OpenGL

    :param lista: Lista OpenGL
    :param pos: Posición
    :param angle: Lista de ángulos a rotar
    :param rot: Indica si rota o no
    :param sz: Escalado de imagen
    :param rgb: Colores del objeto
    :return:
    """
    if pos is None:
        pos = [0.0, 0.0, 0.0]
    glPushMatrix()
    glTranslate(pos[0], pos[1], pos[2])
    if sz is not None:
        glScale(sz[0], sz[1], sz[2])
    if rot is not None:
        glRotatef(angle, rot[0], rot[1], rot[2])
    if rgb is not None:
        glColor4fv(rgb)
    glCallList(lista)
    glPopMatrix()
