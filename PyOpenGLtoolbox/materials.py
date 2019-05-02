# coding=utf-8
"""
PYOPENGL-TOOLBOX MATERIALS
Material definitions.

MIT License
Copyright (c) 2015-2019 Pablo Pizarro R.

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
from OpenGL.GL import GL_AMBIENT as _GL_AMBIENT
from OpenGL.GL import GL_DIFFUSE as _GL_DIFFUSE
from OpenGL.GL import GL_EMISSION as _GL_EMISSION
from OpenGL.GL import GL_FRONT_AND_BACK as _GL_FRONT_AND_BACK
from OpenGL.GL import GL_SHININESS as _GL_SHININESS
from OpenGL.GL import GL_SPECULAR as _GL_SPECULAR
from OpenGL.GL import glMaterialfv as _glMaterialfv

# Constants
_MATERIAL_AMBIENT_COLOR_GREEN = [0.0, 0.403, 0.0]
_MATERIAL_AMBIENT_COLOR_PURPLE = [0.203, 0.0, 0.203]
_MATERIAL_AMBIENT_COLOR_RED = [0.403, 0.0, 0.0, 1.0]
_MATERIAL_AMBIENT_COLOR_YELLOW = [0.603, 0.603, 0.0]
_MATERIAL_DEFAULT_EMISSION = [0.0, 0.0, 0.0, 1.0]
_MATERIAL_DIFFUSE_COLOR_GREEN = [0.0, 0.505, 0.0]
_MATERIAL_DIFFUSE_COLOR_PURPLE = [0.301, 0.0, 0.301]
_MATERIAL_DIFFUSE_COLOR_RED = [0.556, 0.0, 0.0, 1.0]
_MATERIAL_DIFFUSE_COLOR_YELLOW = [0.803, 0.803, 0.0]
_MATERIAL_SPECULAR_COLOR_GREEN = [0.0, 0.705, 0.0]
_MATERIAL_SPECULAR_COLOR_PURPLE = [0.505, 0.0, 0.505]
_MATERIAL_SPECULAR_COLOR_RED = [0.858, 0.0, 0.0, 1.0]
_MATERIAL_SPECULAR_COLOR_YELLOW = [0.901, 0.901, 0.0]
_MATERIAL_WHITE_EMISSION = [1.0, 1.0, 1.0, 1.0]


def material_obsidian(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Obsidian material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_SPECULAR, [0.332741, 0.328634, 0.346435, 1.0])
    _glMaterialfv(face, _GL_AMBIENT, [0.05375, 0.05, 0.0625, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.18275, 0.17, 0.25525, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.3 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_silver(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Silver material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.19225, 0.19225, 0.19225, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.50754, 0.50754, 0.50754, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.508273, 0.508273, 0.508273, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.4 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_copper(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Copper material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.19125, 0.0735, 0.0225, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.7038, 0.27048, 0.0828, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.256777, 0.137622, 0.086014, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.1 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_emerald(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Emerald material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0215, 0.1745, 0.0215, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.07568, 0.61424, 0.007568, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.633, 0.727811, 0.633, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.6 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_jade(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Jade material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.135, 0.2225, 0.1575, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.54, 0.89, 0.63, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.316228, 0.316228, 0.316228, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.1 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_pearl(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Pearl material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.25, 0.20725, 0.20725, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [1.0, 0.829, 0.829, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.296648, 0.296648, 0.296648, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.088 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_turquoise(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Torquoise material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.1, 0.18725, 0.1745, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.396, 0.74161, 0.69102, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.29754, 0.30829, 0.306678, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.1 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_ruby(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Ruby material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.1745, 0.01175, 0.01175, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.61424, 0.04136, 0.04136, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.727811, 0.626959, 0.626959, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.6 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_brass(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Brass material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.329, 0.223529, 0.027451, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.780392, 0.568627, 0.113725, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.992157, 0.941176, 0.807843, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.21794872 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_bronze(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Bronze material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.2125, 0.1275, 0.054, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.714, 0.4284, 0.18144, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.393548, 0.271906, 0.166721, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.2 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_chrome(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Chrome material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.25, 0.25, 0.25, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.4, 0.4, 0.4, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.774597, 0.774957, 0.774957, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.6 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_gold(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Gold material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.24725, 0.1995, 0.0745, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.75164, 0.60648, 0.22648, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.628281, 0.555802, 0.366065, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.4 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_black_plastic(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Black plastic material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.01, 0.01, 0.01, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.50, 0.50, 0.50, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.25 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_cyan_plastic(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Cyan plastic material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.1, 0.06, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.0, 0.50980392, 0.50980392, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.50196078, 0.50196078, 0.50196078, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.25 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_green_plastic(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Green plastic material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.1, 0.35, 0.1, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.45, 0.55, 0.45, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.25 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_red_plastic(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Red plastic material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.5, 0.0, 0.0, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.7, 0.6, 0.6, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.25 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_white_plastic(emission=None, face=_GL_FRONT_AND_BACK):
    """
    White plastic material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.55, 0.55, 0.55, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.70, 0.70, 0.70, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.25 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_yellow_plastic(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Yellow plastic material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.5, 0.5, 0.0, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.6, 0.6, 0.5, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.25 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_black_rubber(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Black rubber material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.01, 0.01, 0.1, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.078125 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_cyan_rubber(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Cyan rubber material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.05, 0.05, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.4, 0.5, 0.5, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.04, 0.7, 0.7, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.078125 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_green_rubber(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Green rubber material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.0, 0.05, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.4, 0.5, 0.4, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.04, 0.7, 0.04, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.078125 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_red_rubber(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Red rubber material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.05, 0.0, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.5, 0.4, 0.4, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.7, 0.04, 0.04, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.078125 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_white_rubber(emission=None, face=_GL_FRONT_AND_BACK):
    """
    White rubber material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.7, 0.7, 0.7, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.078125 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_yellow_rubber(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Yellow rubber material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [0.05, 0.05, 0.0, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [0.5, 0.5, 0.4, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [0.7, 0.7, 0.04, 1.0])
    _glMaterialfv(face, _GL_SHININESS, 0.078125 * 128)
    _glMaterialfv(face, _GL_EMISSION, emission)


def material_natural_white(emission=None, face=_GL_FRONT_AND_BACK):
    """
    Natural white material.

    :param emission: Material emission constant
    :param face: Face mode (OpenGL constant)
    :type emission: list
    :type face: int
    """
    if emission is None:
        emission = _MATERIAL_DEFAULT_EMISSION
    _glMaterialfv(face, _GL_AMBIENT, [1, 1, 1, 1.0])
    _glMaterialfv(face, _GL_DIFFUSE, [1, 1, 1, 1.0])
    _glMaterialfv(face, _GL_SPECULAR, [1, 1, 1, 1])
    _glMaterialfv(face, _GL_SHININESS, 128)
    _glMaterialfv(face, _GL_EMISSION, emission)
