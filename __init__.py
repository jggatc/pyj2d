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
#PyJ2D version 0.27
#Project Site: http://gatc.ca/

from pyj2d import util
from pyj2d.display import Display
from pyj2d.surface import Surface
from pyj2d.rect import Rect
from pyj2d.image import Image
from pyj2d.draw import Draw
from pyj2d.event import Event
from pyj2d.key import Key
from pyj2d.mouse import Mouse
from pyj2d.transform import Transform
from pyj2d.surfarray import Surfarray
from pyj2d.color import Color
from pyj2d.mixer import Mixer
from pyj2d.time import Time
from pyj2d import mask
from pyj2d import font
from pyj2d import sprite
from pyj2d import cursors
from pyj2d.locals import *


def init():
    """
    Initialize module.
    """
    global time, display, image, draw, event, key, mouse, transform, surfarray, mixer, error, initialized
    try:
        if initialized:
            return
    except NameError:
        initialized = True
    time = Time()
    display = Display()
    image = Image()
    draw = Draw()
    event = Event()
    key = Key()
    mouse = Mouse()
    transform = Transform()
    surfarray = Surfarray()
    mixer = Mixer()
    error = None
    return

init()


def quit():
    """
    Uninitialize module.
    """
    global display, sprite, image, draw, time, event, key, mouse, transform, font, surfarray, mask, mixer, initialized
    if not initialized:
        return
    else:
        initialized = False
    try:
        mixer.quit()
    except:
        pass
    for module in (display, sprite, image, draw, time, event, key, mouse, transform, font, surfarray, mask, mixer):
        del(module)
    if not env.japplet:
        env.jframe.dispose()

