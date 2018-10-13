# coding=utf-8
"""
PYOPENGL-TOOLBOX TEXTURES
Texture functions.

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
import numpy as _np

# noinspection PyPep8Naming
import OpenGL.GL as _gl

try:
    from PIL import Image as _Image
except ImportError:
    print('[ERR] Error importing PIL, trying Image')
    # noinspection PyBroadException
    try:
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        import Image as _Image
    except:
        print('[ERR] Error importing Image, this PyOpenGLtoolbox needs Pillow')
        exit()


def load_texture(image_file, repeat=False):
    """
    Loads an texture from a image file.

    :param image_file: Image file
    :param repeat: Repeat image (OPENGL)
    :type image_file: basestring:
    :type repeat: bool
    :return: Image OpenGL object
    """
    img = _Image.open(image_file)
    data = _np.array(list(img.getdata()), _np.int8)

    tex = _gl.glGenTextures(1)
    _gl.glPixelStorei(_gl.GL_UNPACK_ALIGNMENT, 1)
    _gl.glBindTexture(_gl.GL_TEXTURE_2D, tex)

    if repeat:
        _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_S, _gl.GL_REPEAT)
        _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_T, _gl.GL_REPEAT)
    else:
        _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_S, _gl.GL_CLAMP)
        _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_WRAP_T, _gl.GL_CLAMP)

    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_MAG_FILTER, _gl.GL_LINEAR)
    _gl.glTexParameterf(_gl.GL_TEXTURE_2D, _gl.GL_TEXTURE_MIN_FILTER, _gl.GL_LINEAR)
    _gl.glTexImage2D(_gl.GL_TEXTURE_2D, 0, _gl.GL_RGB, img.size[0], img.size[1], 0, _gl.GL_RGB,
                     _gl.GL_UNSIGNED_BYTE, data)
    _gl.glTexEnvf(_gl.GL_TEXTURE_ENV, _gl.GL_TEXTURE_ENV_MODE, _gl.GL_MODULATE)
    return tex
