# coding=utf-8
"""
SHADER
Provee funciones para el manejo de shaders.

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

# Importación de librerías
from OpenGL.GL import *
import ctypes
import types

# Constantes
DEFAULT_PROGRAM = 0
FRAGMENT = 0x01
VERTEX = 0x02


class Shader:
    """Permite cargar y compilar shaders"""

    # noinspection PyShadowingBuiltins
    def __init__(self, path, tipo, compile=False, formatlist=None):
        """Constructor"""
        if tipo == FRAGMENT or tipo == VERTEX:
            self.shader = None
            self.file = str(self.load(path))
            self.tipo = tipo
            self.path = path
            self.compiled = False
            if formatlist is not None:
                if isinstance(formatlist, types.ListType):
                    num = 0
                    for f in formatlist:
                        key = '{' + str(num) + '}'
                        if key in self.file:
                            self.file = self.file.replace(key, str(f))
                        num += 1
                else:
                    raise Exception("el tipo de formatlist debe ser del tipo list")
        else:
            raise Exception("tipo de shader incorrecto, debe ser FRAGMENT o VERTEX")
        if compile:
            self.compile()

    def compile(self):
        """Compila el shader cargado"""
        if not self.isCompiled():
            if self.file is not None:
                try:
                    if self.tipo == VERTEX:
                        self.shader = glCreateShader(GL_VERTEX_SHADER)
                    else:
                        self.shader = glCreateShader(GL_FRAGMENT_SHADER)
                    glShaderSource(self.shader, self.file)
                    glCompileShader(self.shader)
                    self.compiled = True
                except:
                    raise Exception("error al compilar el shader")
            else:
                raise Exception("no se ha cargado un archivo")
        else:
            print "Error :: el shader ya ha sido compilado"

    # noinspection PyMethodMayBeStatic
    def load(self, path):
        """Carga un archivo y lo convierte a un string"""
        try:
            f = open(path, "r")
            program = ""
            for i in f:
                program += i
            return program
        except:
            raise Exception("el archivo no existe")

    def getCompiled(self):
        """Retorna el programa compilado"""
        if self.isCompiled():
            return self.shader
        else:
            raise Exception("el shader no ha sido compilado aun")

    def getType(self):
        """Retorna el tipo de shader"""
        return self.tipo

    def getPath(self):
        """Retorna la ubicacion del shader"""
        return self.path

    def isCompiled(self):
        """Retorna true/false si el shader se ha compilado o no"""
        return self.compiled

    def __str__(self):
        """Retorna el estado del shader"""
        if self.getType() == FRAGMENT:
            t = "FRAGMENT"
        else:
            t = "VERTEX"
        if not self.isCompiled():
            s = "not compiled"
        else:
            s = "compiled"
        return "file: {0}\ntype: {1}\nstatus: {2}\n".format(self.getPath(), t, s)

    def printShader(self):
        """Imprime el codigo fuente del shader"""
        print self.file


# noinspection PyShadowingNames,PyCallingNonCallable,PyTypeChecker
class ShaderProgram:
    """Permite la creacion de un programa que ejecutara shaders en segundo plano"""

    # noinspection PyShadowingBuiltins
    def __init__(self, vertex_shader=None, fragment_shader=None, compile=False):
        """Funcion constructora"""
        self.fshader = None
        self.vshader = None
        if vertex_shader is not None or fragment_shader is not None:
            self.setFragmentShader(fragment_shader)
            self.setVertexShader(vertex_shader)
        self.program = None
        self.compiled = False
        self.name = "shader-name"
        if compile:
            self.compile()
        self.enabled = True

    def getFragmentShader(self):
        """Retorna el fragment shader"""
        return self.fshader

    def getVertexShader(self):
        """Retorna el vertex shader"""
        return self.vshader

    def setFragmentShader(self, fragment):
        """Define el fragment shader"""
        if isinstance(fragment, Shader):
            if fragment.getType() == FRAGMENT:
                self.fshader = fragment
            else:
                raise Exception("se esperaba un fragment shader, en cambio se paso un vertex shader")
        else:
            raise Exception("el fragment shader debe ser del tipo Shader")

    def setVertexShader(self, vertex):
        """Define el vertex shader"""
        if isinstance(vertex, Shader):
            if vertex.getType() == VERTEX:
                self.vshader = vertex
            else:
                raise Exception("se esperaba un vertex shader, en cambio se paso un fragment shader")
        else:
            raise Exception("el vertex shader debe ser del tipo Shader")

    def compile(self):
        """Compila el programa"""
        if not self.isCompiled():
            self.program = glCreateProgram()
            glAttachShader(self.program, self.fshader.getCompiled())
            glAttachShader(self.program, self.vshader.getCompiled())

            glValidateProgram(self.program)
            glLinkProgram(self.program)

            glDeleteShader(self.fshader.getCompiled())
            glDeleteShader(self.vshader.getCompiled())

            self.compiled = True
        else:
            print "Error :: el programa ya ha sido compilado"

    def isCompiled(self):
        """Retorna true/false si el programa ha sido compilado"""
        return self.compiled

    def getCompiled(self):
        """Retorna el programa compilado"""
        if self.isCompiled():
            return self.program
        else:
            raise Exception("el programa no ha sido compilado aun")

    def getName(self):
        """Retorna el nombre del programa"""
        return self.name

    def setName(self, name):
        """Define el nombre del programa"""
        self.name = name

    def __str__(self):
        """Retorna el estado del programa"""
        if self.fshader is None:
            f = "not defined"
        else:
            f = self.fshader.getPath()
        if self.vshader is None:
            v = "not defined"
        else:
            v = self.vshader.getPath()
        if self.enabled:
            e = "enabled"
        else:
            e = "disabled"
        if self.isCompiled():
            c = "compiled | {0}".format(e)
        else:
            c = "not compiled | {0}".format(e)
        return "shader: {3}\nfragment shader: {0}\nvertex shader: {1}\nstatus: {2}".format(f, v, c, self.getName())

    def start(self):
        """Usa el programa"""
        if self.isCompiled():
            try:
                if self.enabled:
                    glUseProgram(self.program)
            except:
                raise Exception("error al ejecutar el programa")
        else:
            raise Exception("el programa no ha sido compilado aun")

    def stop(self):
        """Detiene la ejecucion de programa"""
        if self.isCompiled():
            glUseProgram(0)
        else:
            raise Exception("el programa no ha sido compilado aun")

    def enable(self):
        """Activa el shader"""
        self.enabled = True

    def disable(self):
        """Desactiva el shader"""
        self.enabled = False

    def getStatus(self):
        """Retorna si el shader esta activado o desactivado"""
        return self.enabled

    def uniformf(self, name, *vals):
        """Carga un numero flotante al programa"""
        if len(vals) in range(1, 5) and self.getStatus():
            {1: glUniform1f,
             2: glUniform2f,
             3: glUniform3f,
             4: glUniform4f
             }[len(vals)](glGetUniformLocation(self.program, name), *vals)

    def uniformi(self, name, *vals):
        """Carga un numero entero al programa"""
        if len(vals) in range(1, 5) and self.getStatus():
            {1: glUniform1i,
             2: glUniform2i,
             3: glUniform3i,
             4: glUniform4i
             }[len(vals)](glGetUniformLocation(self.program, name), *vals)

    def uniform_matrixf(self, name, mat):
        """Carga una matriz uniforme al programa"""
        if self.getStatus():
            loc = glGetUniformLocation(self.program, name)
            glUniformMatrix4fv(loc, 1, False, (ctypes.c_float * 16)(*mat))


def loadShader(shaderpath, shadername, vertex_format_list=None, fragment_formatlist=None):
    """Funcion que carga un shader y retorna un objeto del tipo ShaderProgram"""
    fragment = Shader(shaderpath + shadername + ".fsh", FRAGMENT, True, fragment_formatlist)
    vertex = Shader(shaderpath + shadername + ".vsh", VERTEX, True, vertex_format_list)
    return ShaderProgram(vertex, fragment, True)
