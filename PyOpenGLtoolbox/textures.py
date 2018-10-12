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
import numpy
from OpenGL.GL import glGenTextures, GL_UNPACK_ALIGNMENT, glPixelStorei, glBindTexture, GL_TEXTURE_2D, glTexParameterf, \
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TEXTURE_MAG_FILTER, GL_REPEAT, GL_CLAMP, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_RGB, glTexImage2D, GL_UNSIGNED_BYTE, glTexEnvf, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE

try:
    from PIL import Image
except ImportError:
    print('[ERR] Error importing PIL, trying Image')
    # noinspection PyBroadException
    try:
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        import Image
    except:
        print('[ERR] Error importing Image, this PyOpenGLtoolbox needs Pillow')
        exit()


def load_texture(image_file, repeat=False):
    """Carga una textura desde un archivo image_file"""
    img = Image.open(image_file)
    data = numpy.array(list(img.getdata()), numpy.int8)

    tex = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, tex)

    if repeat:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    else:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB,
                 GL_UNSIGNED_BYTE, data)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    return tex
