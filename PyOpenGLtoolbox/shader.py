# coding=utf-8
"""
PYOPENGL-TOOLBOX SHADER
Shader management.

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
from ctypes import c_float as _cfloat

# noinspection PyPep8Naming
import OpenGL.GL as _gl

# Constants
_SHADER_DEFAULT_PROGRAM = 0
_SHADER_FRAGMENT = 0x01
_SHADER_VERTEX = 0x02


class Shader:
    """
    Shader class, can load an compile GLSL shaders.
    """

    def __init__(self, path, shader_type, do_compile=False, format_list=None):
        """
        Constructor.

        :param path: Shader path
        :param shader_type: Shader type
        :param do_compile: Compile after load
        :param format_list: Format list
        :type path: basestring
        :type shader_type: int
        :type do_compile: bool
        :type format_list: list
        """
        if shader_type == _SHADER_FRAGMENT or shader_type == _SHADER_VERTEX:
            self._compiled = False
            self._file = str(self.load(path))
            self._path = path
            self._shader = None
            self._shader_type = shader_type
            if format_list is not None:
                if type(format_list) is list:
                    num = 0
                    for f in format_list:
                        key = '{' + str(num) + '}'
                        if key in self._file:
                            self._file = self._file.replace(key, str(f))
                        num += 1
                else:
                    raise Exception('format_list must be list type')
        else:
            raise Exception('Shader invalid, must be FRAGMENT or VERTEX')
        if do_compile:
            self.compile()

    def compile(self):
        """
        Compiles loaded shader.
        """
        if not self.is_compiled():
            if self._file is not None:
                try:
                    if self._shader_type == _SHADER_VERTEX:
                        self._shader = _gl.glCreateShader(_gl.GL_VERTEX_SHADER)
                    else:
                        self._shader = _gl.glCreateShader(_gl.GL_FRAGMENT_SHADER)
                    _gl.glShaderSource(self._shader, self._file)
                    _gl.glCompileShader(self._shader)
                    self._compiled = True
                except:
                    raise Exception('Error when compilin shader')
            else:
                raise Exception('File not loaded')
        else:
            raise Exception('File already been compiled')

    @staticmethod
    def load(path):
        """
        Loads an file an turns into string.

        :param path: File
        :type path: basestring
        :return: File as string
        :rtype: basestring
        """
        try:
            f = open(path)
            program = ''
            for i in f:
                program += i
            return program
        except:
            raise Exception('File {0} does not exist'.format(path))

    def get_compiled(self):
        """
        Returns compiled shader.

        :return: Shader object
        """
        if self.is_compiled():
            return self._shader
        else:
            raise Exception('Shader has not been compiled yet')

    def get_type(self):
        """
        Return shader type.

        :return: Shader type
        :rtype: int
        """
        return self._shader_type

    def get_path(self):
        """
        Returns shader path.

        :return: Shader path
        :rtype: basestring
        """
        return self._path

    def is_compiled(self):
        """
        Check if shader is compiled.

        :return: Shader is compiled
        :rtype: bool
        """
        return self._compiled

    def __str__(self):
        """
        Returns shader status.

        :return: Shader status
        :rtype: basestring
        """
        if self.get_type() == _SHADER_FRAGMENT:
            t = 'FRAGMENT'
        else:
            t = 'VERTEX'
        if not self.is_compiled():
            s = 'not compiled'
        else:
            s = 'compiled'
        return 'File: {0}\nType: {1}\nStatus: {2}\n'.format(self.get_path(), t, s)

    def print_shader(self):
        """
        Print shader source code.
        """
        print(self._file)


class ShaderProgram:
    """
    ShaderProgram class, contains fragment and shader code that runs in background.
    """

    def __init__(self, vertex_shader=None, fragment_shader=None, do_compile=False):
        """
        Constructor.

        :param vertex_shader: Vertex shader
        :param fragment_shader: Fragment shader
        :param do_compile: Compile instantly
        :type vertex_shader: Shader
        :type fragment_shader: Shader
        :type do_compile: bool
        """
        self._compiled = False
        self._enabled = True
        self._fshader = None
        self._name = 'unnamed'
        self._program = None
        self._vshader = None
        if vertex_shader is not None or fragment_shader is not None:
            self.set_fragment_shader(fragment_shader)
            self.set_vertex_shader(vertex_shader)
        if do_compile:
            self.compile()

    def get_fragment_shader(self):
        """
        Returns fragment shader.

        :return: Fragment shader
        :rtype: Shader
        """
        return self._fshader

    def get_vertex_shader(self):
        """
        Returns vertex shader.

        :return: Vertex shader
        :rtype: Shader
        """
        return self._vshader

    def set_fragment_shader(self, fragment):
        """
        Set fragment shader.

        :param fragment: Shader object
        :type fragment: Shader
        """
        if isinstance(fragment, Shader):
            if fragment.get_type() == _SHADER_FRAGMENT:
                self._fshader = fragment
            else:
                raise Exception('Expected fragment shader, but vertex Shader was given')
        else:
            raise Exception('fragment must be Shader object')

    def set_vertex_shader(self, vertex):
        """
        Set vertex shader.

        :param vertex: Shader object
        :type vertex: Shader
        """
        if isinstance(vertex, Shader):
            if vertex.get_type() == _SHADER_VERTEX:
                self._vshader = vertex
            else:
                raise Exception('Expected vertex shader, but fragment Shader was given')
        else:
            raise Exception('vertex must be Shader object')

    def compile(self):
        """
        Compiles.
        """
        if not self.is_compiled():
            self._program = _gl.glCreateProgram()
            _gl.glAttachShader(self._program, self._fshader.get_compiled())
            _gl.glAttachShader(self._program, self._vshader.get_compiled())

            _gl.glValidateProgram(self._program)
            _gl.glLinkProgram(self._program)

            _gl.glDeleteShader(self._fshader.get_compiled())
            _gl.glDeleteShader(self._vshader.get_compiled())

            self._compiled = True
        else:
            raise Exception('Program already been compiled')

    def is_compiled(self):
        """
        Check if the program is compiled.

        :return: Compile status
        :rtype: bool
        """
        return self._compiled

    def get_compiled(self):
        """
        Returns compiled program.

        :return: Program
        """
        if self.is_compiled():
            return self._program
        else:
            raise Exception('Program has not been compiled yet')

    def get_name(self):
        """
        Returns program name.

        :return: Name
        :rtype: basestring
        """
        return self._name

    def set_name(self, n):
        """
        Set program name.

        :param n: Name
        :type n: basestring
        """
        self._name = n

    def __str__(self):
        """
        Returns program status.

        :return: String
        :rtype: basestring
        """
        if self._fshader is None:
            f = 'not defined'
        else:
            f = self._fshader.get_path()
        if self._vshader is None:
            v = 'not defined'
        else:
            v = self._vshader.get_path()
        if self._enabled:
            e = 'enabled'
        else:
            e = 'disabled'
        if self.is_compiled():
            c = 'compiled | {0}'.format(e)
        else:
            c = 'not compiled | {0}'.format(e)
        return 'shader: {3}\nfragment shader: {0}\nvertex shader: {1}\nstatus: {2}'.format(
            f, v, c, self.get_name())

    def start(self):
        """
        Start program.
        """
        if self.is_compiled():
            try:
                if self._enabled:
                    _gl.glUseProgram(self._program)
            except:
                raise Exception('Error executing program')
        else:
            raise Exception('Program has not been compiled yet')

    def stop(self):
        """
        Stop program.
        """
        if self.is_compiled():
            _gl.glUseProgram(0)
        else:
            raise Exception('Program has not been compiled yet')

    def enable(self):
        """
        Enables the program.
        """
        self._enabled = True

    def disable(self):
        """
        Disables the program.
        """
        self._enabled = False

    def get_status(self):
        """
        Get enable status.

        :return: Bool
        :rtype: bool
        """
        return self._enabled

    def uniformf(self, n, *vals):
        """
        Binds an uniform float value to the program.

        :param n: Index
        :param vals: Value
        """
        if len(vals) in range(1, 5) and self.get_status():
            {1: _gl.glUniform1f,
             2: _gl.glUniform2f,
             3: _gl.glUniform3f,
             4: _gl.glUniform4f
             }[len(vals)](_gl.glGetUniformLocation(self._program, n), *vals)

    def uniformi(self, n, *vals):
        """
        Binds an uniform int value to the program.

        :param n: Index
        :param vals: Value
        """
        if len(vals) in range(1, 5) and self.get_status():
            {1: _gl.glUniform1i,
             2: _gl.glUniform2i,
             3: _gl.glUniform3i,
             4: _gl.glUniform4i
             }[len(vals)](_gl.glGetUniformLocation(self._program, n), *vals)

    def uniform_matrixf(self, n, mat):
        """
        Binds an uniform matrix value to the program.

        :param n: Index
        :param mat: Matrix
        """
        if self.get_status():
            loc = _gl.glGetUniformLocation(self._program, n)
            # noinspection PyCallingNonCallable,PyTypeChecker
            _gl.glUniformMatrix4fv(loc, 1, False, (_cfloat * 16)(*mat))


def load_shader(shaderpath, shadername, vertex_format_list=None, fragment_formatlist=None):
    """
    Loads an shader.

    :param shaderpath: Shader path
    :param shadername: Shader name
    :param vertex_format_list: Vertex format list
    :param fragment_formatlist: Fragment format list
    :type shaderpath: basestring
    :type shadername: basestring
    :type vertex_format_list: list
    :type fragment_formatlist: list
    :return: ShaderProgram object
    :rtype: ShaderProgram
    """
    shadername = shadername.replace('.fsh', '').replace('.vsh', '')
    fragment = Shader(shaderpath + shadername + '.fsh', _SHADER_FRAGMENT, True, fragment_formatlist)
    vertex = Shader(shaderpath + shadername + '.vsh', _SHADER_VERTEX, True, vertex_format_list)
    return ShaderProgram(vertex, fragment, True)
