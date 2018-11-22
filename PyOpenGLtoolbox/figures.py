# coding=utf-8
"""
PYOPENGL-TOOLBOX FIGURES
Utilitary functions to draw figures in PyOpenGL.

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
from math import sqrt as _sqrt
from math import pi as _pi
from numpy import array as _array
from OpenGL.arrays import vbo as _vbo
from PyOpenGLtoolbox.utils import print_gl_error as _print_gl_error
from PyOpenGLtoolbox.geometry import _normal_3_points, draw_vertex_list_create_normal, \
    draw_vertex_list_create_normal_textured
from PyOpenGLtoolbox.mathlib import Point3, _cos, _sin, Point2

# noinspection PyPep8Naming
import OpenGL.GL as _gl
# noinspection PyPep8Naming
import OpenGL.GLUT as _glut

# Constants
_FIGURES_FIGURE_LIST = 0xfa01
_FIGURES_FIGURE_VBO = 0xfa02
_FIGURES_ERRS = []
for i in range(10):
    _FIGURES_ERRS.append(False)


class VBObject:
    """
    VBO object that can load and draw elements using shaders.
    """

    def __init__(self, vertex, fragment, total_vertex, texture=None):
        """
        Constructor.

        :param vertex: Vertex shader
        :param fragment: Fragment shader
        :param total_vertex: Total vertex (int)
        :param texture: Texture list
        """
        if isinstance(vertex, _vbo.VBO) and isinstance(fragment, _vbo.VBO):
            if type(total_vertex) is int:
                self.vertex = vertex
                self.fragment = fragment
                self.totalVertex = total_vertex
                self.texture = texture
                if self.texture is None:
                    self.texlen = 0
                else:
                    self.texlen = len(self.texture)
            else:
                raise Exception('total_vertex must be int type')
        else:
            raise Exception('vertex and fragment must be VBO type (OpenGL.arrays.vbo)')

    def draw(self, pos=None, rgb=None):
        """
        Draw the object.

        :param pos: Position
        :param rgb: Color
        :type pos: list
        :type rgb: list
        """

        if pos is None:
            pos = [0.0, 0.0, 0.0]
        try:

            # Create new matrix
            _gl.glPushMatrix()

            # Make bind between vbos and shader program
            self.vertex.bind()
            _gl.glVertexPointerf(self.vertex)
            self.fragment.bind()
            _gl.glNormalPointerf(self.fragment)

            # Enable vbos
            _gl.glEnableClientState(_gl.GL_VERTEX_ARRAY)
            _gl.glEnableClientState(_gl.GL_NORMAL_ARRAY)

            # Enable transform
            if rgb is not None:
                _gl.glColor4fv(rgb)
            _gl.glTranslate(pos[0], pos[1], pos[2])

            # Enable textures
            for _i in range(self.texlen):
                _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
                _gl.glEnable(_gl.GL_TEXTURE_2D)
                _gl.glBindTexture(_gl.GL_TEXTURE_2D, self.texture[_i])

            # Draw triangles each 3 elements of vbo
            _gl.glDrawArrays(_gl.GL_TRIANGLES, 0, self.totalVertex)

            # Dsiable textures
            for _i in range(self.texlen):
                _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
                _gl.glDisable(_gl.GL_TEXTURE_2D)

            # Disable vbox
            _gl.glDisableClientState(_gl.GL_VERTEX_ARRAY)
            _gl.glDisableClientState(_gl.GL_NORMAL_ARRAY)

            # Pop matrix
            _gl.glPopMatrix()

        except:
            raise Exception('VBO draw error')


def load_obj_model(file_name):
    """
    Load an OBJ file.

    :param file_name: File name
    :type file_name: basestring
    :return: OBJ file tuple
    :rtype: tuple
    """
    file_text = open(file_name)
    text = file_text.readlines()
    vertex = []
    normals = []
    uv = []
    faces_vertex = []
    faces_normal = []
    faces_uv = []

    for line in text:
        info = line.split(' ')
        if info[0] == 'v':
            vertex.append(
                (float(info[1]), float(info[2]) - 0.1, float(info[3])))
        elif info[0] == 'vn':
            normals.append((float(info[1]), float(info[2]), float(info[3])))
        elif info[0] == 'vt':
            uv.append((float(info[1]), float(info[2])))
        elif info[0] == 'f':
            p1 = info[1].split('/')
            p2 = info[2].split('/')
            p3 = info[3].split('/')
            faces_vertex.append((int(p1[0]), int(p2[0]), int(p3[0])))
            faces_uv.append((int(p1[1]), int(p2[1]), int(p3[1])))
            faces_normal.append((int(p1[2]), int(p2[2]), int(p3[2])))

    return vertex, normals, uv, faces_vertex, faces_normal, faces_uv


def load_gmsh_model(modelfile, scale, dx=0.0, dy=0.0, dz=0.0, avg=True,
                    neg_normal=False, texture=None):
    """
    Loads an .MSH or .GMSH file and returns an vboObject scaled as 'scale', by default
    normal are average, to disable use avg=False. The model also can be displaced by
    (dx,dy,dz) and reverse the normals if neg_normal is True.

    :param modelfile: File name
    :param scale: Scale parameter
    :param dx: X-displacement
    :param dy: Y-displacement
    :param dz: Z-displacement
    :param avg: Normal-avg
    :param neg_normal: Reverse normal
    :param texture: Texture file
    :type modelfile: basestring
    :type scale: float
    :type dx: float, int
    :type dy: float, int
    :type avg: bool
    :type neg_normal: bool
    :type texture: list
    :return: VBO Object that contains GMSH model
    :rtype: VBObject
    """

    def load(gmshfile, _scale, _dx, _dy, _dz):
        """
        Load an GMSH file and returns 3 lists, one for vertex, one for normals and another for
        normal averages. Takes file, scale and displacement.
        :param gmshfile: GMSH file
        :param _scale: Scale parameter
        :param _dx: X-displacement
        :param _dy: Y-displacement
        :param _dz: Z-displacement
        :return:
        """

        def get_ave_normals(_nodes, _elems):
            """
            Calculate normal average for each vertex
            :param _nodes:
            :param _elems:
            :return:
            """
            nodetrilist = []
            for _nodenum in range(len(_nodes)):
                nodetrilist.append([])
                for elemnum in range(len(_elems)):
                    if _nodenum in _elems[elemnum]:
                        nodetrilist[_nodenum].append(elemnum)
            _avenorms = []

            for tri in nodetrilist:
                ave_ni = 0.0
                ave_nj = 0.0
                ave_nk = 0.0
                denom = max(float(len(tri)), 1)
                for _elem in tri:
                    _vert1 = [_nodes[_elems[_elem][0]][0], _nodes[_elems[_elem][0]][1],
                              _nodes[_elems[_elem][0]][2]]
                    _vert2 = [_nodes[_elems[_elem][1]][0], _nodes[_elems[_elem][1]][1],
                              _nodes[_elems[_elem][1]][2]]
                    _vert3 = [_nodes[_elems[_elem][2]][0], _nodes[_elems[_elem][2]][1],
                              _nodes[_elems[_elem][2]][2]]
                    _normals = get_normals(_vert1, _vert2, _vert3)
                    ave_ni += _normals[0]
                    ave_nj += _normals[1]
                    ave_nk += _normals[2]
                _avenorms.append([ave_ni / denom, ave_nj / denom, ave_nk / denom])
            return _avenorms

        def get_normals(vert_a, vert_b, vert_c):
            """
            Calculate normal each 3 vertex
            :param vert_a:
            :param vert_b:
            :param vert_c:
            :return:
            """
            x_a = vert_a[0]
            x_b = vert_b[0]
            x_c = vert_c[0]
            y_a = vert_a[1]
            y_b = vert_b[1]
            y_c = vert_c[1]
            z_a = vert_a[2]
            z_b = vert_b[2]
            z_c = vert_c[2]
            a_bx = x_b - x_a
            a_by = y_b - y_a
            a_bz = z_b - z_a
            b_cx = x_c - x_b
            b_cy = y_c - y_b
            b_cz = z_c - z_b
            nx = a_by * b_cz - a_bz * b_cy
            ny = a_bz * b_cx - a_bx * b_cz
            nz = a_bx * b_cy - a_by * b_cx
            vec_mag = _sqrt(nx ** 2 + ny ** 2 + nz ** 2)
            ni = nx / vec_mag
            nj = ny / vec_mag
            nk = nz / vec_mag
            return [ni, nj, nk]

        # Read file
        try:
            infile = open(gmshfile)
        except:
            raise Exception('Model file does not exist')

        # Create model
        nodes = []
        try:
            gmshlines = infile.readlines()
            readnodes = False
            readelems = False
            skipline = 0
            elems = []
            lnum = 0
            for line in gmshlines:
                if '$Nodes' in line:
                    readnodes = True
                    skipline = 2
                    nnodes = int(gmshlines[lnum + 1].strip())
                    nodes = []
                    for _i in range(nnodes):
                        nodes.append(99999.9)
                elif '$EndNodes' in line:
                    readnodes = False
                    skipline = 1
                elif '$Elements' in line:
                    readelems = True
                    skipline = 2
                elif '$EndElements' in line:
                    readelems = False
                    skipline = 1
                if skipline < 1:
                    if readnodes:
                        n_xyz = line.strip().split()
                        nodenum = int(n_xyz[0]) - 1
                        n_x = float(n_xyz[1]) * _scale + _dx
                        n_y = float(n_xyz[2]) * _scale + _dy
                        n_z = float(n_xyz[3]) * _scale + _dz
                        if neg_normal:
                            n_z *= -1
                        nodes[nodenum] = [n_x, n_y, n_z]
                    elif readelems:
                        n123 = line.split()
                        if n123[1] == '2':
                            n1 = int(n123[-3]) - 1
                            n2 = int(n123[-1]) - 1
                            n3 = int(n123[-2]) - 1
                            elems.append([n1, n2, n3])
                else:
                    skipline -= 1
                lnum += 1
            triarray = []
            normarray = []
            avenorms = []
            nodeavenorms = get_ave_normals(nodes, elems)
            for elem in elems:
                vert1 = [nodes[elem[0]][0], nodes[elem[0]][1],
                         nodes[elem[0]][2]]
                vert2 = [nodes[elem[1]][0], nodes[elem[1]][1],
                         nodes[elem[1]][2]]
                vert3 = [nodes[elem[2]][0], nodes[elem[2]][1],
                         nodes[elem[2]][2]]
                avenorm0 = nodeavenorms[elem[0]]
                avenorm1 = nodeavenorms[elem[1]]
                avenorm2 = nodeavenorms[elem[2]]
                normals = get_normals(vert1, vert2, vert3)
                triarray.append(vert1)
                triarray.append(vert2)
                triarray.append(vert3)
                normarray.append(normals)
                normarray.append(normals)
                normarray.append(normals)
                avenorms.append(avenorm0)
                avenorms.append(avenorm1)
                avenorms.append(avenorm2)
            return triarray, normarray, avenorms

        except:
            raise Exception('Error load model')

    vertex, norm, avgnorm = load(modelfile, scale, float(dx), float(dy), float(dz))
    if avg:
        return VBObject(_vbo.VBO(_array(vertex, 'f')),
                        _vbo.VBO(_array(avgnorm, 'f')), len(vertex), texture)
    else:
        return VBObject(_vbo.VBO(_array(vertex, 'f')), _vbo.VBO(_array(norm, 'f')),
                        len(vertex), texture)


def create_sphere(lats=10, longs=10, color=None):
    """
    Creates an sphere.

    :param lats: Latitude
    :param longs: Longitude
    :param color: Color
    :type lats: int
    :type longs: int
    :type color: list
    :return: OpenGL list
    """
    if lats >= 3 and longs >= 10:
        obj = _gl.glGenLists(1)
        _gl.glNewList(obj, _gl.GL_COMPILE)
        _gl.glPushMatrix()
        if color is not None:
            _gl.glColor4fv(color)
        # noinspection PyBroadException
        try:
            _glut.glutSolidSphere(1.0, lats, longs)
        except:
            if not _FIGURES_ERRS[0]:
                _print_gl_error('OpenGL actual version does not support glutSolidSphere function')
            _FIGURES_ERRS[0] = True

            for _i in range(0, lats + 1):
                lat0 = _pi * (-0.5 + float(float(_i - 1) / float(lats)))
                z0 = _sin(lat0)
                zr0 = _cos(lat0)

                lat1 = _pi * (-0.5 + float(float(_i) / float(lats)))
                z1 = _sin(lat1)
                zr1 = _cos(lat1)

                # Use Quad strips to draw the sphere
                _gl.glBegin(_gl.GL_QUAD_STRIP)

                for _j in range(0, longs + 1):
                    long = 2 * _pi * float(float(_j - 1) / float(longs))
                    x = _cos(long)
                    y = _sin(long)
                    _gl.glNormal3f(x * zr0, y * zr0, z0)
                    _gl.glVertex3f(x * zr0, y * zr0, z0)
                    _gl.glNormal3f(x * zr1, y * zr1, z1)
                    _gl.glVertex3f(x * zr1, y * zr1, z1)

                _gl.glEnd()

        _gl.glPopMatrix()
        _gl.glEndList()
        return obj
    else:
        raise Exception('Latitude and logitude must be greater than 3')


def create_circle(rad=1.0, diff=0.1, normal=None, color=None):
    """
    Creates a circle.

    :param rad: Radius
    :param diff: Difference
    :param normal: Normal
    :param color: Color
    :type rad: float, int
    :type diff: float, int
    :type normal: list
    :type color: list
    :return: OpenGL list
    """
    if normal is None:
        normal = [0.0, 0.0, 1.0]
    if diff > 0:
        obj = _gl.glGenLists(1)
        _gl.glNewList(obj, _gl.GL_COMPILE)
        _gl.glPushMatrix()
        if color is not None:
            _gl.glColor4fv(color)
        ang = 0.0
        _gl.glBegin(_gl.GL_POLYGON)
        while ang <= 360.0:
            _gl.glNormal3fv(normal)
            _gl.glVertex2f(_sin(ang) * rad, _cos(ang) * rad)
            ang += diff
        _gl.glEnd()
        _gl.glBegin(_gl.GL_LINE_LOOP)
        while ang <= 360.0:
            _gl.glVertex2f(_sin(ang) * rad, _cos(ang) * rad)
            ang += diff
        _gl.glEnd()
        _gl.glPopMatrix()
        _gl.glEndList()
        return obj
    else:
        raise Exception('Difference must be greater than zero')


def create_cone(base=1.0, height=1.0, lat=20, lng=20, color=None):
    """
    Creates an cone with base and height, radius 1.

    :param base: Cone base
    :param height: Cone height
    :param lat: Cone latitude
    :param lng: Cone longitude
    :param color: Cone color
    :type base: float, int
    :type height: float, int
    :type lat: int
    :type lng: int
    :type color: list
    :return: OpenGL list
    """
    if lat >= 3 and lng >= 10:
        # noinspection PyArgumentEqualDefault
        circlebase = create_circle(base - 0.05, 0.1, [0.0, 0.0, -1.0], color)
        obj = _gl.glGenLists(1)
        _gl.glNewList(obj, _gl.GL_COMPILE)
        _gl.glPushMatrix()
        if color is not None:
            _gl.glColor4fv(color)
        # noinspection PyBroadException
        try:
            _glut.glutSolidCone(base, height, lat, lng)
        except:
            if not _FIGURES_ERRS[3]:
                _print_gl_error('OpenGL actual version does not support glutSolidCone function')
            _FIGURES_ERRS[3] = True
        _gl.glCallList(circlebase)
        _gl.glPopMatrix()
        _gl.glEndList()
        return obj
    else:
        raise Exception('Latitude and longitude of the figure must be greater than 3')


def create_cube(color=None):
    """
    Cretes a cube.

    :param color: Cube color
    :type color: list
    :return: OpenGL list
    """
    a = Point3(-1.0, -1.0, -1.0)
    b = Point3(1.0, -1.0, -1.0)
    c = Point3(1.0, -1.0, 1.0)
    d = Point3(-1.0, -1.0, 1.0)
    e = Point3(-1.0, 1.0, -1.0)
    f = Point3(1.0, 1.0, -1.0)
    g = Point3(1.0, 1.0, 1.0)
    h = Point3(-1.0, 1.0, 1.0)

    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    _gl.glBegin(_gl.GL_QUADS)
    if color is not None:
        _gl.glColor4fv(color)
    draw_vertex_list_create_normal([a, b, c, d])
    draw_vertex_list_create_normal([b, f, g, c])
    draw_vertex_list_create_normal([f, e, h, g])
    draw_vertex_list_create_normal([e, a, d, h])
    draw_vertex_list_create_normal([d, c, g, h])
    draw_vertex_list_create_normal([a, e, f, b])
    _gl.glEnd()
    _gl.glPopMatrix()
    _gl.glEndList()

    return obj


def create_cube_textured(texture_list):
    """
    Create a textured cube.

    :param texture_list: Texture OpenGL list
    :return: OpenGL list
    """
    a = Point3(-1.0, -1.0, -1.0)
    b = Point3(1.0, -1.0, -1.0)
    c = Point3(1.0, -1.0, 1.0)
    d = Point3(-1.0, -1.0, 1.0)
    e = Point3(-1.0, 1.0, -1.0)
    f = Point3(1.0, 1.0, -1.0)
    g = Point3(1.0, 1.0, 1.0)
    h = Point3(-1.0, 1.0, 1.0)
    t_list = [Point2(0, 0), Point2(1, 0), Point2(1, 1), Point2(0, 1)]

    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()

    for _i in range(len(texture_list)):
        _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glBindTexture(_gl.GL_TEXTURE_2D, texture_list[_i])
    _gl.glBegin(_gl.GL_QUADS)
    draw_vertex_list_create_normal_textured([a, b, c, d], t_list)
    draw_vertex_list_create_normal_textured([b, f, g, c], t_list)
    draw_vertex_list_create_normal_textured([f, e, h, g], t_list)
    draw_vertex_list_create_normal_textured([e, a, d, h], t_list)
    draw_vertex_list_create_normal_textured([d, c, g, h], t_list)
    draw_vertex_list_create_normal_textured([a, e, f, b], t_list)
    _gl.glEnd()

    for _i in range(len(texture_list)):
        _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
        _gl.glDisable(_gl.GL_TEXTURE_2D)
    _gl.glPopMatrix()
    _gl.glEndList()

    return obj


def create_torus(minr=0.5, maxr=1.0, lat=30, lng=30, color=None):
    """
    Creates a torus.

    :param minr: Minimum radius
    :param maxr: Maximum radius
    :param lat: Latitude
    :param lng: Longitude
    :param color: Color
    :type minr: float, int
    :type maxr: float, int
    :type lat: int
    :type lng: int
    :type color: list
    :return: OpenGl list
    """
    if lat >= 3 and lng >= 3:
        obj = _gl.glGenLists(1)
        _gl.glNewList(obj, _gl.GL_COMPILE)
        _gl.glPushMatrix()
        if color is not None:
            _gl.glColor4fv(color)
        # noinspection PyBroadException
        try:
            _glut.glutSolidTorus(minr, maxr, lat, lng)
        except:
            if not _FIGURES_ERRS[2]:
                _print_gl_error('OpenGL actual version does not support glutSolidTorus function')
            _FIGURES_ERRS[2] = True
        _gl.glPopMatrix()
        _gl.glEndList()
        return obj
    else:
        raise Exception('Latitude and longitude of the figure must be greater than 3')


def create_cube_solid(color=None):
    """
    Create a solid cube.

    :param color: Cube color
    :type color: list
    :return: OpenGL list
    """
    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    # noinspection PyBroadException
    try:
        _glut.glutSolidCube(1.0)
    except:
        if not _FIGURES_ERRS[3]:
            _print_gl_error('OpenGL actual version does not support glutSolidCube function')
        _FIGURES_ERRS[3] = True
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_pyramid(color=None):
    """
    Creates a pyramid.

    :param color: Pyramid color
    :type color: list
    :return: OpenGL list
    """
    arista = 2.0
    a = Point3(-0.5, -0.5, -0.333) * arista
    b = Point3(0.5, -0.5, -0.333) * arista
    c = Point3(0.5, 0.5, -0.333) * arista
    d = Point3(-0.5, 0.5, -0.333) * arista
    # noinspection PyArgumentEqualDefault
    e = Point3(0.0, 0.0, 0.666) * arista

    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    _gl.glBegin(_gl.GL_QUADS)
    draw_vertex_list_create_normal([d, c, b, a])
    _gl.glEnd()
    _gl.glBegin(_gl.GL_TRIANGLES)
    draw_vertex_list_create_normal([a, b, e])
    draw_vertex_list_create_normal([b, c, e])
    draw_vertex_list_create_normal([c, d, e])
    draw_vertex_list_create_normal([d, a, e])
    _gl.glEnd()
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_pyramid_textured(texture_list):
    """
    Create a textured pyramid.

    :param texture_list: Texture OpenGL list
    :return: OpenGL list
    """
    edge = 2.0
    a = Point3(-0.5, -0.5, -0.333) * edge
    b = Point3(0.5, -0.5, -0.333) * edge
    c = Point3(0.5, 0.5, -0.333) * edge
    d = Point3(-0.5, 0.5, -0.333) * edge
    # noinspection PyArgumentEqualDefault
    e = Point3(0.0, 0.0, 0.666) * edge
    t_list = [Point2(0, 0), Point2(1, 0), Point2(1, 1), Point2(0, 1)]
    t_list_face = [Point2(0, 0), Point2(0.5, 1.0), Point2(1, 0)]

    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    for _i in range(len(texture_list)):
        _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glBindTexture(_gl.GL_TEXTURE_2D, texture_list[_i])
    _gl.glBegin(_gl.GL_QUADS)
    draw_vertex_list_create_normal_textured([d, c, b, a], t_list)
    _gl.glEnd()
    _gl.glBegin(_gl.GL_TRIANGLES)
    draw_vertex_list_create_normal_textured([a, b, e], t_list_face)
    draw_vertex_list_create_normal_textured([b, c, e], t_list_face)
    draw_vertex_list_create_normal_textured([c, d, e], t_list_face)
    draw_vertex_list_create_normal_textured([d, a, e], t_list_face)
    _gl.glEnd()
    for _i in range(len(texture_list)):
        _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
        _gl.glDisable(_gl.GL_TEXTURE_2D)
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_diamond(color=None):
    """
    Creates a diamond.

    :param color: Diamond color
    :type color: list
    :return: OpenGL list
    """
    # noinspection PyArgumentEqualDefault
    a = Point3(-1.0, -1.0, 0.0)
    # noinspection PyArgumentEqualDefault
    b = Point3(1.0, -1.0, 0.0)
    # noinspection PyArgumentEqualDefault
    c = Point3(1.0, 1.0, 0.0)
    # noinspection PyArgumentEqualDefault
    d = Point3(-1.0, 1.0, 0.0)
    # noinspection PyArgumentEqualDefault
    e = Point3(0.0, 0.0, 1.0)
    # noinspection PyArgumentEqualDefault
    f = Point3(0.0, 0.0, -1.0)

    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    _gl.glBegin(_gl.GL_TRIANGLES)
    draw_vertex_list_create_normal([a, b, e])
    draw_vertex_list_create_normal([b, c, e])
    draw_vertex_list_create_normal([c, d, e])
    draw_vertex_list_create_normal([d, a, e])
    draw_vertex_list_create_normal([b, a, f])
    draw_vertex_list_create_normal([c, b, f])
    draw_vertex_list_create_normal([d, c, f])
    draw_vertex_list_create_normal([a, d, f])
    _gl.glEnd()
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_teapot(color=None):
    """
    Create a OpenGL teapot.

    :param color: Object color
    :type color: list
    :return: OpenGL list
    """
    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    _gl.glRotate(90, 1, 0, 0)
    # noinspection PyBroadException
    try:
        _glut.glutSolidTeapot(1.0)
    except:
        if not _FIGURES_ERRS[4]:
            _print_gl_error('OpenGL actual version doest not support glutSolidTeapot function')
        _FIGURES_ERRS[4] = True
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_teapot_textured(texture_list):
    """
    Creates a teapot textured.

    :param texture_list: Texture OpenGL list
    :return: Object list
    """
    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    for _i in range(len(texture_list)):
        _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glBindTexture(_gl.GL_TEXTURE_2D, texture_list[_i])
    _gl.glRotate(90, 1, 0, 0)
    # noinspection PyBroadException
    try:
        _glut.glutSolidTeapot(1.0)
    except:
        if not _FIGURES_ERRS[4]:
            _print_gl_error('OpenGL actual version does not support glutSolidTeapot function')
        _FIGURES_ERRS[4] = True
    for _i in range(len(texture_list)):
        _gl.glActiveTexture(_gl.GL_TEXTURE0 + _i)
        _gl.glDisable(_gl.GL_TEXTURE_2D)
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_pyramid_vbo(edge=1.0):
    """
    Creates a VBO pyramid for shaders.

    :param edge: Edge length
    :type edge: float, int
    :return: VBO Object
    :rtype: VBObject
    """

    def ex(element):
        """
        Export element to list.

        :param element: Element
        :return: List
        :rtype: list
        """
        return element.export_to_list()

    # Create points
    a = Point3(-0.5, -0.5, -0.333) * edge
    b = Point3(0.5, -0.5, -0.333) * edge
    c = Point3(0.5, 0.5, -0.333) * edge
    d = Point3(-0.5, 0.5, -0.333) * edge
    # noinspection PyArgumentEqualDefault
    e = Point3(0.0, 0.0, 0.666) * edge

    # Create normals
    n1 = ex(_normal_3_points(a, b, e))
    n2 = ex(_normal_3_points(b, c, e))
    n3 = ex(_normal_3_points(c, d, e))
    n4 = ex(_normal_3_points(d, a, e))
    n5 = ex(_normal_3_points(c, b, a))

    # Create point list
    vertex_array = [ex(b), ex(e), ex(a), ex(b), ex(c), ex(e), ex(c), ex(d),
                    ex(e), ex(d), ex(a), ex(e), ex(a), ex(b),
                    ex(c), ex(c), ex(d), ex(a)]
    normal_array = [n1, n1, n1, n2, n2, n2, n3, n3, n3, n4, n4, n4, n5, n5, n5,
                    n5, n5, n5]

    # Return VBO Object
    return VBObject(_vbo.VBO(_array(vertex_array, 'f')), _vbo.VBO(_array(normal_array, 'f')), len(vertex_array))


def create_tetrahedron_vbo(edge=1.0):
    """
    Creates a VBO tetrahedron for shaders.

    :param edge: Edge length
    :type edge: float, int
    :return: VBO object
    :rtype: VBObject
    """

    def ex(element):
        """
        Export element to list.

        :param element: Element
        :return: List
        :rtype: list
        """
        return element.export_to_list()

    # Create points
    a = Point3(-0.5, -0.288675, -0.288675) * edge
    b = Point3(0.5, -0.288675, -0.288675) * edge
    # noinspection PyArgumentEqualDefault
    c = Point3(0.0, 0.577350, -0.288675) * edge
    # noinspection PyArgumentEqualDefault
    d = Point3(0.0, 0.0, 0.57735) * edge

    # Create normals
    n1 = ex(_normal_3_points(a, b, d))
    n2 = ex(_normal_3_points(b, c, d))
    n3 = ex(_normal_3_points(c, a, d))
    n4 = ex(_normal_3_points(c, b, a))

    # Create triangles
    vertex_array = [ex(a), ex(b), ex(d), ex(b), ex(c), ex(d), ex(c), ex(a),
                    ex(d), ex(a), ex(b), ex(c)]
    normal_array = [n1, n1, n1, n2, n2, n2, n3, n3, n3, n4, n4, n4]

    # Return VBO
    return VBObject(_vbo.VBO(_array(vertex_array, 'f')), _vbo.VBO(_array(normal_array, 'f')),
                    len(vertex_array))


def create_tetrahedron(color=None):
    """
    Creates a tetrahedron.

    :param color: Tetrahedron color
    :type color: list
    :return: OpenGL list
    """
    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    # noinspection PyBroadException
    try:
        _glut.glutSolidTetrahedron()
    except:
        if not _FIGURES_ERRS[5]:
            _print_gl_error('OpenGL actual version does not support glutSolidTetrahedron function')
        _FIGURES_ERRS[5] = True
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_dodecahedron(color=None):
    """
    Creates a dodecahedron.

    :param color: Dodecahedron color
    :type color: list
    :return: OpenGL list
    """
    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    # noinspection PyBroadException
    try:
        _glut.glutSolidDodecahedron()
    except:
        if not _FIGURES_ERRS[6]:
            _print_gl_error('OpenGL actual version dost not support glutSolidDodecahedron function')
        _FIGURES_ERRS[6] = True
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_octahedron(color=None):
    """
    Crates an octahedron.

    :param color: Octahedron color
    :type color: list
    :return: OpenGL list
    """
    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    # noinspection PyBroadException
    try:
        _glut.glutSolidOctahedron()
    except:
        if not _FIGURES_ERRS[7]:
            _print_gl_error('OpenGL actual version does not support glutSolidOctahedron function')
        _FIGURES_ERRS[7] = True
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj


def create_icosahedron(color=None):
    """
    Creates an icosahedron.

    :param color: Icosahedron color
    :type color: list
    :return: OpenGL list
    """
    obj = _gl.glGenLists(1)
    _gl.glNewList(obj, _gl.GL_COMPILE)
    _gl.glPushMatrix()
    if color is not None:
        _gl.glColor4fv(color)
    # noinspection PyBroadException
    try:
        _glut.glutSolidIcosahedron()
    except:
        if not _FIGURES_ERRS[8]:
            _print_gl_error('OpenGL actual version does not support glutSolidIcosahedron function')
        _FIGURES_ERRS[8] = True
    _gl.glPopMatrix()
    _gl.glEndList()
    return obj
