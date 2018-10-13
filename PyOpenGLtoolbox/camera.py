# coding=utf-8
"""
PYOPENGL-TOOLBOX CAMERA
Camera classes.

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
from OpenGL.GL import glLoadIdentity
from OpenGL.GLU import gluLookAt
from PyOpenGLtoolbox.utils_math import Point3, Vector3, _cos, _sin, _xyz_to_spr, _spr_to_xyz
import math as _math

# Constants
_CAMERA_CENTER_LIMIT_Z_DOWN = -3500
_CAMERA_CENTER_LIMIT_Z_UP = 3500
_CAMERA_CENTER_VEL = 1
_CAMERA_DEFAULT_RVEL = 1
_CAMERA_MIN_RADIAL_VALUE = 0.000001
_CAMERA_MIN_THETA_VALUE = 0.000001
_CAMERA_NEGATIVE = -1.0
_CAMERA_POSITIVE = 1.0
_CAMERA_ROUNDED = 2
_CAMERA_SPHERICAL = 0x0fb
_CAMERA_XYZ = 0x0fa


class _Camera:
    """
    Abstract camera class.
    """

    def __init__(self):
        """
        Void constructor.
        """
        pass

    def place(self):
        """
        Place camera in world.

        :return:
        """
        pass

    def move_x(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to x-position.

        :param direction: X-axis position
        :type direction: float, int
        :return:
        """
        pass

    def move_y(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to y-position.

        :param direction: Y-axis position
        :type direction: float, int
        :return:
        """
        pass

    def move_z(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to z-position.

        :param direction: Z-axis position
        :type direction: float, int
        :return:
        """
        pass

    def set_vel_move_x(self, vel):
        """
        Defines x-axis movement velocity.

        :param vel: X-axis velocity
        :type vel: float, int
        :return:
        """
        pass

    def set_vel_move_y(self, vel):
        """
        Defines y-axis movement velocity.

        :param vel: Y-axis velocity
        :type vel: float, int
        :return:
        """
        pass

    def set_vel_move_z(self, vel):
        """
        Defines z-axis movement velocity.

        :param vel: Z-axis velocity
        :type vel: float, int
        :return:
        """
        pass

    def set_center_vel(self, vel):
        """
        Defines center movement velocity.

        :param vel: Center velocity
        :type vel: float, int
        :return:
        """
        pass

    def move_center_x(self, dist):
        """
        Moves center x coordinate.

        :param dist: X-distance
        :type dist: float, int
        :return:
        """
        pass

    def move_center_y(self, dist):
        """
        Moves center y coordinate.

        :param dist: Y-distance
        :type dist: float, int
        :return:
        """
        pass

    def move_center_z(self, dist):
        """
        Moves center z coordinate.

        :param dist: Z-distance
        :type dist: float, int
        :return:
        """
        pass

    def rotate_center_z(self, angle):
        """
        Rotate center around z.

        :param angle: Rotation angle
        :type angle: float, int
        :return:
        """
        pass

    def far(self):
        """
        Camera zoom-out.

        :return:
        """
        pass

    def close(self):
        """
        Camera zoom-in.

        :return:
        """
        pass

    def set_r_vel(self, vel):
        """
        Defines radial velocity.

        :param vel: Velocity
        :type vel: float, int
        :return:
        """
        pass

    def rotate_x(self, angle):
        """
        Rotate eye position in x-axis.

        :param angle: Rotation angle
        :type angle: float, int
        :return:
        """
        pass

    def rotate_y(self, angle):
        """
        Rotate eye position in y-axis.

        :param angle: Rotation angle
        :type angle: float, int
        :return:
        """
        pass

    def rotate_z(self, angle):
        """
        Rotate eye position in z-axis.

        :param angle: Rotation angle
        :type angle: float, int
        :return:
        """
        pass

    def convert_to_xyz(self):
        """
        Convert spheric to cartesian.

        :return:
        """
        pass

    def __str__(self):
        """
        Return camera status.

        :return:
        """
        pass

    def get_name(self):
        """
        Returns camera name.

        :return:
        """
        pass

    def set_name(self, n):
        """
        Set camera name
        :param n: Camera name
        :return:
        """
        pass


class CameraXYZ(_Camera):
    """
    Camera in XYZ, position (x,y,z), can rotate around z.
    """

    def __init__(self, pos, center, up=Point3(0, 0, 1)):
        """
        Constructor.

        :param pos: Position
        :param center: Center coordinate
        :param up: Up vector
        :type pos: float, int
        :type center: float, int
        :type up: float, int
        """
        _Camera.__init__(self)
        if isinstance(pos, Point3) and isinstance(center, Point3) and isinstance(up, Point3):
            self.pos = Vector3(*pos.export_to_list())
            self.center = Vector3(*center.export_to_list())
            self.up = Vector3(*up.export_to_list())
        else:
            raise Exception('pos, center and up must be Point3 type')
        self._name = 'unnamed'
        self.angle = 45.0
        self.cameraVel = Vector3(1.0, 1.0, 1.0)
        self.centerangle = 0.0
        self.centervel = Vector3(_CAMERA_CENTER_VEL, _CAMERA_CENTER_VEL, _CAMERA_CENTER_VEL)
        self.viewVel = Vector3(1.0, 1.0, 1.0)

    def place(self):
        """
        Place camera in world.

        :return:
        """
        glLoadIdentity()
        gluLookAt(self.pos.get_x(), self.pos.get_y(), self.pos.get_z(),
                  self.center.get_x(), self.center.get_y(),
                  self.center.get_z(), self.up.get_x(), self.up.get_y(),
                  self.up.get_z())

    def move_x(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to x-position.

        :param direction: X-axis position
        :type direction: float, int
        :return:
        """
        self.pos.set_x(self.pos.get_x() + self.cameraVel.get_x() * direction)

    def move_y(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to y-position.

        :param direction: Y-axis position
        :type direction: float, int
        :return:
        """
        self.pos.set_y(self.pos.get_y() + self.cameraVel.get_y() * direction)

    def move_z(self, direction=_CAMERA_POSITIVE):
        """
        Moves camera to z-position.

        :param direction: Z-axis position
        :type direction: float, int
        :return:
        """
        self.pos.set_z(self.pos.get_z() + self.cameraVel.get_z() * direction)

    def set_vel_move_x(self, vel):
        """
        Defines x-axis movement velocity.

        :param vel: X-axis velocity
        :type vel: float, int
        :return:
        """
        self.cameraVel.set_x(vel)

    def set_vel_move_y(self, vel):
        """
        Defines y-axis movement velocity.

        :param vel: Y-axis velocity
        :type vel: float, int
        :return:
        """
        self.cameraVel.set_y(vel)

    def set_vel_move_z(self, vel):
        """
        Defines z-axis movement velocity.

        :param vel: Z-axis velocity
        :return:
        """
        self.cameraVel.set_z(vel)

    def set_center_vel(self, vel):
        """
        Defines center movement velocity.

        :param vel: Center velocity
        :type vel: float, int
        :return:
        """
        self.centervel = Vector3(abs(vel), abs(vel), abs(vel))

    def rotate_x(self, angle):
        """
        Rotate eye position in x-axis.

        :param angle: Rotation angle
        :type angle: float, int
        :return:
        """
        x = self.pos.get_x()
        y = self.pos.get_y() * _cos(angle) - self.pos.get_z() * _sin(angle)
        z = self.pos.get_y() * _sin(angle) + self.pos.get_z() * _cos(angle)
        self.pos.set_x(x)
        self.pos.set_y(y)
        self.pos.set_z(z)

    def rotate_y(self, angle):
        """
        Rotate eye position in y-axis.

        :param angle: Rotation angle
        :type angle: float, int
        :return:
        """
        x = self.pos.get_x() * _cos(angle) + self.pos.get_z() * _sin(angle)
        y = self.pos.get_y()
        z = -self.pos.get_x() * _sin(angle) + self.pos.get_z() * _cos(angle)
        self.pos.set_x(x)
        self.pos.set_y(y)
        self.pos.set_z(z)

    def rotate_z(self, angle):
        """
        Rotate eye position in z-axis
        :param angle: Rotation angle
        :return:
        """
        x = self.pos.get_x() * _cos(angle) - self.pos.get_y() * _sin(angle)
        y = self.pos.get_x() * _sin(angle) + self.pos.get_y() * _cos(angle)
        z = self.pos.get_z()
        self.pos.set_x(x)
        self.pos.set_y(y)
        self.pos.set_z(z)

    def move_center_x(self, dist):
        """
        Moves center x coordinate
        :param dist: X-distance
        :return:
        """
        self.center.set_x(self.center.get_x() + dist)

    def move_center_y(self, dist):
        """
        Moves center y coordinate
        :param dist: Y-distance
        :return:
        """
        self.center.set_y(self.center.get_y() + dist)

    def move_center_z(self, dist):
        """
        Moves center z coordinate
        :param dist: Z-distance
        :return:
        """
        if (_CAMERA_CENTER_LIMIT_Z_DOWN <= self.center.get_z() and dist < 0) or \
                (self.center.get_z() <= _CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self.center.set_z(self.center.get_z() + dist)

    def rotate_center_z(self, angle):
        """
        Rotate center around z
        :param angle: Rotation angle
        :return:
        """
        rad = _math.sqrt(self.pos.get_x() ** 2 + self.pos.get_y() ** 2)
        self.pos.set_x(rad * _cos(self.angle))
        self.pos.set_y(rad * _sin(self.angle))

    def far(self):
        """
        Camera zoom-out
        :return:
        """
        self.center += self.centervel

    def close(self):
        """
        Camera zoom-in
        :return:
        """
        self.center -= self.centervel

    def get_name(self):
        """Retorna el nombre de la cámara"""
        return self._name

    # noinspection PyShadowingNames
    def set_name(self, name):
        """
        Set camera name
        :param name: Camera name
        :return:
        """
        self._name = name


class CameraR(_Camera):
    """
    Camera in spheric coordinates
    """

    def __init__(self, r=1.0, phi=45, theta=45, center_point=Point3(),
                 up_vector=Vector3(0, 0, 1)):
        """
        Constructor
        :param r: Radius
        :param phi: Phi angle
        :param theta: Theta angle
        :param center_point: Center point
        :param up_vector: Up vector
        """
        _Camera.__init__(self)
        if isinstance(center_point, Point3):
            if isinstance(up_vector, Vector3):
                if r > 0:
                    if 0 <= phi <= 360 and 0 <= theta <= 180:
                        self.r = r
                        self.phi = phi
                        self.theta = theta
                        self.center = center_point
                        self.up = up_vector
                        self.rvel = _CAMERA_DEFAULT_RVEL
                        self._name = 'unnamed'
                    else:
                        raise Exception('Phi angle must be between 0 and 360 degrees, theta must be between 0 and 180')
                else:
                    raise Exception('Radius must be greater than zero')
            else:
                raise Exception('up_vector must be Vector3 type')
        else:
            raise Exception('center_point must be Point3 type')

    def set_r_vel(self, vel):
        """
        Defines radial velocity
        :param vel: Velocity
        :return:
        """
        if vel > 0:
            self.rvel = vel
        else:
            raise Exception('Velocity must be greater than zero')

    def place(self):
        """
        Place camera in world
        :return:
        """
        glLoadIdentity()
        gluLookAt(self.r * _sin(self.theta) * _cos(self.phi),
                  self.r * _sin(self.theta) * _sin(self.phi),
                  self.r * _cos(self.theta),
                  self.center.get_x(), self.center.get_y(), self.center.get_z(),
                  self.up.get_x(), self.up.get_y(),
                  self.up.get_z())

    def __str__(self):
        """Retorna el estado de la camara"""
        x, y, z = self.convert_to_xyz()
        r = _CAMERA_ROUNDED
        msg = 'Camera: {12}\nRadius: {0}\nPhi angle: {1}, Theta angle: {2}\nXYZ eye pos: ({3},{4},{5})\nXYZ center ' \
              'pos: ({6},{7},{8})\nXYZ up vector: ({9},{10},{11})'
        return msg.format(round(self.r, r), round(self.phi, r),
                          round(self.theta, r), round(x, r), round(y, r),
                          round(z, r), round(self.center.get_x(), r),
                          round(self.center.get_y(), r),
                          round(self.center.get_z(), r),
                          round(self.up.get_x(), r), round(self.up.get_y(), r),
                          round(self.up.get_z(), r), self.get_name())

    def far(self):
        """
        Camera zoom-out
        :return:
        """
        self.r += self.rvel

    def close(self):
        """
        Camera zoom-in
        :return:
        """
        self.r -= self.rvel
        self.r = max(_CAMERA_MIN_RADIAL_VALUE, self.r)

    def rotate_x(self, angle):
        """
        Rotate eye position in x-axis
        :param angle: Rotation angle
        :return:
        """
        # Converts to (x,y,z)
        x, y, z = self.convert_to_xyz()
        # Rotate (x,y,z) by x
        xr = x
        yr = y * _cos(angle) - z * _sin(angle)
        zr = y * _sin(angle) + z * _cos(angle)
        # Convert to spheric
        r, phi, theta = _xyz_to_spr(xr, yr, zr)
        self.r = r
        self.phi = phi
        self.theta = theta

    def rotate_y(self, angle):
        """
        Rotate eye position in y-axis
        :param angle: Rotation angle
        :return:
        """
        self.theta = min(max(self.theta + angle, _CAMERA_MIN_THETA_VALUE), 180)

    def rotate_z(self, angle):
        """
        Rotate eye position in z-axis
        :param angle: Rotation angle
        :return:
        """
        self.phi = (self.phi + angle) % 360

    def convert_to_xyz(self):
        """
        Convert spheric to cartesian
        :return:
        """
        return _spr_to_xyz(self.r, self.phi, self.theta)

    def move_center_x(self, dist):
        """
        Moves center x coordinate
        :param dist: X-distance
        :return:
        """
        self.center.set_x(self.center.get_x() + dist)

    def move_center_y(self, dist):
        """
        Moves center y coordinate
        :param dist: Y-distance
        :return:
        """
        self.center.set_y(self.center.get_y() + dist)

    def move_center_z(self, dist):
        """
        Moves center z coordinate
        :param dist: Z-distance
        :return:
        """
        if (_CAMERA_CENTER_LIMIT_Z_DOWN <= self.center.get_z() and dist < 0) or \
                (self.center.get_z() <= _CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self.center.set_z(self.center.get_z() + dist)

    def get_name(self):
        """
        Returns camera name
        :return:
        """
        return self._name

    # noinspection PyShadowingNames
    def set_name(self, name):
        """
        Set camera name
        :param name: Camera name
        :return:
        """
        self._name = name

    def get_radius(self):
        """
        Get camera radius
        :return:
        """
        return self.r

    def set_radius(self, r):
        """
        Set camera radius
        :param r: Camera radius
        :return:
        """
        self.r = r

    def get_phi(self):
        """
        Get camera phi
        :return: Phi angle
        """
        return self.phi

    def set_phi(self, phi):
        """
        Set camera phi
        :param phi: Phi angle
        :return:
        """
        """Define el angulo phi"""
        self.phi = phi

    def get_theta(self):
        """
        Returns theta angle
        :return: Theta angle
        """
        return self.theta

    def set_theta(self, theta):
        """
        Set theta angle
        :param theta: Theta angle
        :return:
        """
        self.theta = theta