# coding=utf-8
"""
CAMERA
Provee clases para manejar una cámara.

Copyright (C) 2017 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Importacion de librerias
from OpenGL.GL import *
from OpenGL.GLU import *
from utils_math import *

# Constantes
CAMERA_CENTER_LIMIT_Z_DOWN = -3500
CAMERA_CENTER_LIMIT_Z_UP = 3500
CAMERA_CENTER_VEL = 10
CAMERA_DEFAULT_RVEL = 10
CAMERA_MIN_THETA_VALUE = 0.000001
CAMERA_NEGATIVE = -1.0
CAMERA_POSITIVE = 1.0
CAMERA_ROUNDED = 2
CAMERA_SPHERICAL = 0x0fb
CAMERA_XYZ = 0x0fa


# noinspection PyMethodMayBeStatic
class _Camera:
    """Clase abstracta"""

    def __init__(self):
        """Funcion constructora void"""
        pass

    def place(self):
        """Ubica la camara en el mundo"""
        pass

    def move_x(self, direction=CAMERA_POSITIVE):
        """Mueve la posicion de la camara en el eje x"""
        pass

    def move_y(self, direction=CAMERA_POSITIVE):
        """Mueve la posicion de la camara en el eje y"""
        pass

    def move_z(self, direction=CAMERA_POSITIVE):
        """Mueve la posicion de la camara en el eje z"""
        pass

    def setVelMoveX(self, vel):
        """Define la velocidad de movimiento de la camara en el eje x"""
        pass

    def setVelMoveY(self, vel):
        """Define la velocidad de movimiento de la camara en el eje y"""
        pass

    def setVelMoveZ(self, vel):
        """Define la velocidad de movimiento de la camara en el eje z"""
        pass

    def setCenterVel(self, vel):
        """Define la velocidad de acercamiento/alejamiento de la camara"""
        pass

    def moveCenterX(self, dist):
        """Mueve la coorenada x del centro de vision"""
        pass

    def moveCenterY(self, dist):
        """Mueve la coorenada y del centro de vision"""
        pass

    def moveCenterZ(self, dist):
        """Mueve la coorenada z del centro de vision"""
        pass

    def rotateCenterZ(self, angle):
        """Rota la posicion en el eje z"""
        pass

    def far(self):
        """Aleja la posicion de la camara"""
        pass

    def close(self):
        """Acerca la posicion de la camara"""
        pass

    def setRvel(self, vel):
        """Define la velocidad radial con la que la camara se mueve"""
        pass

    # noinspection PyRedeclaration
    def place(self):
        """Ubica la camara en el mundo"""
        pass

    def rotateX(self, angle):
        """Rota la posicion eye en el eje X cartesiano"""
        pass

    def rotateY(self, angle):
        """Rota la posicion eye en el eje Y cartesiano"""
        pass

    def rotateZ(self, angle):
        """Rota la posicion eye en el eje Z cartesiano"""
        pass

    def convertoXYZ(self):
        """Convierte el sistema esferico a cartesiano"""
        pass

    def __str__(self):
        """Retorna el estado de la camara"""
        pass

    def getName(self):
        """Retorna el nombre de la camara"""
        pass

    # noinspection PyShadowingNames
    def setName(self, name):
        """Define el nombre de la camara"""
        pass


# Clase que maneja la camara
class CameraXYZ(_Camera):
    """Camara en XYZ, pos es del tipo (x,y,z), permite rotacion en z
    @deprecated"""

    def __init__(self, pos, center, up=Point3(0, 0, 1)):
        """Funcion constructora"""
        _Camera.__init__(self)
        if isinstance(pos, Point3) and isinstance(center, Point3) and isinstance(up, Point3):
            self.pos = Vector3(*pos.exportToList())
            self.center = Vector3(*center.exportToList())
            self.up = Vector3(*up.exportToList())
        else:
            raise Exception("pos, center y up deben ser del tipo point3")
        self.cameraVel = Vector3(1.0, 1.0, 1.0)
        self.viewVel = Vector3(1.0, 1.0, 1.0)
        self.angle = 45.0
        self.centerangle = 0.0
        self.centervel = Vector3(CAMERA_CENTER_VEL, CAMERA_CENTER_VEL, CAMERA_CENTER_VEL)
        self._name = "unnamed"

    def place(self):
        """Ubica la camara en el mundo"""
        glLoadIdentity()
        gluLookAt(self.pos.getX(), self.pos.getY(), self.pos.getZ(), self.center.getX(), self.center.getY(),
                  self.center.getZ(), self.up.getX(), self.up.getY(), self.up.getZ())

    def move_x(self, direction=CAMERA_POSITIVE):
        """Mueve la posicion de la camara en el eje x"""
        self.pos.setX(self.pos.getX() + self.cameraVel.getX() * direction)

    def move_y(self, direction=CAMERA_POSITIVE):
        """Mueve la posicion de la camara en el eje y"""
        self.pos.setY(self.pos.getY() + self.cameraVel.getY() * direction)

    def move_z(self, direction=CAMERA_POSITIVE):
        """Mueve la posicion de la camara en el eje z"""
        self.pos.setZ(self.pos.getZ() + self.cameraVel.getZ() * direction)

    def setVelMoveX(self, vel):
        """Define la velocidad de movimiento de la camara en el eje x"""
        self.cameraVel.setX(vel)

    def setVelMoveY(self, vel):
        """Define la velocidad de movimiento de la camara en el eje y"""
        self.cameraVel.setY(vel)

    def setVelMoveZ(self, vel):
        """Define la velocidad de movimiento de la camara en el eje z"""
        self.cameraVel.setZ(vel)

    def setCenterVel(self, vel):
        """Define la velocidad de acercamiento/alejamiento de la camara"""
        self.centervel = Vector3(abs(vel), abs(vel), abs(vel))

    def rotateX(self, ang):
        """Rota la posicion con respecto al eje X"""
        x = self.pos.getX()
        y = self.pos.getY() * cos(ang) - self.pos.getZ() * sin(ang)
        z = self.pos.getY() * sin(ang) + self.pos.getZ() * cos(ang)
        self.pos.setX(x)
        self.pos.setY(y)
        self.pos.setZ(z)

    def rotateY(self, ang):
        """Rota la posicion de la camara con respecto al eje Y"""
        x = self.pos.getX() * cos(ang) + self.pos.getZ() * sin(ang)
        y = self.pos.getY()
        z = -self.pos.getX() * sin(ang) + self.pos.getZ() * cos(ang)
        self.pos.setX(x)
        self.pos.setY(y)
        self.pos.setZ(z)

    def rotateZ(self, ang):
        """Rota la posicion de la camara con respecto al eje Z"""
        x = self.pos.getX() * cos(ang) - self.pos.getY() * sin(ang)
        y = self.pos.getX() * sin(ang) + self.pos.getY() * cos(ang)
        z = self.pos.getZ()
        self.pos.setX(x)
        self.pos.setY(y)
        self.pos.setZ(z)

    def moveCenterX(self, dist):
        """Mueve la coorenada x del centro de vision"""
        self.center.setX(self.center.getX() + dist)

    def moveCenterY(self, dist):
        """Mueve la coorenada y del centro de vision"""
        self.center.setY(self.center.getY() + dist)

    def moveCenterZ(self, dist):
        """Mueve la coorenada z del centro de vision"""
        if (CAMERA_CENTER_LIMIT_Z_DOWN <= self.center.getZ() and dist < 0) or \
                (self.center.getZ() <= CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self.center.setZ(self.center.getZ() + dist)

    def rotateCenterZ(self, angle):
        """Rota la posicion en el eje z"""
        rad = math.sqrt(self.pos.getX() ** 2 + self.pos.getY() ** 2)
        self.pos.setX(rad * cos(self.angle))
        self.pos.setY(rad * sin(self.angle))

    def far(self):
        """Aleja la posicion de la camara
        @deprecated"""
        self.center += self.centervel

    def close(self):
        """Acerca la posicion de la camara
        @deprecated"""
        self.center -= self.centervel

    def getName(self):
        """Retorna el nombre de la camara"""
        return self._name

    # noinspection PyShadowingNames
    def setName(self, name):
        """Define el nombre de la camara"""
        self._name = name


class CameraR(_Camera):
    """Camara en coordenadas esfericas, recibe un radio R, y angulos phi y theta"""

    def __init__(self, r=1.0, phi=45, theta=45, center_point=Point3(), up_vector=Vector3(0, 0, 1)):
        """Funcion constructora"""
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
                        self.rvel = CAMERA_DEFAULT_RVEL
                        self._name = "unnamed"
                    else:
                        raise Exception("el angulo phi debe variar entre 0 y 360, theta debe variar entre 0 y 180")
                else:
                    raise Exception("El radio debe ser mayor a cero""")
            else:
                raise Exception("up_vector debe ser del tipo vector3")
        else:
            raise Exception("center_point debe ser del tipo point3")

    def setRvel(self, vel):
        """Define la velocidad radial con la que la camara se mueve"""
        if vel > 0:
            self.rvel = vel
        else:
            raise Exception("la velocidad debe ser mayor a cero")

    def place(self):
        """Ubica la camara en el mundo"""
        glLoadIdentity()
        gluLookAt(self.r * sin(self.theta) * cos(self.phi), self.r * sin(self.theta) * sin(self.phi),
                  self.r * cos(self.theta),
                  self.center.getX(), self.center.getY(), self.center.getZ(), self.up.getX(), self.up.getY(),
                  self.up.getZ())

    def __str__(self):
        """Retorna el estado de la camara"""
        x, y, z = self.convertoXYZ()
        r = CAMERA_ROUNDED
        msg = 'Camera: {12}\nRadius: {0}\nPhi angle: {1}, Theta angle: {2}\nXYZ eye pos: ({3},{4},{5})\nXYZ center ' \
              'pos: ({6},{7},{8})\nXYZ up vector: ({9},{10},{11})'
        return msg.format(round(self.r, r), round(self.phi, r), round(self.theta, r), round(x, r), round(y, r),
                          round(z, r), round(self.center.getX(), r), round(self.center.getY(), r),
                          round(self.center.getZ(), r), round(self.up.getX(), r), round(self.up.getY(), r),
                          round(self.up.getZ(), r), self.getName())

    def far(self):
        """Aleja la camara"""
        self.r += self.rvel

    def close(self):
        """Aleja la camara"""
        self.r -= self.rvel

    def rotateX(self, angle):
        """Rota la posicion eye en el eje X cartesiano"""
        # Convierto a (x,y,z)
        x, y, z = self.convertoXYZ()
        # Roto las componentes (x,y,z) segun x en
        xr = x
        yr = y * cos(angle) - z * sin(angle)
        zr = y * sin(angle) + z * cos(angle)
        # Convierto a componentes esfericas y se guardan
        r, phi, theta = XYZtoSPR(xr, yr, zr)
        self.r = r
        self.phi = phi
        self.theta = theta

    def rotateY(self, angle):
        """Rota la posicion eye en el eje Y cartesiano"""
        self.theta = min(max(self.theta + angle, CAMERA_MIN_THETA_VALUE), 180)

    def rotateZ(self, angle):
        """Rota la posicion eye en el eje Z cartesiano"""
        self.phi = (self.phi + angle) % 360

    def convertoXYZ(self):
        """Convierte el sistema esferico a cartesiano"""
        return SPRtoXYZ(self.r, self.phi, self.theta)

    def moveCenterX(self, dist):
        """Mueve la coorenada x del centro de vision"""
        self.center.setX(self.center.getX() + dist)

    def moveCenterY(self, dist):
        """Mueve la coorenada y del centro de vision"""
        self.center.setY(self.center.getY() + dist)

    def moveCenterZ(self, dist):
        """Mueve la coorenada z del centro de vision"""
        if (CAMERA_CENTER_LIMIT_Z_DOWN <= self.center.getZ() and dist < 0) or \
                (self.center.getZ() <= CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self.center.setZ(self.center.getZ() + dist)

    def getName(self):
        """Retorna el nombre de la camara"""
        return self._name

    # noinspection PyShadowingNames
    def setName(self, name):
        """Define el nombre de la camara"""
        self._name = name

    def getRadius(self):
        """Retorna el radio de la camara"""
        return self.r

    def setRadius(self, r):
        """Define el radio de la camara"""
        self.r = r

    def getPhi(self):
        """Retorna el angulo phi"""
        return self.phi

    def setPhi(self, phi):
        """Define el angulo phi"""
        self.phi = phi

    def getTheta(self):
        """Retorna el angulo theta"""
        return self.theta

    def setTheta(self, theta):
        """Define el angulo theta"""
        self.theta = theta
