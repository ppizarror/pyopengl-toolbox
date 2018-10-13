# coding=utf-8
"""
PYOPENGL-TOOLBOX PARTICLES
Particle class.

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
from PyOpenGLtoolbox.mathlib import _cos, _sin, Point3, Vector3
import types as _types

# Constants
PARTICLES_OPERATOR_ADD = 0x0f60
PARTICLES_OPERATOR_AND = 0x0f61
PARTICLES_OPERATOR_DIFF = 0x0f62
PARTICLES_OPERATOR_DIV = 0x0f63
PARTICLES_OPERATOR_MOD = 0x0f64
PARTICLES_OPERATOR_MULT = 0x0f65
PARTICLES_OPERATOR_OR = 0x0f66
PARTICLES_OPERATOR_POW = 0x0f67
PARTICLES_OPERATOR_XOR = 0x0f68
_PARTICLES_ROUND = 3


class Particle:
    """
    Particle.
    """

    def __init__(self, posx=0.0, posy=0.0, posz=0.0):
        """
        Constructor.

        :param posx: X-position
        :param posy: Y-position
        :param posz: Z-position
        :type posx: float, int
        :type posy: float, int
        :type posz: float, int
        """
        self._name = 'unnamed'
        self._angvel = Vector3()  # Angular velocity
        self._boolrot = [False, False, False]
        self._boolvel = [False, False, False]
        self._functionArguments = []
        self._functions = []
        self._functionUpdate = []
        self._position = Point3(posx, posy, posz)
        self._posVel = Vector3()  # Velocity
        self._properties = {}

    def set_x(self, x):
        """
        Modify x-position of the particle.

        :param x: X-position
        :type x: float, int
        """
        self._position.set_x(x)

    def set_y(self, y):
        """
        Modify y-position of the particle.

        :param y: Y-position
        :type y: float, int
        """
        self._position.set_y(y)

    def set_z(self, z):
        """
        Modify z-position of the particle.

        :param z: Z-position
        :type z: float, int
        """
        self._position.set_z(z)

    def get_x(self):
        """
        Get the x-coordinate of the particle.

        :return: X-coordinate
        :rtype: float, int
        """
        return self._position.get_x()

    def get_y(self):
        """
        Get the y-coordinate of the particle.

        :return: Y-coordinate
        :rtype: float, int
        """
        return self._position.get_y()

    def get_z(self):
        """
        Get the z-coordinate of the particle.

        :return: Z-coordinate
        :rtype: float, int
        """
        return self._position.get_z()

    def rotate_x(self, ang):
        """
        Rotates the particle by <ang> grades in x-axis.

        :param ang: Rotation angle
        :type ang: float, int
        """
        if ang != 0.0:
            x = self.get_x()
            y = self.get_y() * _cos(ang) - self.get_z() * _sin(ang)
            z = self.get_y() * _sin(ang) + self.get_z() * _cos(ang)
            self.set_x(x)
            self.set_y(y)
            self.set_z(z)

    def rotate_y(self, ang):
        """
        Rotates the particle by <ang> grades in y-axis.

        :param ang: Rotation angle
        :type ang: float, int
        """
        if ang != 0.0:
            x = self.get_x() * _cos(ang) + self.get_z() * _sin(ang)
            y = self.get_y()
            z = -self.get_x() * _sin(ang) + self.get_z() * _cos(ang)
            self.set_x(x)
            self.set_y(y)
            self.set_z(z)

    def rotate_z(self, ang):
        """
        Rotates the particle by <ang> grades in z-axis.

        :param ang: Rotation angle
        :type ang: float, int
        """
        if ang != 0.0:
            x = self.get_x() * _cos(ang) - self.get_y() * _sin(ang)
            y = self.get_x() * _sin(ang) + self.get_y() * _cos(ang)
            z = self.get_z()
            self.set_x(x)
            self.set_y(y)
            self.set_z(z)

    def get_position_list(self):
        """
        Return position list.

        :return: Position
        :rtype: list
        """
        return self._position.export_to_list()

    def get_position_tuple(self):
        """
        Get position tuple.

        :return: Position
        :rtype: tuple
        """
        return self._position.export_to_tuple()

    def set_ang_vel(self, velx=0.0, vely=0.0, velz=0.0):
        """
        Set angular velocity of the particle in all axis.

        :param velx: Angular velocity in x-axis
        :param vely: Angular velocity in y-axis
        :param velz: Angular velocity in z-axis
        :type velx: float, int
        :type vely: float, int
        :type velz: float, int
        """
        self.set_ang_vel_x(velx)
        self.set_ang_vel_y(vely)
        self.set_ang_vel_z(velz)

    def set_ang_vel_x(self, angvel, enable_movement=False):
        """
        Set angular velocity in x-axis.

        :param angvel: X-axis angular velocity
        :param enable_movement: Starts movement in x-axis
        :type angvel: float, int
        :type enable_movement: bool
        """
        self._angvel.set_x(angvel)
        if enable_movement:
            self.start_ang_movement_x()

    def set_ang_vel_y(self, angvel, enable_movement=False):
        """
        Set angular velocity in y-axis.

        :param angvel: Y-axis angular velocity
        :param enable_movement: Starts movement in y-axis
        :type angvel: float, int
        :type enable_movement: bool
        """
        self._angvel.set_y(angvel)
        if enable_movement:
            self.start_ang_movement_y()

    def set_ang_vel_z(self, angvel, enable_movement=False):
        """
        Set angular velocity in z-axis.

        :param angvel: Z-axis angular velocity
        :param enable_movement: Starts movement in z-axis
        :type angvel: float, int
        :type enable_movement: bool
        """
        self._angvel.set_z(angvel)
        if enable_movement:
            self.start_ang_movement_z()

    def get_ang_vel_x(self):
        """
        Returns angular velocity in x-axis.

        :return: Angular velocity
        :rtype: float, int
        """
        return self._angvel.get_x()

    def get_ang_vel_y(self):
        """
        Returns angular velocity in x-axis.

        :return: Angular velocity
        :rtype: float, int
        """
        return self._angvel.get_y()

    def get_ang_vel_z(self):
        """
        Returns angular velocity in x-axis.

        :return: Angular velocity
        :rtype: float, int
        """
        return self._angvel.get_z()

    def start_ang_movement_all(self):
        """
        Enable all angular movement.
        """
        self.start_ang_movement_x()
        self.start_ang_movement_y()
        self.start_ang_movement_z()

    def stop_ang_movement_all(self):
        """
        Stop angular movement.
        """
        self.stop_ang_movement_x()
        self.stop_ang_movement_y()
        self.stop_ang_movement_z()

    def start_ang_movement_x(self):
        """
        Start angular movement in x-axis.
        """
        self._boolrot[0] = True

    def stop_ang_movement_x(self):
        """
        Stop angular movement in x-axis.
        """
        self._boolrot[0] = False

    def start_ang_movement_y(self):
        """
        Start angular movement in y-axis.
        """
        self._boolrot[1] = True

    def stop_ang_movement_y(self):
        """
        Stop angular movement in y-axis.
        """
        self._boolrot[1] = False

    def start_ang_movement_z(self):
        """
        Start angular movement in z-axis.
        """
        self._boolrot[2] = True

    def stop_ang_movement_z(self):
        """
        Stop angular movement in z-axis.
        """
        self._boolrot[2] = False

    def set_vel(self, velx=0.0, vely=0.0, velz=0.0):
        """
        Set velocity of the particle in all axis.

        :param velx: Velocity in x-axis
        :param vely: Velocity in y-axis
        :param velz: Velocity in z-axis
        :type velx: float, int
        :type vely: float, int
        :type velz: float, int
        """
        self.set_vel_x(velx)
        self.set_vel_y(vely)
        self.set_vel_z(velz)

    def set_vel_x(self, vel, enable_movement=False):
        """
        Set velocity in x-axis.

        :param vel: Velocity
        :param enable_movement: Starts movement
        :type vel: float, int
        :type enable_movement: bool
        """
        self._posVel.set_x(vel)
        if enable_movement:
            self.start_movement_x()

    def set_vel_y(self, vel, enable_movement=False):
        """
        Set velocity in y-axis.

        :param vel: Velocity
        :param enable_movement: Starts movement
        :type vel: float, int
        :type enable_movement: bool
        """
        self._posVel.set_y(vel)
        if enable_movement:
            self.start_movement_y()

    def set_vel_z(self, vel, enable_movement=False):
        """
        Set velocity in z-axis.

        :param vel: Velocity
        :param enable_movement: Starts movement
        :type vel: float, int
        :type enable_movement: bool
        """
        self._posVel.set_z(vel)
        if enable_movement:
            self.start_movement_z()

    def get_vel_x(self):
        """
        Returns velocity in x-axis.

        :return: X-axis velocity
        :rtype: float, int
        """
        return self._posVel.get_x()

    def get_vel_y(self):
        """
        Returns velocity in y-axis.

        :return: Y-axis velocity
        :rtype: float, int
        """
        return self._posVel.get_y()

    def get_vel_z(self):
        """
        Returns velocity in z-axis.

        :return: Z-axis velocity
        :rtype: float, int
        """
        return self._posVel.get_z()

    def move_x(self, delta):
        """
        Moves the particle in x-axis.

        :param delta: Distance
        :type delta: float, int
        """
        self.set_x(delta + self.get_x())

    def move_y(self, delta):
        """
        Moves the particle in x-axis.

        :param delta: Distance
        :type delta: float, int
        """
        self.set_y(delta + self.get_y())

    def move_z(self, delta):
        """
        Moves the particle in x-axis.

        :param delta: Distance
        :type delta: float, int
        """
        self.set_z(delta + self.get_z())

    def start_movement_all(self):
        """
        Enables movement in all axis.
        """
        self.start_movement_x()
        self.start_movement_y()
        self.start_movement_z()

    def stop_movement_all(self):
        """
        Stop movement in all axis.
        """
        self.stop_movement_x()
        self.stop_movement_y()
        self.stop_movement_z()

    def start_movement_x(self):
        """
        Enables movement in x-axis.
        """
        self._boolvel[0] = True

    def stop_movement_x(self):
        """
        Stops movement in x-axis.
        """
        self._boolvel[0] = False

    def start_movement_y(self):
        """
        Enables movement in y-axis.
        """
        self._boolvel[1] = True

    def stop_movement_y(self):
        """
        Stops movement in y-axis.
        """
        self._boolvel[1] = False

    def start_movement_z(self):
        """
        Enables movement in z-axis.
        """
        self._boolvel[2] = True

    def stop_movement_z(self):
        """
        Stops movement in z-axis.
        """
        self._boolvel[2] = False

    def has_movement_ang_x(self):
        """
        Indicates if particle has any angular movement in x-axis.

        :return: Angular movement
        :rtype: bool
        """
        return self._boolrot[0]

    def has_movement_ang_y(self):
        """
        Indicates if particle has any angular movement in y-axis.

        :return: Angular movement
        :rtype: bool
        """
        return self._boolrot[1]

    def has_movement_ang_z(self):
        """
        Indicates if particle has any angular movement in z-axis.

        :return: Angular movement
        :rtype: bool
        """
        return self._boolrot[2]

    def has_movement_x(self):
        """
        Indicates if particle has any movement in x-axis.

        :return: Movement
        :rtype: bool
        """
        return self._boolvel[0]

    def has_movement_y(self):
        """
        Indicates if particle has any movement in y-axis.

        :return: Movement
        :rtype: bool
        """
        return self._boolvel[0]

    def has_movement_z(self):
        """
        Indicates if particle has any movement in z-axis.

        :return: Movement
        :rtype: bool
        """
        return self._boolvel[0]

    def start(self):
        """
        Enable all movements.
        """
        self.start_ang_movement_all()
        self.start_movement_all()

    def stop(self):
        """
        Stop all movements.
        """
        self.stop_ang_movement_all()
        self.stop_movement_all()

    def update(self):
        """
        Updates particle status.
        """
        if self.has_movement_ang_x():
            self.rotate_x(self._angvel.get_x())
        if self.has_movement_ang_y():
            self.rotate_y(self._angvel.get_y())
        if self.has_movement_ang_z():
            self.rotate_z(self._angvel.get_z())
        if self.has_movement_x():
            self.move_x(self._posVel.get_x())
        if self.has_movement_y():
            self.move_y(self._posVel.get_y())
        if self.has_movement_z():
            self.move_z(self._posVel.get_z())
        f_count = 0
        for fun in self._functions:
            if self._functionUpdate[f_count]:
                fun(*self._functionArguments[f_count])
            f_count += 1

    def get_name(self):
        """
        Returns particle name.

        :return: Name
        :rtype: basestring
        """
        return self._name

    def set_name(self, n):
        """
        Set particle name.

        :param n: Name
        :type n: basestring
        """
        self._name = n

    def bind(self, fun, exec_on_update=True, arguments=None):
        """
        Bind a function to the partcle, that function will be executed after each update, or can be executed
        indepently using execFunc particle method.

        :param fun: Function
        :param exec_on_update: The function is executed after each update
        :param arguments: Arguments of the function
        :type fun: FunctionType
        :type exec_on_update: bool
        :type arguments: list
        """
        if arguments is None:
            arguments = []
        if isinstance(fun, _types.FunctionType):
            self._functions.append(fun)
            self._functionArguments.append(arguments)
            self._functionUpdate.append(exec_on_update)
        else:
            raise Exception('fun must be FunctionType')

    def get_total_binded(self):
        """
        Return total function binded.

        :return: Total function binded
        :rtype: int
        """
        return len(self._functions)

    def get_binded_names(self):
        """
        Get binded function names.

        :return: Function names
        :rtype: basestring
        """
        names = []
        for fun in self._functions:
            names.append(fun.__name__)
        return ', '.join(names)

    def exec_func(self, funcname):
        """
        Executes an function.

        :param funcname: Function name
        :type funcname: basestring
        """
        if funcname in self.get_binded_names():
            f_count = 0
            for fun in self._functions:
                if funcname == fun.__name__:
                    if type(self._functionArguments[f_count]) is tuple:
                        fun(*self._functionArguments[f_count])
                    else:
                        fun(self._functionArguments[f_count])
                f_count += 1
        else:
            raise Exception('Function {0} does not exists'.format(funcname))

    def exec_property_func(self, propertyname, params=None):
        """
        Executes an property function.

        :param propertyname: Property name
        :param params: Function parameters
        :type propertyname: basestring
        :type params: tuple, list, object
        """
        fun = self.get_property(propertyname)
        if params is not None:
            if type(params) is tuple or type(params) is list:
                fun(*params)
            else:
                fun(params)
        else:
            fun()

    def add_property(self, propname, value):
        """
        Add a property to the particle.

        :param propname: Property name
        :param value: Property value
        :type propname: basestring, int
        :type value: object
        """
        if type(propname) is int or type(propname) is str:
            self._properties[propname] = value
        else:
            raise Exception('Property name must be int or string')

    def get_property(self, propname):
        """
        Return property value.

        :param propname: Property name
        :type propname: basestring, int
        :return: object
        """
        if propname in self._get_prop_name():
            return self._properties[propname]
        else:
            raise Exception('Property {0} does not exists'.format(propname))

    def get_property_list(self, propname, propindex):
        """
        Returns property value from index.

        :param propname: Property name
        :param propindex: Property index
        :type propname: basestring, int
        :type propindex: basestring, int
        :return: Value
        :rtype: object
        """
        if propname in self._get_prop_name():
            try:
                return self._properties[propname][propindex]
            except:
                raise Exception('Index {0} not valid'.format(propindex))
        else:
            raise Exception('Property {0} does not exists'.format(propname))

    def modify_property(self, propname, newvalue, operator=None):
        """
        Modify an property, receive parameter, value and a operator.
        Accepted operators:

        PARTICLE_OPERATOR_ADD   Adds to another value
        PARTICLE_OPERATOR_AND   AND logic operator
        PARTICLE_OPERATOR_DIFF  Substract to another value
        PARTICLE_OPERATOR_DIV   Divide with another value
        PARTICLE_OPERATOR_MOD   Module
        PARTICLE_OPERATOR_MULT  Multiply
        PARTICLE_OPERATOR_OR    OR logic operator
        PARTICLE_OPERATOR_POW   POW operator
        PARTICLE_OPERATOR_XOR   XOR logic operator

        :param propname: Property name
        :param newvalue: Property value
        :param operator: Operator
        :type propname: basestring, int
        :type newvalue: object
        :type operator: int
        """
        if propname in self._get_prop_name():
            if operator is None:
                self._properties[propname] = newvalue
            else:
                if operator == PARTICLES_OPERATOR_ADD:
                    self._properties[propname] += newvalue
                elif operator == PARTICLES_OPERATOR_AND:
                    self._properties[propname] = self._properties[propname] and newvalue
                elif operator == PARTICLES_OPERATOR_DIFF:
                    self._properties[propname] -= newvalue
                elif operator == PARTICLES_OPERATOR_DIV:
                    self._properties[propname] /= newvalue
                elif operator == PARTICLES_OPERATOR_MOD:
                    self._properties[propname] %= newvalue
                elif operator == PARTICLES_OPERATOR_OR:
                    self._properties[propname] = self._properties[propname] or newvalue
                elif operator == PARTICLES_OPERATOR_POW:
                    self._properties[propname] = self._properties[propname] ** newvalue
                elif operator == PARTICLES_OPERATOR_XOR:
                    _p = self._properties[propname]
                    _q = newvalue
                    self._properties[propname] = (_p and not _q) or (not _p and _q)
                else:
                    raise Exception('Invalid operator')
        else:
            raise Exception('Property {0} does not exits'.format(propname))

    def _get_prop_name(self):
        """
        Get all property names.

        :return: Property names
        :rtype: list
        """
        return self._properties.keys()

    def print_properties(self):
        """
        Print particle properties to console.
        """
        print('Properties of: {0}'.format(self.get_name()))
        for prop in self._get_prop_name():
            if type(prop) is int:
                print('\t{0} => {1}'.format(prop, self.get_property(prop)))
            else:
                print('\t\'{0}\' => {1}'.format(prop, self.get_property(prop)))

    def __getitem__(self):
        """
        Get position list.

        :return: Position as list
        :rtype: list
        """
        return self.get_position_list()

    def __str__(self):
        """
        Returns particle status.

        :return: Particle status
        :rtype: basestring
        """

        def onoff(boolean):
            """
            Returns on/off depeding boolean value.

            :param boolean: Value
            :type boolean: bool
            :return: String on/off
            :rtype: basestring
            """
            if boolean:
                return 'on'
            else:
                return 'off'

        def get_prop_list():
            """
            Return properties list as string.

            :return: Properties list
            :rtype: basestring
            """
            s = []
            for prop in self._get_prop_name():
                s.append(str(prop))
            return ', '.join(s)

        def get_funct_list():
            """
            Get function list name.

            :return: String
            :rtype: basestring
            """
            s = self.get_binded_names()
            if s == '':
                s = 'None'
            return s

        msg = 'Particle: {15}\nXYZ position: ({0},{1},{2})\nAngular velocity: ({3},{4},{5}); ({9},{10},{11})\nLinear ' \
              'velocity: ({6},{7},{8})); ({12},{13},{14})\nBinded functions: {16}\nProperties: {17} '
        return msg.format(round(self.get_x(), _PARTICLES_ROUND),
                          round(self.get_y(), _PARTICLES_ROUND),
                          round(self.get_z(), _PARTICLES_ROUND),
                          round(self.get_ang_vel_x(), _PARTICLES_ROUND),
                          round(self.get_ang_vel_y(), _PARTICLES_ROUND),
                          round(self.get_ang_vel_z(), _PARTICLES_ROUND),
                          round(self.get_vel_x(), _PARTICLES_ROUND),
                          round(self.get_vel_y(), _PARTICLES_ROUND),
                          round(self.get_vel_z(), _PARTICLES_ROUND),
                          onoff(self.has_movement_ang_x()),
                          onoff(self.has_movement_ang_y()),
                          onoff(self.has_movement_ang_z()),
                          onoff(self.has_movement_x()),
                          onoff(self.has_movement_y()),
                          onoff(self.has_movement_z()), self.get_name(),
                          get_funct_list(), get_prop_list())
