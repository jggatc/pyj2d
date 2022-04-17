#PyJ2D - Python-to-Java Multimedia Framework
#Copyright (c) 2011 James Garnon
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
#PyJ2D version 0.32
#Project Site: https://gatc.ca/


from pyj2d import env
from pyj2d import util
from pyj2d.display import Display
from pyj2d.surface import Surface
from pyj2d.rect import Rect
from pyj2d.image import Image
from pyj2d.event import Event
from pyj2d.key import Key
from pyj2d.mouse import Mouse
from pyj2d.color import Color
from pyj2d.mixer import Mixer
from pyj2d.time import Time
from pyj2d.vector import Vector2
from pyj2d import draw
from pyj2d import transform
from pyj2d import surface
from pyj2d import surfarray
from pyj2d import mask
from pyj2d import font
from pyj2d import sprite
from pyj2d import cursors
from pyj2d.constants import *


def init():
    """
    Initialize module.
    """
    global time, display, image, event, key, mouse, mixer, error, initialized
    try:
        if initialized:
            return
    except NameError:
        initialized = True
    event = Event()
    env.event = event
    time = Time()
    display = Display()
    image = Image()
    key = Key()
    mouse = Mouse()
    mixer = Mixer()
    error = None
    return

init()


def quit():
    """
    Uninitialize module.
    """
    global display, sprite, image, time, event, key, mouse, font, mask, mixer, initialized
    if not initialized:
        return
    else:
        initialized = False
    try:
        mixer.quit()
    except:
        pass
    time._stop_timers()
    for module in (display, sprite, image, time, event, key, mouse, font, mask, mixer):
        del(module)
    if env.jframe:
        env.jframe.stop()


def bounding_rect_return(setting):
    """
    Set whether blit/draw return bounding Rect.
    Setting (bool) defaults to True on module initialization.
    """
    surface.bounding_rect_return(setting)
    draw.bounding_rect_return(setting)

