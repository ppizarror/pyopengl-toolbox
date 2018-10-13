# coding=utf-8
"""
PYOPENGL-TOOLBOX GLPYTHON
Utilitary function to manage PyOpenGL.

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
from pygame.locals import DOUBLEBUF as _DOUBLEBUF
from pygame.locals import OPENGLBLIT as _OPENGLBLIT
import os as _os
import pygame as _pygame

# Constants
_PYOPENGL_DEFAULT_CAPTION = 'Program title'


def init_pygame(w, h, caption=_PYOPENGL_DEFAULT_CAPTION, icon=None, centered_mouse=False, centered_window=True):
    """
    Init pygame.

    :param w: Window width (px)
    :param h: Window height (px)
    :param caption: Window title
    :param icon: Window icon, pygame Surface object
    :param centered_mouse: Centered mouse
    :param centered_window: Centered window
    :type w: int
    :type h: int
    :type caption: basestring
    :type icon: Surface
    :type centered_mouse: bool
    :type centered_window: bool
    """
    _pygame.init()
    if centered_window:
        _os.environ['SDL_VIDEO_CENTERED'] = '1'
    _pygame.display.set_mode((w, h), _OPENGLBLIT | _DOUBLEBUF)
    _pygame.display.set_caption(caption)
    if centered_mouse:
        _pygame.mouse.set_pos(w / 2, h / 2)
    if icon is not None:
        _pygame.display.set_icon(icon)


def load_image(path, convert=False):
    """
    Loads an image.

    :param path: Imagepath
    :param convert: Convert alpha
    :type path: basestring
    :type convert: bool
    :return: Pygame Surface object
    :rtype: Surface
    """
    # noinspection PyBroadException
    try:
        image = _pygame.image.load(path)
        if convert:
            image = image.convert_alpha()
        return image
    except:
        print('Error when loading <' + path + '> image')
        return None
