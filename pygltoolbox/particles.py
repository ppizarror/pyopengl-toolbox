# coding=utf-8
"""
PARTICLES
Provee funciones para manejar partículas
"""

# Importación de librerías
from utils import *

# Definicion de constantes
OPERATOR_ADD = 0x0f60  # Operador de suma
OPERATOR_AND = 0x0f61  # Operador and
OPERATOR_DIFF = 0x0f62  # Operador de resta
OPERATOR_DIV = 0x0f63  # Operador de division
OPERATOR_MOD = 0x0f64  # Operador de modulo
OPERATOR_MULT = 0x0f65  # Operador de multiplicacion
OPERATOR_OR = 0x0f66  # Operador or
OPERATOR_POW = 0x0f67  # Operador de elevacion
OPERATOR_XOR = 0x0f68  # Operador xor
PARTICLES_ROUND = 2  # Numero de decimales


# noinspection PyShadowingNames,PyShadowingBuiltins,PyDefaultArgument
class Particle:
    """Particula"""

    def __init__(self, posx=0.0, posy=0.0, posz=0.0):
        """Funcion constructora"""
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

    def setX(self, x):
        """Modifica la posicion X de la particula"""
        self.position.setX(x)

    def setY(self, y):
        """Modifica la posicion Y de la particula"""
        self.position.setY(y)

    def setZ(self, z):
        """Modifica la posicion Z de la particula"""
        self.position.setZ(z)

    def getX(self):
        """Retorna la posicion X de la particula"""
        return self.position.getX()

    def getY(self):
        """Retorna la posicion Y de la particula"""
        return self.position.getY()

    def getZ(self):
        """Retorna la posicion Z de la particula"""
        return self.position.getZ()

    def rotateX(self, ang):
        """Rota la particula segun el eje X en ang grados"""
        if ang != 0.0:
            x = self.getX()
            y = self.getY() * cos(ang) - self.getZ() * sin(ang)
            z = self.getY() * sin(ang) + self.getZ() * cos(ang)
            self.setX(x)
            self.setY(y)
            self.setZ(z)

    def rotateY(self, ang):
        """Rota la particula segun el eje Y en ang grados"""
        if ang != 0.0:
            x = self.getX() * cos(ang) + self.getZ() * sin(ang)
            y = self.getY()
            z = -self.getX() * sin(ang) + self.getZ() * cos(ang)
            self.setX(x)
            self.setY(y)
            self.setZ(z)

    def rotateZ(self, ang):
        """Rota la particula segun el eje Z en ang grados"""
        if ang != 0.0:
            x = self.getX() * cos(ang) - self.getY() * sin(ang)
            y = self.getX() * sin(ang) + self.getY() * cos(ang)
            z = self.getZ()
            self.setX(x)
            self.setY(y)
            self.setZ(z)

    def getList(self):
        """Retorna la posicion de la particula como una lista"""
        return self.position.exportToList()

    def getTuple(self):
        """Retorna la posicion de la particula como una tupla"""
        return self.position.exportToTuple()

    def setAngVel(self, velx=0.0, vely=0.0, velz=0.0):
        """Define la velocidad angular de la particula"""
        self.setAngVelX(velx)
        self.setAngVelY(vely)
        self.setAngVelZ(velz)

    def setAngVelX(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje X"""
        self.angvel.setX(angvel)
        if enable_movement:
            self.startAngMovementX()

    def setAngVelY(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje Y"""
        self.angvel.setY(angvel)
        if enable_movement:
            self.startAngMovementY()

    def setAngVelZ(self, angvel, enable_movement=False):
        """Define la velocidad angular en el eje Z"""
        self.angvel.setZ(angvel)
        if enable_movement:
            self.startAngMovementZ()

    def getAngVelX(self):
        """Retorna la velocidad angular en el eje X"""
        return self.angvel.getX()

    def getAngVelY(self):
        """Retorna la velocidad angular en el eje Y"""
        return self.angvel.getY()

    def getAngVelZ(self):
        """Retorna la velocidad angular en el eje Z"""
        return self.angvel.getZ()

    def startAngMovementALl(self):
        """Activa la rotacion en todos los ejes"""
        self.startAngMovementX()
        self.startAngMovementY()
        self.startAngMovementZ()

    def stopAngMovementAll(self):
        """Desactiva la rotacion en todos los ejes"""
        self.stopAngMovementX()
        self.stopAngMovementY()
        self.stopAngMovementZ()

    def startAngMovementX(self):
        """Activa la rotacion en el eje X"""
        self.boolrot[0] = True

    def stopAngMovementX(self):
        """Detiene la rotacion en el eje X"""
        self.boolrot[0] = False

    def startAngMovementY(self):
        """Activa la rotacion en el eje Y"""
        self.boolrot[1] = True

    def stopAngMovementY(self):
        """Detiene la rotacion en el eje Y"""
        self.boolrot[1] = False

    def startAngMovementZ(self):
        """Activa la rotacion en el eje Z"""
        self.boolrot[2] = True

    def stopAngMovementZ(self):
        """Detiene la rotacion en el eje Z"""
        self.boolrot[2] = False

    def setVel(self, velx=0.0, vely=0.0, velz=0.0):
        """Define la velocidad de la particula en todos los ejes"""
        self.setVelX(velx)
        self.setVelY(vely)
        self.setVelZ(velz)

    def setVelX(self, vel, enable_movement=False):
        """Define la velocidad de la particula en el eje X"""
        self.posvel.setX(vel)
        if enable_movement:
            self.startMovementX()

    def setVelY(self, vel, enable_movement=False):
        """Define la velocidad de la particula en el eje Y"""
        self.posvel.setY(vel)
        if enable_movement:
            self.startMovementY()

    def setVelZ(self, vel, enable_movement=False):
        """Define la velocidad de la particula en el eje Z"""
        self.posvel.setZ(vel)
        if enable_movement:
            self.startMovementZ()

    def getVelX(self):
        """Retorna la velocidad en el eje X"""
        return self.posvel.getX()

    def getVelY(self):
        """Retorna la velocidad en el eje Y"""
        return self.posvel.getY()

    def getVelZ(self):
        """Retorna la velocidad en el eje Z"""
        return self.posvel.getZ()

    def moveX(self, delta):
        """Mueva la particula en delta en el eje X"""
        self.setX(delta + self.getX())

    def moveY(self, delta):
        """Mueva la particula en delta en el eje Y"""
        self.setY(delta + self.getY())

    def moveZ(self, delta):
        """Mueva la particula en delta en el eje Z"""
        self.setZ(delta + self.getZ())

    def startMovementAll(self):
        """Activa el movimiento en todos los ejes"""
        self.startMovementX()
        self.startMovementY()
        self.startMovementZ()

    def stopMovementAll(self):
        """Detiene el movimiento en todos los ejes"""
        self.stopMovementX()
        self.stopMovementY()
        self.stopMovementZ()

    def startMovementX(self):
        """Activa el movimiento en el eje X"""
        self.boolvel[0] = True

    def stopMovementX(self):
        """Desactiva el movimiento en el eje X"""
        self.boolvel[0] = False

    def startMovementY(self):
        """Activa el movimiento en el eje Y"""
        self.boolvel[1] = True

    def stopMovementY(self):
        """Desactiva el movimiento en el eje Y"""
        self.boolvel[1] = False

    def startMovementZ(self):
        """Activa el movimiento en el eje Z"""
        self.boolvel[2] = True

    def stopMovementZ(self):
        """Desactiva el movimiento en el eje Z"""
        self.boolvel[2] = False

    def hasMovementAngX(self):
        """Retorna si tiene movimiento angular en el eje X"""
        return self.boolrot[0]

    def hasMovementAngY(self):
        """Retorna si tiene movimiento angular en el eje Y"""
        return self.boolrot[1]

    def hasMovementAngZ(self):
        """Retorna si tiene movimiento angular en el eje Z"""
        return self.boolrot[2]

    def hasMovementX(self):
        """Retorna si tiene movimiento en el eje X"""
        return self.boolvel[0]

    def hasMovementY(self):
        """Retorna si tiene movimiento en el eje Y"""
        return self.boolvel[0]

    def hasMovementZ(self):
        """Retorna si tiene movimiento en el eje Z"""
        return self.boolvel[0]

    def start(self):
        """Activa todos los movimientos"""
        self.startAngMovementALl()
        self.startMovementAll()

    def stop(self):
        """Desactiva todos los movimientos"""
        self.stopAngMovementAll()
        self.stopMovementAll()

    def update(self):
        """Actualiza el estado de la particula"""
        if self.hasMovementAngX():
            self.rotateX(self.angvel.getX())
        if self.hasMovementAngY():
            self.rotateY(self.angvel.getY())
        if self.hasMovementAngZ():
            self.rotateZ(self.angvel.getZ())
        if self.hasMovementX():
            self.moveX(self.posvel.getX())
        if self.hasMovementY():
            self.moveY(self.posvel.getY())
        if self.hasMovementZ():
            self.moveZ(self.posvel.getZ())
        f_count = 0
        for func in self.functions:
            if self.functionUpdate[f_count]:
                func(*self.functionArguments[f_count])
            f_count += 1

    def getName(self):
        """Retorna el nombre de la particula"""
        return self._name

    def setName(self, name):
        """Define el nombre de la particula"""
        self._name = name

    def bind(self, function, exec_on_update=True, arguments=[]):
        """Agrega una funcion a la particula la cual puede ejecutarse en cada update o ejecutarse separadamente
        llamando a execFunc """
        if isinstance(function, types.FunctionType):
            self.functions.append(function)
            self.functionArguments.append(arguments)
            self.functionUpdate.append(exec_on_update)
        else:
            raise Exception("el elemento a agregar debe ser una funcion")

    def getTotalBinded(self):
        """Retorna la cantidad de funciones bindeadas a la particula"""
        return len(self.functions)

    def getBindedNames(self):
        """Retorna el nombre de las funciones bindeadas a la particula"""
        names = []
        for function in self.functions:
            names.append(function.__name__)
        return ", ".join(names)

    def execFunc(self, funcname):
        """Ejecuta una funcion"""
        if funcname in self.getBindedNames():
            f_count = 0
            for func in self.functions:
                if funcname == func.__name__:
                    func(*self.functionArguments[f_count])
                f_count += 1
        else:
            raise Exception("la funcion {0} no existe".format(funcname))

    def addPropertie(self, propname, value):
        """Agrega una propiedad a la particula"""
        if isinstance(propname, types.IntType) or isinstance(propname, types.StringType):
            self.properties[propname] = value
        else:
            raise Exception("la propiedad debe ser de tipo int o string")

    def getPropertie(self, propname):
        """Retorna el valor de una propiedad"""
        if propname in self._getPropName():
            return self.properties[propname]
        else:
            raise Exception("la propiedad no existe")

    def getPropertieList(self, propname, propindex):
        """Retorna el valor de una propiedad que es lista y es parte de indice index"""
        if propname in self._getPropName():
            try:
                return self.properties[propname][propindex]
            except:
                raise Exception("indice {0} incorrecto".format(propindex))
        else:
            raise Exception("la propiedad {0} no existe".format(propname))

    def modifyPropertie(self, propname, newvalue, operator=None):
        """Modifica el valor de una propiedad, recibe como parametro el nombre de la propiedad, un valor y una operacion, operadores aceptados:
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
        if propname in self._getPropName():
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
                    p = self.properties[propname]
                    q = newvalue
                    self.properties[propname] = (p and not q) or (not p and q)
                else:
                    raise Exception("operacion incorrecta")
        else:
            raise Exception("la propiedad no existe")

    def _getPropName(self):
        """Retorna todos los nombres de propiedades"""
        return self.properties.keys()

    def printProperties(self):
        """Imprime las propiedades de la particula y sus valores"""
        print "Properties of: {0}".format(self.getName())
        for prop in self._getPropName():
            if isinstance(prop, types.IntType):
                print "\t{0} => {1}".format(prop, self.getPropertie(prop))
            else:
                print "\t'{0}' => {1}".format(prop, self.getPropertie(prop))

    def __getitem__(self, item):
        """Retorna el elemento en forma de lista"""
        return self.getList()

    def __str__(self):
        """Retorna el estado de la particula"""

        def onoff(boolean):
            """Retorna on/off en funcion del valor booleano"""
            if boolean:
                return "on"
            else:
                return "off"

        def getPropList():
            s = []
            for prop in self._getPropName():
                s.append(str(prop))
            return ", ".join(s)

        def getFunctList():
            s = self.getBindedNames()
            if s == "":
                s = "None"
            return s

        msg = 'Particle: {15}\nXYZ position: ({0},{1},{2})\nAngular velocity: ({3},{4},{5}); ({9},{10},{11})\nLinear ' \
              'velocity: ({6},{7},{8})); ({12},{13},{14})\nBinded functions: {16}\nProperties: {17} '
        return msg.format(round(self.getX(), PARTICLES_ROUND), round(self.getY(), PARTICLES_ROUND),
                          round(self.getZ(), PARTICLES_ROUND), round(self.getAngVelX(), PARTICLES_ROUND),
                          round(self.getAngVelY(), PARTICLES_ROUND), round(self.getAngVelZ(), PARTICLES_ROUND),
                          round(self.getVelX(), PARTICLES_ROUND), round(self.getVelY(), PARTICLES_ROUND),
                          round(self.getVelZ(), PARTICLES_ROUND), onoff(self.hasMovementAngX()),
                          onoff(self.hasMovementAngY()),
                          onoff(self.hasMovementAngZ()), onoff(self.hasMovementX()), onoff(self.hasMovementY()),
                          onoff(self.hasMovementZ()), self.getName(), getFunctList(), getPropList())
