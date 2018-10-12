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
from PyOpenGLtoolbox.utils_math import cos, sin, Point3, Vector3
import types

# Constants
OPERATOR_ADD = 0x0f60
OPERATOR_AND = 0x0f61
OPERATOR_DIFF = 0x0f62
OPERATOR_DIV = 0x0f63
OPERATOR_MOD = 0x0f64
OPERATOR_MULT = 0x0f65
OPERATOR_OR = 0x0f66
OPERATOR_POW = 0x0f67
OPERATOR_XOR = 0x0f68
PARTICLES_ROUND = 3


class Particle:
    """
    Particle
    """

    def __init__(self, posx=0.0, posy=0.0, posz=0.0):
        """Función constructora"""
        self.position = Point3(posx, posy, posz)
        # Velocidades angulares y booleano de movimiento por ejes (x,y,z)
        self.angvel = Vector3()
        self.boolrot = [False, False, False]
        # Velocidades y booleano de movimiento por ejes (x,y,z)
        self.posvel = Vector3()
        self.boolvel = [False, False, False]
        self._name = "unnamed"
        self.functions = []
        self.functionArguments = []
        self.functionUpdate = []
        self.properties = {}

    def set_x(self, x):
        """Modifica la posición X de la partícula"""
        self.position.set_x(x)

    def set_y(self, y):
        """Modifica la posición Y de la partícula"""
        self.position.set_y(y)

    def set_z(self, z):
        """Modifica la posición Z de la partícula"""
        self.position.set_z(z)

    def get_x(self):
        """Retorna la posición X de la partícula"""
        return self.position.get_x()

    def get_y(self):
        """Retorna la posición Y de la partícula"""
        return self.position.get_y()

    def get_z(self):
        """Retorna la posición Z de la partícula"""
        return self.position.get_z()

    def rotate_x(self, ang):
        """Rota la partícula según el eje X en ang grados"""
        if ang != 0.0:
            x = self.get_x()
            y = self.get_y() * cos(ang) - self.get_z() * sin(ang)
            z = self.get_y() * sin(ang) + self.get_z() * cos(ang)
            self.set_x(x)
            self.set_y(y)
            self.set_z(z)

    def rotate_y(self, ang):
        """Rota la partícula según el eje Y en ang grados"""
        if ang != 0.0:
            x = self.get_x() * cos(ang) + self.get_z() * sin(ang)
            y = self.get_y()
            z = -self.get_x() * sin(ang) + self.get_z() * cos(ang)
            self.set_x(x)
            self.set_y(y)
            self.set_z(z)

    def rotate_z(self, ang):
        """Rota la partícula según el eje Z en ang grados"""
        if ang != 0.0:
            x = self.get_x() * cos(ang) - self.get_y() * sin(ang)
            y = self.get_x() * sin(ang) + self.get_y() * cos(ang)
            z = self.get_z()
            self.set_x(x)
            self.set_y(y)
            self.set_z(z)

    def get_position_list(self):
        """Retorna la posición de la partícula como una lista"""
        return self.position.export_to_list()

    def get_position_tuple(self):
        """Retorna la posición de la partícula como una tupla"""
        return self.position.export_to_tuple()

    def set_ang_vel(self, velx=0.0, vely=0.0, velz=0.0):
        """Define la velocidad angular de la partícula"""
        self.set_ang_vel_x(velx)
        self.set_ang_vel_y(vely)
        self.set_ang_vel_z(velz)

    def set_ang_vel_x(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje X"""
        self.angvel.set_x(angvel)
        if enable_movement:
            self.start_ang_movement_x()

    def set_ang_vel_y(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje Y"""
        self.angvel.set_y(angvel)
        if enable_movement:
            self.start_ang_movement_y()

    def set_ang_vel_z(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje Z"""
        self.angvel.set_z(angvel)
        if enable_movement:
            self.start_ang_movement_z()

    def get_ang_vel_x(self):
        """Retorna la velocidad angular en el eje X"""
        return self.angvel.get_x()

    def get_ang_vel_y(self):
        """Retorna la velocidad angular en el eje Y"""
        return self.angvel.get_y()

    def get_ang_vel_z(self):
        """Retorna la velocidad angular en el eje Z"""
        return self.angvel.get_z()

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
        self.boolrot[0] = True

    def stop_ang_movement_x(self):
        """Detiene la rotación en el eje X"""
        self.boolrot[0] = False

    def start_ang_movement_y(self):
        """Activa la rotación en el eje Y"""
        self.boolrot[1] = True

    def stop_ang_movement_y(self):
        """Detiene la rotación en el eje Y"""
        self.boolrot[1] = False

    def start_ang_movement_z(self):
        """Activa la rotación en el eje Z"""
        self.boolrot[2] = True

    def stop_ang_movement_z(self):
        """Detiene la rotación en el eje Z"""
        self.boolrot[2] = False

    def set_vel(self, velx=0.0, vely=0.0, velz=0.0):
        """Define la velocidad de la partícula en todos los ejes"""
        self.set_vel_x(velx)
        self.set_vel_y(vely)
        self.set_vel_z(velz)

    def set_vel_x(self, vel, enable_movement=False):
        """Define la velocidad de la partícula en el eje X"""
        self.posvel.set_x(vel)
        if enable_movement:
            self.start_movement_x()

    def set_vel_y(self, vel, enable_movement=False):
        """Define la velocidad de la partícula en el eje Y"""
        self.posvel.set_y(vel)
        if enable_movement:
            self.start_movement_y()

    def set_vel_z(self, vel, enable_movement=False):
        """Define la velocidad de la partícula en el eje Z"""
        self.posvel.set_z(vel)
        if enable_movement:
            self.start_movement_z()

    def get_vel_x(self):
        """Retorna la velocidad en el eje X"""
        return self.posvel.get_x()

    def get_vel_y(self):
        """Retorna la velocidad en el eje Y"""
        return self.posvel.get_y()

    def get_vel_z(self):
        """Retorna la velocidad en el eje Z"""
        return self.posvel.get_z()

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
        self.boolvel[0] = True

    def stop_movement_x(self):
        """Desactiva el movimiento en el eje X"""
        self.boolvel[0] = False

    def start_movement_y(self):
        """Activa el movimiento en el eje Y"""
        self.boolvel[1] = True

    def stop_movement_y(self):
        """Desactiva el movimiento en el eje Y"""
        self.boolvel[1] = False

    def start_movement_z(self):
        """Activa el movimiento en el eje Z"""
        self.boolvel[2] = True

    def stop_movement_z(self):
        """Desactiva el movimiento en el eje Z"""
        self.boolvel[2] = False

    def has_movement_ang_x(self):
        """Retorna si tiene movimiento angular en el eje X"""
        return self.boolrot[0]

    def has_movement_ang_y(self):
        """Retorna si tiene movimiento angular en el eje Y"""
        return self.boolrot[1]

    def has_movement_ang_z(self):
        """Retorna si tiene movimiento angular en el eje Z"""
        return self.boolrot[2]

    def has_movement_x(self):
        """Retorna si tiene movimiento en el eje X"""
        return self.boolvel[0]

    def has_movement_y(self):
        """Retorna si tiene movimiento en el eje Y"""
        return self.boolvel[0]

    def has_movement_z(self):
        """Retorna si tiene movimiento en el eje Z"""
        return self.boolvel[0]

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
            self.rotate_x(self.angvel.get_x())
        if self.has_movement_ang_y():
            self.rotate_y(self.angvel.get_y())
        if self.has_movement_ang_z():
            self.rotate_z(self.angvel.get_z())
        if self.has_movement_x():
            self.move_x(self.posvel.get_x())
        if self.has_movement_y():
            self.move_y(self.posvel.get_y())
        if self.has_movement_z():
            self.move_z(self.posvel.get_z())
        f_count = 0
        for fun in self.functions:
            if self.functionUpdate[f_count]:
                fun(*self.functionArguments[f_count])
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
        if isinstance(fun, types.FunctionType):
            self.functions.append(fun)
            self.functionArguments.append(arguments)
            self.functionUpdate.append(exec_on_update)
        else:
            raise Exception("el elemento a agregar debe ser una función")

    def get_total_binded(self):
        """Retorna la cantidad de funciones bindeadas a la partícula"""
        return len(self.functions)

    def get_binded_names(self):
        """Retorna el nombre de las funciones bindeadas a la partícula"""
        names = []
        for fun in self.functions:
            names.append(fun.__name__)
        return ", ".join(names)

    def exec_func(self, funcname):
        """Ejecuta una función"""
        if funcname in self.get_binded_names():
            f_count = 0
            for fun in self.functions:
                if funcname == fun.__name__:
                    if type(self.functionArguments[f_count]) is tuple:
                        fun(*self.functionArguments[f_count])
                    else:
                        fun(self.functionArguments[f_count])
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
            self.properties[propname] = value
        else:
            raise Exception("la propiedad debe ser de tipo int o string")

    def get_property(self, propname):
        """Retorna el valor de una propiedad"""
        if propname in self._get_prop_name():
            return self.properties[propname]
        else:
            raise Exception("la propiedad no existe")

    def get_property_list(self, propname, propindex):
        """Retorna el valor de una propiedad que es lista y es parte de índice index"""
        if propname in self._get_prop_name():
            try:
                return self.properties[propname][propindex]
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
                self.properties[propname] = newvalue
            else:
                if operator == OPERATOR_ADD:
                    self.properties[propname] += newvalue
                elif operator == OPERATOR_AND:
                    self.properties[propname] = self.properties[propname] and newvalue
                elif operator == OPERATOR_DIFF:
                    self.properties[propname] -= newvalue
                elif operator == OPERATOR_DIV:
                    self.properties[propname] /= newvalue
                elif operator == OPERATOR_MOD:
                    self.properties[propname] %= newvalue
                elif operator == OPERATOR_OR:
                    self.properties[propname] = self.properties[propname] or newvalue
                elif operator == OPERATOR_POW:
                    self.properties[propname] = self.properties[propname] ** newvalue
                elif operator == OPERATOR_XOR:
                    _p = self.properties[propname]
                    _q = newvalue
                    self.properties[propname] = (_p and not _q) or (not _p and _q)
                else:
                    raise Exception("operacion incorrecta")
        else:
            raise Exception("la propiedad no existe")

    def _get_prop_name(self):
        """Retorna todos los nombres de propiedades"""
        return self.properties.keys()

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
        return msg.format(round(self.get_x(), PARTICLES_ROUND),
                          round(self.get_y(), PARTICLES_ROUND),
                          round(self.get_z(), PARTICLES_ROUND),
                          round(self.get_ang_vel_x(), PARTICLES_ROUND),
                          round(self.get_ang_vel_y(), PARTICLES_ROUND),
                          round(self.get_ang_vel_z(), PARTICLES_ROUND),
                          round(self.get_vel_x(), PARTICLES_ROUND),
                          round(self.get_vel_y(), PARTICLES_ROUND),
                          round(self.get_vel_z(), PARTICLES_ROUND),
                          onoff(self.has_movement_ang_x()),
                          onoff(self.has_movement_ang_y()),
                          onoff(self.has_movement_ang_z()),
                          onoff(self.has_movement_x()),
                          onoff(self.has_movement_y()),
                          onoff(self.has_movement_z()), self.get_name(),
                          get_funct_list(), get_prop_list())
