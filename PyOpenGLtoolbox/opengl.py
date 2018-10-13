# coding=utf-8
"""
PYOPENGL-TOOLBOX OPENGL_LIB
Manage OpenGL libraries, init system.

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
from PyOpenGLtoolbox.utils import print_gl_error
from OpenGL.GLU import gluPerspective as _gluPerspective

# noinspection PyPep8Naming
import OpenGL.GL as _gl

# Constants
_DEFAULT_AMBIENT_COLOR = [0.2, 0.2, 0.2, 1.0]
_DEFAULT_BGCOLOR = [0.0, 0.0, 0.0, 1.0]
_DEFAULT_BGDEPTH = 1.0
_DEFAULT_CONSTANT_ATTENUATION = 1.0
_DEFAULT_DIFFUSE_COLOR = [0.8, 0.8, 0.8, 1.0]
_DEFAULT_LINEAR_ATTENUATION = 0.0
_DEFAULT_QUADRATIC_ATTENUATION = 0.0
_DEFAULT_SPECULAR_COLOR = [1.0, 1.0, 1.0, 1.0]
_DEFAULT_SPOT_CUTOFF = 180.0
_DEFAULT_SPOT_DIRECTION = [0.0, 0.0, -1.0, 1.0]
_DEFAULT_SPOT_EXPONENT = 1.0
_OPENGL_CONFIGS = [False]
_SPOT_DIRECTION_ALL = [1.0, 1.0, 1.0, 1.0]


def init_gl(**kwargs):
    """
    Init opengl, params

    antialiasing=true/false (activa el antialiasing, true por defecto)
    bgcolor=color de fondo
    bgdepth=profundidad de dibujo
    depth=true/false (activa el depth map, true por defecto)
    lighting=true/false (activa la iluminacion, false por defecto)
    materialcolor=true/false (activa el color natural de los materiales, true por defecto)
    normalized=true/false (normaliza las normales, true por defecto)
    numlights=1..9 (indica el numero de luces a activar, 0 por defecto)
    perspectivecorr=true/false (activa la correccion de perspectiva, false por defecto)
    polygonfillmode=true/false (indica el rellenar las superficies, true por defecto)
    smooth=true/false (activa el dibujado suave, true por defecto)
    surffil=true/false (activa el rellenado de superficies, true por defecto)
    textures=true/false (activa las texturas, false por defecto)
    transparency=true/false (activa la transparencia de los modelos, true por defecto)
    verbose=true/false (activa el logging, false por defecto)
    version=true/false (imprime la version en pantalla de OpenGL, false por defecto)
    """

    global verbose

    def is_true(value):
        """
        Value is true or not
        :param value:
        :return:
        """
        if kwargs.get(value) is not None:
            return kwargs.get(value)
        else:
            return False

    # Se define el verbose
    if is_true('verbose'):
        verbose = True
    else:
        verbose = False

    def log(msg):
        """
        Print a message on screen
        :param msg:
        :return:
        """
        if verbose:
            print('[GL] {0}'.format(msg))

    def log_info(msg):
        """
        Print information on screen
        :param msg:
        :return:
        """
        print('[GL-INFO] {0}'.format(msg))

    log('Init OPENGL')

    # Print OpenGL version
    if is_true('version'):
        log_info('GPU {0}'.format(_gl.glGetString(_gl.GL_VENDOR)))
        log_info('Renderer {0}'.format(_gl.glGetString(_gl.GL_RENDERER)))
        log_info('OpenGL version {0}'.format(_gl.glGetString(_gl.GL_VERSION)))
        log_info('SLSL version {0}'.format(_gl.glGetString(_gl.GL_SHADING_LANGUAGE_VERSION)))
        log_info('Extensions {0}'.format(_gl.glGetString(_gl.GL_EXTENSIONS)))

    # Set background clear color
    if kwargs.get('bgcolor') is not None:
        log('Clear color set: {0}'.format(kwargs.get('bgcolor')))
        _gl.glClearColor(*kwargs.get('bgcolor'))
    else:
        log('Clear color set default')
        _gl.glClearColor(*_DEFAULT_BGCOLOR)

    # Set clear depth color
    if kwargs.get('bgdepth') is not None:
        log('Clear depth color set: {0}'.format(kwargs.get("bgdepth")))
        _gl.glClearDepth(kwargs.get('bgdepth'))
    else:
        log('Clear depth color set default')
        _gl.glClearDepth(_DEFAULT_BGDEPTH)

    # Enable transparency
    if is_true('transparency'):
        log('Transparency enabled')
        _gl.glEnable(_gl.GL_BLEND)
        _gl.glBlendFunc(_gl.GL_SRC_ALPHA, _gl.GL_ONE_MINUS_SRC_ALPHA)

    # Smooth
    if is_true('smooth'):
        log('Enable SMOOTH shade model')
        _gl.glShadeModel(_gl.GL_SMOOTH)

    # Depth test
    if is_true('depth'):
        log('Enable depth test')
        _gl.glEnable(_gl.GL_DEPTH_TEST)
        _gl.glDepthFunc(_gl.GL_LEQUAL)

    # Antialiasing
    if is_true('antialiasing'):
        log('Antialiasing enabled')
        _gl.glHint(_gl.GL_POLYGON_SMOOTH_HINT, _gl.GL_NICEST)

    # Enabled normalized normal
    if is_true('normalized'):
        log('Normalized normal enabled')
        _gl.glEnable(_gl.GL_NORMALIZE)

    # Enable offset fill
    if is_true('surffill'):
        log('Enabled polygon offset fill')
        _gl.glEnable(_gl.GL_POLYGON_OFFSET_FILL)

    # Enable lighting
    if kwargs.get('lighting') is not None and kwargs.get('lighting'):
        log('Enable lighting')
        _gl.glEnable(_gl.GL_LIGHTING)
        if kwargs.get('numlights') is not None:
            total = int(kwargs.get('numlights'))
            for light in range(total):
                log('Light {0} enabled'.format(light))
                eval('glEnable(GL_LIGHT{0})'.format(light))
        _OPENGL_CONFIGS[0] = True

    # Polygon fill mode
    if is_true('polygonfillmode'):
        log('Enabled polygoon fill by both sides')
        _gl.glPolygonMode(_gl.GL_FRONT_AND_BACK, _gl.GL_FILL)

    # Enable color material
    if is_true('materialcolor'):
        log('Enabled color material')
        _gl.glEnable(_gl.GL_COLOR_MATERIAL)

    # Enable perspective correction
    if is_true('perspectivecorr'):
        log('Enabled pespective correction')
        _gl.glHint(_gl.GL_PERSPECTIVE_CORRECTION_HINT, _gl.GL_NICEST)

    # Enable textures
    if is_true("textures"):
        log('Textures enabled')
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glLightModeli(_gl.GL_LIGHT_MODEL_COLOR_CONTROL, _gl.GL_SEPARATE_SPECULAR_COLOR)

    log('OpenGL init finished')


def clear_buffer():
    """
    Clear buffer
    :return:
    """
    _gl.glClear(_gl.GL_COLOR_BUFFER_BIT | _gl.GL_DEPTH_BUFFER_BIT)


def reshape(w, h, fov=60, nearplane=10, farplane=10000):
    """
    Reshape OpenGL window
    :param w: Window width
    :param h: Window height
    :param fov: Field of view
    :param nearplane: Near plane
    :param farplane: Far plane
    :return:
    """
    h = max(h, 1)
    _gl.glLoadIdentity()

    # Create viewport
    _gl.glViewport(0, 0, w, h)
    _gl.glMatrixMode(_gl.GL_PROJECTION)

    # Create perspective camera
    _gluPerspective(fov, float(w) / float(h), nearplane, farplane)

    # Set model mode
    _gl.glMatrixMode(_gl.GL_MODELVIEW)
    _gl.glLoadIdentity()


def init_light(light=None, *args, **kwargs):
    """
    Set light properties
    light: light to init, type GL_LIGHTn, n=0..8

    Valid parameters:
    ambient: color ambiente rgba
    diffuse: color difuso rgba
    specular: color especular rgba
    spot_cutoff: angulo de enfoque
    spot_exponent: exponente del enfoque
    spot_direction: direccion de enfoque
    constant_att: atenuacion constante
    linear_att: atenuacion linear
    quad_att: atenuacion cuadratica
    """

    if light is None:
        print_gl_error('Light cannot be None')

    # Ambient color
    if kwargs.get('ambient') is not None:
        _gl.glLightfv(light, _gl.GL_AMBIENT, kwargs.get('ambient'))
    else:
        _gl.glLightfv(light, _gl.GL_AMBIENT, _DEFAULT_AMBIENT_COLOR)

    # Diffuse color
    if kwargs.get('diffuse') is not None:
        _gl.glLightfv(light, _gl.GL_DIFFUSE, kwargs.get('diffuse'))
    else:
        _gl.glLightfv(light, _gl.GL_DIFFUSE, _DEFAULT_DIFFUSE_COLOR)

    # Specular color
    if kwargs.get('specular') is not None:
        _gl.glLightfv(light, _gl.GL_SPECULAR, kwargs.get('specular'))
    else:
        _gl.glLightfv(light, _gl.GL_SPECULAR, _DEFAULT_SPECULAR_COLOR)

    # Cutoff
    if kwargs.get('spot_cutoff') is not None:
        _gl.glLightfv(light, _gl.GL_SPOT_CUTOFF, kwargs.get('spot_cutoff'))
    else:
        _gl.glLightfv(light, _gl.GL_SPOT_CUTOFF, _DEFAULT_SPOT_CUTOFF)

    # Exponent
    if kwargs.get('spot_exponent') is not None:
        _gl.glLightfv(light, _gl.GL_SPOT_EXPONENT, kwargs.get('spot_exponent'))
    else:
        _gl.glLightfv(light, _gl.GL_SPOT_EXPONENT, _DEFAULT_SPOT_EXPONENT)

    # Spot direction
    if kwargs.get('spot_direction') is not None:
        _gl.glLightfv(light, _gl.GL_SPOT_DIRECTION, kwargs.get('spot_direction'))
    else:
        _gl.glLightfv(light, _gl.GL_SPOT_DIRECTION, _DEFAULT_SPOT_DIRECTION)

    # Constant attenuation factor
    if kwargs.get('constant_att') is not None:
        _gl.glLightfv(light, _gl.GL_CONSTANT_ATTENUATION, kwargs.get('constant_att'))
    else:
        _gl.glLightfv(light, _gl.GL_CONSTANT_ATTENUATION, _DEFAULT_CONSTANT_ATTENUATION)

    # Lineal attenuation factor
    if kwargs.get('linear_att') is not None:
        _gl.glLightfv(light, _gl.GL_LINEAR_ATTENUATION, kwargs.get('linear_att'))
    else:
        _gl.glLightfv(light, _gl.GL_LINEAR_ATTENUATION, _DEFAULT_LINEAR_ATTENUATION)

    # Quadratic attenuation
    if kwargs.get('quad_att') is not None:
        _gl.glLightfv(light, _gl.GL_QUADRATIC_ATTENUATION, kwargs.get('quad_att'))
    else:
        _gl.glLightfv(light, _gl.GL_QUADRATIC_ATTENUATION, _DEFAULT_QUADRATIC_ATTENUATION)


def is_light_enabled():
    """
    Check if lights are enabled
    :return:
    """
    return _OPENGL_CONFIGS[0]
