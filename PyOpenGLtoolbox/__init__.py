# coding=utf-8
"""
PYOPENGL-TOOLBOX
Toolbox for PyOpenGL.

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

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.camera import CameraR, CameraXYZ

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.geometry import draw_vertex_list, draw_vertex_list_create_normal, draw_list, \
    draw_vertex_list_create_normal_textured, draw_vertex_list_normal, draw_vertex_list_normal_textured, \
    draw_vertex_list_textured

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.figures import VBObject, load_obj_model, load_gmsh_model, load_gmsh_model, create_circle, \
    create_cone, create_cube, create_cube_solid, create_cube_textured, create_diamond, create_dodecahedron, \
    create_icosahedron, create_octahedron, create_pyramid, create_pyramid_textured, create_pyramid_vbo, create_sphere, \
    create_teapot, create_teapot_textured, create_tetrahedron, create_tetrahedron_vbo, create_torus

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.materials import material_black_plastic, material_black_rubber, material_brass, material_bronze, \
    material_chrome, material_copper, material_cyan_plastic, material_cyan_rubber, material_emerald, material_gold, \
    material_green_plastic, material_green_rubber, material_jade, material_natural_white, material_obsidian, \
    material_pearl, material_red_plastic, material_red_rubber, material_ruby, material_silver, material_turquoise, \
    material_white_plastic, material_white_rubber, material_yellow_plastic, material_yellow_rubber

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.mathlib import Point3, Point2, Vector3

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.opengl import init_gl, init_light, clear_buffer, reshape_window_perspective, is_light_enabled

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.particles import Particle, PARTICLES_OPERATOR_ADD, PARTICLES_OPERATOR_AND, \
    PARTICLES_OPERATOR_DIFF, PARTICLES_OPERATOR_DIV, PARTICLES_OPERATOR_MOD, PARTICLES_OPERATOR_MULT, \
    PARTICLES_OPERATOR_OR, PARTICLES_OPERATOR_POW, PARTICLES_OPERATOR_XOR

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.pyopengl import init_pygame, load_image

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.shader import load_shader, Shader, ShaderProgram

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.textures import load_texture

# noinspection PyUnresolvedReferences
from PyOpenGLtoolbox.utils import create_axes, draw_text

# Base libraries
# noinspection PyUnresolvedReferences
from OpenGL.GL import *
# noinspection PyUnresolvedReferences
from OpenGL.GLU import *
# noinspection PyUnresolvedReferences
from OpenGL.GLUT import *
# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from pygame.locals import *

# Metadata
__author__ = 'Pablo Pizarro @ppizarror.com'
__description__ = 'PyOpenGL toolbox'
__email__ = 'pablo.pizarro@ing.uchile.cl'
__version__ = 'v2.1.0'
__url__ = 'https://github.com/ppizarror/pyopengl-toolbox'
