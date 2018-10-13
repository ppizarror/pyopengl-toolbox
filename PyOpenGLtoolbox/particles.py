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
from PyOpenGLtoolbox.utils_math import _cos, _sin, Point3, Vector3
import types as _types

# Constants
_OPERATOR_ADD = 0x0f60
_OPERATOR_AND = 0x0f61
_OPERATOR_DIFF = 0x0f62
_OPERATOR_DIV = 0x0f63
_OPERATOR_MOD = 0x0f64
_OPERATOR_MULT = 0x0f65
_OPERATOR_OR = 0x0f66
_OPERATOR_POW = 0x0f67
_OPERATOR_XOR = 0x0f68
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
        """Retorna la posición de la partícula como una lista"""
        return self._position.export_to_list()

    def get_position_tuple(self):
        """Retorna la posición de la partícula como una tupla"""
        return self._position.export_to_tuple()

    def set_ang_vel(self, velx=0.0, vely=0.0, velz=0.0):
        """Define la velocidad angular de la partícula"""
        self.set_ang_vel_x(velx)
        self.set_ang_vel_y(vely)
        self.set_ang_vel_z(velz)

    def set_ang_vel_x(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje X"""
        self._angvel.set_x(angvel)
        if enable_movement:
            self.start_ang_movement_x()

    def set_ang_vel_y(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje Y"""
        self._angvel.set_y(angvel)
        if enable_movement:
            self.start_ang_movement_y()

    def set_ang_vel_z(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje Z"""
        self._angvel.set_z(angvel)
        if enable_movement:
            self.start_ang_movement_z()

    def get_ang_vel_x(self):
        """Retorna la velocidad angular en el eje X"""
        return self._angvel.get_x()

    def get_ang_vel_y(self):
        """Retorna la velocidad angular en el eje Y"""
        return self._angvel.get_y()

    def get_ang_vel_z(self):
        """Retorna la velocidad angular en el eje Z"""
        return self._angvel.get_z()

    def start_ang_movement_all(self):
        """Activa la rotación en todos los ejes"""
        self.start_ang_movement_x()
        self.start_ang_movement_y()
        self.start_ang_movement_z()

    def stop_ang_movement_all(self):
        """Desactiva la rotación en todos los ejes"""
        self.stop_ang_movement_x()
        self.stop_ang_movement_y()
        self.stop_ang_movement_z()

    def start_ang_movement_x(self):
        """Activa la rotación en el eje X"""
        self._boolrot[0] = True

    def stop_ang_movement_x(self):
        """Detiene la rotación en el eje X"""
        self._boolrot[0] = False

    def start_ang_movement_y(self):
        """Activa la rotación en el eje Y"""
        self._boolrot[1] = True

    def stop_ang_movement_y(self):
        """Detiene la rotación en el eje Y"""
        self._boolrot[1] = False

    def start_ang_movement_z(self):
        """Activa la rotación en el eje Z"""
        self._boolrot[2] = True

    def stop_ang_movement_z(self):
        """Detiene la rotación en el eje Z"""
        self._boolrot[2] = False

    def set_vel(self, velx=0.0, vely=0.0, velz=0.0):
        """Define la velocidad de la partícula en todos los ejes"""
        self.set_vel_x(velx)
        self.set_vel_y(vely)
        self.set_vel_z(velz)

    def set_vel_x(self, vel, enable_movement=False):
        """Define la velocidad de la partícula en el eje X"""
        self._posVel.set_x(vel)
        if enable_movement:
            self.start_movement_x()

    def set_vel_y(self, vel, enable_movement=False):
        """Define la velocidad de la partícula en el eje Y"""
        self._posVel.set_y(vel)
        if enable_movement:
            self.start_movement_y()

    def set_vel_z(self, vel, enable_movement=False):
        """Define la velocidad de la partícula en el eje Z"""
        self._posVel.set_z(vel)
        if enable_movement:
            self.start_movement_z()

    def get_vel_x(self):
        """Retorna la velocidad en el eje X"""
        return self._posVel.get_x()

    def get_vel_y(self):
        """Retorna la velocidad en el eje Y"""
        return self._posVel.get_y()

    def get_vel_z(self):
        """Retorna la velocidad en el eje Z"""
        return self._posVel.get_z()

    def move_x(self, delta):
        """Mueva la partícula en delta en el eje X"""
        self.set_x(delta + self.get_x())

    def move_y(self, delta):
        """Mueva la partícula en delta en el eje Y"""
        self.set_y(delta + self.get_y())

    def move_z(self, delta):
        """Mueva la partícula en delta en el eje Z"""
        self.set_z(delta + self.get_z())

    def start_movement_all(self):
        """Activa el movimiento en todos los ejes"""
        self.start_movement_x()
        self.start_movement_y()
        self.start_movement_z()

    def stop_movement_all(self):
        """Detiene el movimiento en todos los ejes"""
        self.stop_movement_x()
        self.stop_movement_y()
        self.stop_movement_z()

    def start_movement_x(self):
        """Activa el movimiento en el eje X"""
        self._boolvel[0] = True

    def stop_movement_x(self):
        """Desactiva el movimiento en el eje X"""
        self._boolvel[0] = False

    def start_movement_y(self):
        """Activa el movimiento en el eje Y"""
        self._boolvel[1] = True

    def stop_movement_y(self):
        """Desactiva el movimiento en el eje Y"""
        self._boolvel[1] = False

    def start_movement_z(self):
        """Activa el movimiento en el eje Z"""
        self._boolvel[2] = True

    def stop_movement_z(self):
        """Desactiva el movimiento en el eje Z"""
        self._boolvel[2] = False

    def has_movement_ang_x(self):
        """Retorna si tiene movimiento angular en el eje X"""
        return self._boolrot[0]

    def has_movement_ang_y(self):
        """Retorna si tiene movimiento angular en el eje Y"""
        return self._boolrot[1]

    def has_movement_ang_z(self):
        """Retorna si tiene movimiento angular en el eje Z"""
        return self._boolrot[2]

    def has_movement_x(self):
        """Retorna si tiene movimiento en el eje X"""
        return self._boolvel[0]

    def has_movement_y(self):
        """Retorna si tiene movimiento en el eje Y"""
        return self._boolvel[0]

    def has_movement_z(self):
        """Retorna si tiene movimiento en el eje Z"""
        return self._boolvel[0]

    def start(self):
        """Activa todos los movimientos"""
        self.start_ang_movement_all()
        self.start_movement_all()

    def stop(self):
        """Desactiva todos los movimientos"""
        self.stop_ang_movement_all()
        self.stop_movement_all()

    def update(self):
        """Actualiza el estado de la partícula"""
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
        """Retorna el nombre de la partícula"""
        return self._name

    def set_name(self, n):
        """Define el nombre de la partícula"""
        self._name = n

    def bind(self, fun, exec_on_update=True, arguments=None):
        """Agrega una función a la partícula la cual puede ejecutarse en cada update o ejecutarse separadamente
        llamando a execFunc"""
        if arguments is None:
            arguments = []
        if isinstance(fun, _types.FunctionType):
            self._functions.append(fun)
            self._functionArguments.append(arguments)
            self._functionUpdate.append(exec_on_update)
        else:
            raise Exception("el elemento a agregar debe ser una función")

    def get_total_binded(self):
        """Retorna la cantidad de funciones bindeadas a la partícula"""
        return len(self._functions)

    def get_binded_names(self):
        """Retorna el nombre de las funciones bindeadas a la partícula"""
        names = []
        for fun in self._functions:
            names.append(fun.__name__)
        return ", ".join(names)

    def exec_func(self, funcname):
        """Ejecuta una función"""
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
            raise Exception("la función {0} no existe".format(funcname))

    def exec_property_func(self, propertyname, params=None):
        """Ejecuta una función de una propiedad"""
        fun = self.get_property(propertyname)
        if params is not None:
            if type(params) is tuple:
                fun(*params)
            else:
                fun(params)
        else:
            fun()

    def add_property(self, propname, value):
        """Agrega una propiedad a la partícula"""
        if type(propname) is int or type(propname) is str:
            self._properties[propname] = value
        else:
            raise Exception("la propiedad debe ser de tipo int o string")

    def get_property(self, propname):
        """Retorna el valor de una propiedad"""
        if propname in self._get_prop_name():
            return self._properties[propname]
        else:
            raise Exception("la propiedad no existe")

    def get_property_list(self, propname, propindex):
        """Retorna el valor de una propiedad que es lista y es parte de índice index"""
        if propname in self._get_prop_name():
            try:
                return self._properties[propname][propindex]
            except:
                raise Exception("indice {0} incorrecto".format(propindex))
        else:
            raise Exception("la propiedad {0} no existe".format(propname))

    def modify_property(self, propname, newvalue, operator=None):
        """Modifica el valor de una propiedad, recibe como parametro el nombre de la propiedad, un valor y una operacion,
        operadores aceptados:

        OPERATOR_ADD: Sumar con otro valor
        OPERATOR_AND: Calcular el operador logico and
        OPERATOR_DIFF: Restar con otro valor
        OPERATOR_DIV: Dividir con otro valor
        OPERATOR_MOD: Sacar modulo con otor valor
        OPERATOR_MULT: Multiplicar por otro valor
        OPERATOR_OR: Calcular el operador logico or
        OPERATOR_POW: Elevar a la potencia
        OPERATOR_XOR: Calcular el operador logico xor
        """
        if propname in self._get_prop_name():
            if operator is None:
                self._properties[propname] = newvalue
            else:
                if operator == _OPERATOR_ADD:
                    self._properties[propname] += newvalue
                elif operator == _OPERATOR_AND:
                    self._properties[propname] = self._properties[propname] and newvalue
                elif operator == _OPERATOR_DIFF:
                    self._properties[propname] -= newvalue
                elif operator == _OPERATOR_DIV:
                    self._properties[propname] /= newvalue
                elif operator == _OPERATOR_MOD:
                    self._properties[propname] %= newvalue
                elif operator == _OPERATOR_OR:
                    self._properties[propname] = self._properties[propname] or newvalue
                elif operator == _OPERATOR_POW:
                    self._properties[propname] = self._properties[propname] ** newvalue
                elif operator == _OPERATOR_XOR:
                    _p = self._properties[propname]
                    _q = newvalue
                    self._properties[propname] = (_p and not _q) or (not _p and _q)
                else:
                    raise Exception("operacion incorrecta")
        else:
            raise Exception("la propiedad no existe")

    def _get_prop_name(self):
        """Retorna todos los nombres de propiedades"""
        return self._properties.keys()

    def print_properties(self):
        """Imprime las propiedades de la partícula y sus valores"""
        print('Properties of: {0}'.format(self.get_name()))
        for prop in self._get_prop_name():
            if type(prop) is int:
                print('\t{0} => {1}'.format(prop, self.get_property(prop)))
            else:
                print('\t\'{0}\' => {1}'.format(prop, self.get_property(prop)))

    def __getitem__(self, item):
        """Retorna el elemento en forma de lista"""
        return self.get_position_list()

    def __str__(self):
        """Retorna el estado de la partícula"""

        def onoff(boolean):
            """Retorna on/off en función del valor booleano"""
            if boolean:
                return "on"
            else:
                return "off"

        def get_prop_list():
            """
            Return properties list
            :return:
            """
            s = []
            for prop in self._get_prop_name():
                s.append(str(prop))
            return ", ".join(s)

        def get_funct_list():
            """
            Get function list
            :return:
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
