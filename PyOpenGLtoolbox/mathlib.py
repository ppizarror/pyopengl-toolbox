# coding=utf-8
"""
PYOPENGL-TOOLBOX MATH
Utilitary math tools.

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
import math as _math
import sys as _sys

# Constants
_UTILS_MATH_POINT_2 = 'util-point-2'
_UTILS_MATH_POINT_3 = 'util-point-3'


class Point3:
    """
    Point with 3 components.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """
        Constructor.

        :param x: X-coordinate
        :param y: Y-coordinate
        :param z: Z-coordinate
        :type x: float, int, hex, oct, complex
        :type y: float, int, hex, oct, complex
        :type z: float, int, hex, oct, complex
        """
        self._point = Vector3(x, y, z)
        self._type = _UTILS_MATH_POINT_3

    def get_type(self):
        """
        Get point type.

        :return: Point type
        :rtype: string
        """
        return self._type

    def get_x(self):
        """
        Return x-coordinate.

        :return: X-coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self._point.get_x()

    def get_y(self):
        """
        Return y-coordinate.

        :return: y-coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self._point.get_y()

    def get_z(self):
        """
        Return z-coordinate.

        :return: z-coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self._point.get_z()

    def set_x(self, value):
        """
        Set x-value of the point.

        :param value: Value
        :type value: float, int, hex, oct, complex
        """
        self._point.set_x(value)

    def set_y(self, value):
        """
        Set y-value of the point.

        :param value: Value
        :type value: float, int, hex, oct, complex
        """
        self._point.set_y(value)

    def set_z(self, value):
        """
        Set z-value of the point.

        :param value: Value
        :type value: float, int, hex, oct, complex
        """
        self._point.set_z(value)

    def export_to_list(self):
        """
        Export point to list.

        :return: List
        :rtype: list
        """
        return [self._point.get_x(), self._point.get_y(), self._point.get_z()]

    def export_to_tuple(self):
        """
        Export point to tuple.

        :return: Tuple
        :rtype: tuple
        """
        return self._point.get_x(), self._point.get_y(), self._point.get_z()

    def normalize(self):
        """
        Normalize the point.
        """
        self._point.normalize()

    def echo(self, mantise=1):
        """
        Print the point.

        :param mantise: Point mantise
        :type mantise: int
        """
        self._point.echo(mantise, point3=True)

    def __add__(self, other):
        """
        Divide point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        return self._vec_to_point(self._point.__add__(self._point_to_vec(other)))

    def __sub__(self, other):
        """
        Substract point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        return self._vec_to_point(self._point.__sub__(self._point_to_vec(other)))

    def __mul__(self, other):
        """
        Multiply point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        return self._vec_to_point(self._point.__mul__(self._point_to_vec(other)))

    def __str__(self, mantise=1, **kwargs):
        """
        Return string value of the point.

        :return: Point to string
        :rtype: basestring
        """
        return self._point.__str__(mantise, point3=True)

    def __div__(self, other):
        """
        Divide point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        return self._vec_to_point(self._point.__div__(self._point_to_vec(other)))

    def __abs__(self):
        """
        Return absolute value of the point.

        :return: Point
        """
        return self._vec_to_point(self._point.__abs__())

    # noinspection PyMethodFirstArgAssignment
    def __iadd__(self, other):
        """
        Adds point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        self = self._vec_to_point(self._point.__iadd__(other))
        return self

    # noinspection PyMethodFirstArgAssignment
    def __isub__(self, other):
        """
        Substract point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        self = self._vec_to_point(self._point.__isub__(other))
        return self

    # noinspection PyMethodFirstArgAssignment
    def __imul__(self, other):
        """
        Multiply point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        self = self._vec_to_point(self._point.__imul__(other))
        return self

    # noinspection PyMethodFirstArgAssignment
    def __idiv__(self, other):
        """
        Divide point with another.

        :param other: Other point
        :type other: Point3, Point2
        :return: Point
        """
        self = self._vec_to_point(self._point.__iadd__(other))
        return self

    @staticmethod
    def _point_to_vec(point):
        """
        Converts a point to a vector.

        :param point: Point
        :type point: Point3
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(point, Point3):
            return Vector3(point.get_x(), point.get_y(), point.get_z())
        else:
            return point

    @staticmethod
    def _vec_to_point(vec):
        """
        Converts a vector to point.

        :param vec: Vector
        :type vec: Vector3
        :return: New point
        :rtype: Point2
        """
        if isinstance(vec, Vector3):
            return Point3(vec.get_x(), vec.get_y(), vec.get_z())
        else:
            return vec


class Point2(Point3):
    """
    2-coordinates point.
    """

    def __init__(self, x=0.0, y=0.0):
        """
        Constructor.

        :param x: X-coordinate
        :param y: Y-coordinate
        :type x: float, int, hex, oct, complex
        :type y: float, int, hex, oct, complex
        """
        Point3.__init__(self, x, y)
        self._point = Vector3(x, y)
        self._type = _UTILS_MATH_POINT_2

    @staticmethod
    def _point_to_vec(point):
        """
        Converts a point to a vector.

        :param point: Point
        :type point: Point2
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(point, Point2):
            return Vector3(point.get_x(), point.get_y())
        else:
            return point

    @staticmethod
    def _vec_to_point(vec):
        """
        Converts a vector to point.

        :param vec: Vector
        :type vec: Vector3
        :return: New point
        :rtype: Point2
        """
        if isinstance(vec, Vector3):
            return Point2(vec.get_x(), vec.get_y())
        else:
            return vec

    def __str__(self, mantise=1, **kwargs):
        """
        Return point as string.

        :param mantise: Point mantise
        :param kwargs: Optional arguments
        :type mantise: int
        :type kwargs: object
        :return: Point string
        :rtype: basestring
        """
        return self._point.__str__(mantise, point2=True)

    def echo(self, mantise=1):
        """
        Print the point.

        :param mantise: Point mantise
        :type mantise: int
        """
        self._point.echo(mantise, point2=True)

    def export_to_list(self):
        """
        Export point to list.

        :return: List
        :rtype: list
        """
        return [self._point.get_x(), self._point.get_y()]

    def export_to_tuple(self):
        """
        Export point to tuple.

        :return: Tuple
        :rtype: tuple
        """
        return self._point.get_x(), self._point.get_y()


class Vector3(object):
    """
    3 component Vector.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """
        Constructor.

        :param x: X-coordinate
        :param y: Y-coordinate
        :param z: Z-coordinate
        :type x: float, int, hex, oct, complex
        :type y: float, int, hex, oct, complex
        :type z: float, int, hex, oct, complex
        """
        self.x = x
        self.y = y
        self.z = z

    def get_module(self):
        """
        Returns vector module.

        :return: Module
        :rtype: float
        """
        return self.distance_with(Vector3(0, 0, 0))

    def set_x(self, x):
        """
        Set x-coordinate.

        :param x: X-coordinate
        :type x: float, int, hex, oct, complex
        """
        self.x = x

    def set_y(self, y):
        """
        Set y-coordinate.

        :param y: Y-coordinate
        :type y: float, int, hex, oct, complex
        """
        self.y = y

    def set_z(self, z):
        """
        Set z-coordinate.

        :param z: Z-coordinate
        :type z: float, int, hex, oct, complex
        """
        self.z = z

    def get_x(self):
        """
        Get x-coordinate

        :return: Coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self.x

    def get_y(self):
        """
        Get y-coordinate

        :return: Coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self.y

    def get_z(self):
        """
        Get z-coordinate

        :return: Coordinate
        :rtype: float, int, hex, oct, complex
        """
        return self.z

    def ponderate(self, a=1.0):
        """
        Multiply vector with a number.

        :param a: Number
        :type a: float, int
        """
        if type(a) is float or type(a) is int:
            self.x *= a
            self.y *= a
            self.z *= a
        else:
            self.throw_error(2, 'ponderate')
            return self

    def __add__(self, other):
        """
        Adds vector with another.

        :param other: Vector
        :type other: Vector3, tuple, list
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            return Vector3(self.x + other.get_x(), self.y + other.get_y(),
                           self.z + other.get_z())
        elif type(other) is tuple or type(other) is list:
            if len(other) == 3:
                return Vector3(self.x + other[0], self.y + other[1],
                               self.z + other[2])
        else:
            self.throw_error(2, '__add__')
            return self

    def __sub__(self, other):
        """
        Substract vector with another.

        :param other: Vector
        :type other: Vector3, tuple, list
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            return Vector3(self.x - other.get_x(), self.y - other.get_y(),
                           self.z - other.get_z())
        elif type(other) is tuple or type(other) is list:
            if len(other) == 3:
                return Vector3(self.x - other[0], self.y - other[1],
                               self.z - other[2])
        else:
            self.throw_error(2, '__sub__')
            return self

    def __mod__(self, other):
        """
        Return module value.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(self.x % other.get_x(), self.y % other.get_y(),
                       self.z % other.get_z())

    def __mul__(self, other):
        """
        Multiply vector with another.

        :param other: Vector or value
        :type other: Vector3, int, float, hex, complex, oct
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            return Vector3(self.x * other.get_x(), self.y * other.get_y(),
                           self.z * other.get_z())
        else:
            if type(other) is list or type(other) is tuple:
                return Vector3(self.x * other[0], self.y * other[1],
                               self.z * other[2])
            elif type(other) is int or type(other) is float:
                return Vector3(self.x * other, self.y * other, self.z * other)
            else:
                self.throw_error(2, '__mul__')
                return self

    def __abs__(self):
        """
        Return absolute value.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __div__(self, other):
        """
        Divide vector with another.

        :param other: Vector or value
        :type other: Vector3, int, float, hex, complex, oct
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            return Vector3(self.x / other.get_x(), self.y / other.get_y(),
                           self.z / other.get_z())
        else:
            if type(other) is int or type(other) is float or type(other) is hex or type(other) is complex or type(
                    other) is oct:
                return Vector3(self.x / other, self.y / other, self.z / other)
            else:
                self.throw_error(2, '__div__')
                return self

    def __invert__(self, other):
        """
        Apply positive sign to vector.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(-self.x, -self.y, -self.z)

    def __neg__(self):
        """
        Apply negative sign to vector.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(-self.x, -self.y, -self.z)

    def __pos__(self):
        """
        Apply positive sign to vector.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(self.x, self.y, self.z)

    def __and__(self, other):
        """
        Logic AND operator.

        :param other: Vector
        :type other: Vector3
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            if self.x > 0 and other.get_x() > 0:
                x = 1
            else:
                x = 0
            if self.y > 0 and other.get_y() > 0:
                y = 1
            else:
                y = 0
            if self.z > 0 and other.get_z() > 0:
                z = 1
            else:
                z = 0
            return Vector3(x, y, z)
        else:
            self.throw_error(2, '__and__')
            return Vector3()

    def __or__(self, other):
        """
        Logic OR operator.

        :param other: Vector
        :type other: Vector3
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            if self.x > 0 or other.get_x() > 0:
                x = 1
            else:
                x = 0
            if self.y > 0 or other.get_y() > 0:
                y = 1
            else:
                y = 0
            if self.z > 0 or other.get_z() > 0:
                z = 1
            else:
                z = 0
            return Vector3(x, y, z)
        else:
            self.throw_error(2, '__or__')
            return Vector3()

    def normalize(self):
        """
        Normalize the vector.
        """
        modl = self.get_module()
        self.x /= modl
        self.y /= modl
        self.z /= modl

    def get_normalized(self):
        """
        Generates normalized vector.

        :return: New vector
        :rtype: Vector3
        """
        modl = self.get_module()
        return Vector3(self.x / modl, self.y / modl, self.z / modl)

    def clone(self):
        """
        Clones vector.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(self.x, self.y, self.z)

    def __int__(self):
        """
        Generates int vector.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(int(self.x), int(self.y), int(self.z))

    def __float__(self):
        """
        Generates float vector.

        :return: New vector
        :rtype: Vector3
        """
        return Vector3(float(self.x), float(self.y), float(self.z))

    def __complex__(self):
        """
        Generates complex vector.

        :return: New vector
        :rtype: Vector3
        """
        # noinspection PyTypeChecker
        return Vector3(complex(self.x), complex(self.y), complex(self.z))

    def __hex__(self):
        """
        Generates hex vector.

        :return: New vector
        :rtype: Vector3
        """
        # noinspection PyTypeChecker
        return Vector3(hex(self.x), hex(self.y), hex(self.z))

    def __oct__(self):
        """
        Generates oct vector.

        :return: New vector
        :rtype: Vector3
        """
        # noinspection PyTypeChecker
        return Vector3(oct(self.x), oct(self.y), oct(self.z))

    def __iadd__(self, other):
        """
        Add with another vector.

        :param other: Vector
        :type other: Vector3, list, tuple
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            self.x += other.get_x()
            self.y += other.get_y()
            self.z += other.get_z()
            return self
        elif type(other) is tuple or type(other) is list:
            if len(other) == 3:
                self.x += other[0]
                self.y += other[1]
                self.z += other[2]
                return self
        else:
            self.throw_error(2, '__iadd__')
            return self

    def __isub__(self, other):
        """
        Substract with another vector.

        :param other: Vector
        :type other: Vector3, list, tuple
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            self.x -= other.get_x()
            self.y -= other.get_y()
            self.z -= other.get_z()
            return self
        elif type(other) is tuple or type(other) is list:
            if len(other) == 3:
                self.x -= other[0]
                self.y -= other[1]
                self.z -= other[2]
                return self
        else:
            self.throw_error(2, '__isub__')
            return self

    def __imul__(self, other):
        """
        Multiplication with another vector.

        :param other: Vector
        :type other: Vector3, list, tuple
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            self.x *= other.get_x()
            self.y *= other.get_y()
            self.z *= other.get_z()
            return self
        else:
            if type(other) is list or type(other) is tuple:
                self.x *= other[0]
                self.y *= other[1]
                self.z *= other[2]
                return self
            elif type(other) is int or type(other) is float:
                self.x *= other
                self.y *= other
                self.z *= other
                return self
            else:
                self.throw_error(2, '__imul__')
                return self

    def __idiv__(self, other):
        """
        Division with another vector.

        :param other: Vector
        :type other: Vector3, list, tuple
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            self.x /= other.get_x()
            self.y /= other.get_y()
            self.z /= other.get_z()
            return self
        else:
            if type(other) is list or type(other) is tuple:
                self.x /= other[0]
                self.y /= other[1]
                self.z /= other[2]
                return self
            elif type(other) is int or type(other) is float:
                self.x /= other
                self.y /= other
                self.z /= other
                return self
            else:
                self.throw_error(2, '__idiv__')
                return self

    @staticmethod
    def throw_error(err_num, err_func):
        """
        Print error to console.

        :param err_num: Error code
        :param err_func: Error name function
        :type err_num: int
        :type err_func: basestring
        """

        def _print_error(error):
            print('{0} ~ {1}'.format(error, err_func), file=_sys.stderr)

        if err_num == 1:
            _print_error('Mantise less than 1')
        elif err_num == 2:
            _print_error('Invalid type')

    def echo(self, mantise=1, **kwargs):
        """
        Prints vector to console.

        :param mantise: Mantise
        :param kwargs: Optional parameters
        :type mantise: int
        :type kwargs: object
        """
        print(self.__str__(mantise, **kwargs))

    def dot(self, other):
        """
        Return new vector from dot operation.

        :param other: Vector
        :type other: Vector3
        :return: New vector
        :rtype: Vector3
        """
        return self.__mul__(other)

    def dotwith(self, other):
        """
        Dot operation, save to object.

        :param other: Vector
        :type other: Vector3
        """
        dot = self.dot(other)
        self.x = dot.get_x()
        self.y = dot.get_y()
        self.z = dot.get_z()

    def cross(self, other):
        """
        Return new vector from cross operation.

        :param other: Vector
        :type other: Vector3, tuple, list
        :return: New vector
        :rtype: Vector3
        """
        if isinstance(other, Vector3):
            i = self.y * other.get_z() - self.z * other.get_y()
            j = self.z * other.get_x() - self.x * other.get_z()
            k = self.x * other.get_y() - self.y * other.get_x()
            return Vector3(i, j, k)
        elif type(other) is tuple or type(other) is list:
            return self.cross(Vector3(*other))
        else:
            self.throw_error(2, 'cross')
            return self

    def crosswith(self, other):
        """
        Cross operation, save to object.

        :param other: Vector
        :type other: Vector3
        """
        cross = self.cross(other)
        self.x = cross.get_x()
        self.y = cross.get_y()
        self.z = cross.get_z()

    def distance_with(self, other):
        """
        Return distance from another vector.

        :param other: Vector
        :type other: Vector3, tuple, list
        :return: Distance
        :rtype: float
        """
        if isinstance(other, Vector3):
            return _math.sqrt(
                (self.x - other.get_x()) ** 2 + (self.y - other.get_y()) ** 2 + (self.z - other.get_y()) ** 2)
        elif type(other) is list or type(other) is tuple:
            return self.distance_with(Vector3(*other))
        else:
            self.throw_error(2, 'distance')
            return 0.0

    def __str__(self, mantise=1, **kwargs):
        """
        Display point as string.

        :param mantise: Point mantise
        :param kwargs: Optional parameters
        :type mantise: int
        :type kwargs: object
        :return: Point as string
        :rtype: basestring
        """
        if mantise >= 1:
            if kwargs.get('formatted'):
                _format = '/{0}\\\n|{1}|\n\\{2}/'
            else:
                _format = '[{0},{1},{2}]'
            if kwargs.get('point3'):
                _format = '({0},{1},{2})'
            if kwargs.get('point2'):
                _format = '({0},{1})'
            return _format.format(round(self.x, mantise),
                                  round(self.y, mantise),
                                  round(self.z, mantise))
        else:
            self.throw_error(1, 'echo')

    def export_to_list(self):
        """
        Export vector to list.

        :return: List containing coordinates
        :rtype: list
        """
        return [self.x, self.y, self.z]

    def export_to_tuple(self):
        """
        Export vector to tuple.

        :return: Tuple containing coordinates
        :rtype: tuple
        """
        return self.x, self.y, self.z


def _normal_3_points(a, b, c):
    """
    Return normal vector from 3 points.

    :param a: Point a
    :param b: Point b
    :param c: Point c
    :type a: tuple, Point3
    :type b: tuple, Point3
    :type c: tuple, Point3
    :return: Normal vector
    :rtype: Vector3
    """
    if type(a) is list or type(a) is tuple:
        a = Vector3(*a)
        b = Vector3(*b)
        c = Vector3(*c)
    elif isinstance(a, Point3):
        a = Vector3(*a.export_to_list())
        b = Vector3(*b.export_to_list())
        c = Vector3(*c.export_to_list())
    cross_result = (a - c).cross(b - c).get_normalized()
    if cross_result.get_x() == -0.0:
        cross_result.set_x(0.0)
    if cross_result.get_y() == -0.0:
        cross_result.set_y(0.0)
    if cross_result.get_z() == -0.0:
        cross_result.set_z(0.0)
    return cross_result


def _cos(angle):
    """
    Return cosine of the angle (in radians).

    :param angle: Angle in radians
    :type angle: float, int
    :return: Cosine value
    :rtype: float
    """
    return _math.cos(_math.radians(angle))


def _sin(angle):
    """
    Return sine of the angle (in radians).

    :param angle: Angle in radians
    :type angle: float, int
    :return: Sine value
    :rtype: float
    """
    return _math.sin(_math.radians(angle))


def _sgn(x):
    """
    Returns sign(x).

    :param x: Number
    :type x: float, int
    :return: 1, 0, -1
    :rtype: int
    """
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def _spr_to_xyz(r, phi, theta):
    """
    Convertes spheric coordinates to (x,y,z).

    :param r: Radius
    :param phi: Phi angle
    :param theta: Theta angle
    :type r: float, int
    :type phi: float, int
    :type theta: float, int
    :return: (x,y,z) tuple
    :rtype: tuple
    """
    x = r * _sin(theta) * _cos(phi)
    y = r * _sin(theta) * _sin(phi)
    z = r * _cos(theta)
    return x, y, z


def _xyz_to_spr(x, y, z):
    """
    Converts cartesian coordinates (x,y,z) to spheric coordinates (r,phi,theta) in sexagesimal angles.

    :param x: X-coordinate
    :param y: Y-coordinate
    :param z: Z-coordinate
    :type x: float, int
    :type y: float, int
    :type z: float, int
    :return: (r,phi,theta) coordinates
    :rtype: tuple
    """

    # Radius
    r = _math.sqrt(x ** 2 + y ** 2 + z ** 2)

    # Theta
    if z > 0:
        theta = _math.atan(_math.sqrt(x ** 2 + y ** 2) / z)
    elif z == 0:
        theta = _math.pi / 2
    else:
        theta = _math.pi + _math.atan(_math.sqrt(x ** 2 + y ** 2) / z)

    # Calculate phi angle
    if x > 0:
        if y > 0:
            phi = _math.atan(y / x)
        else:
            phi = 2 * _math.pi + _math.atan(y / x)
    elif x == 0:
        phi = _sgn(y) * _math.pi / 2
    else:
        phi = _math.pi + _math.atan(y / x)
    theta = _math.degrees(theta)
    phi = _math.degrees(phi) % 360
    theta = min(max(theta, 0.000001), 180)

    # Return tuple
    return r, phi, theta
