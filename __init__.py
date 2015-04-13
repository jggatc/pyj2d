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

from display import Display
from surface import Surface
from rect import Rect
from image import Image
from draw import Draw
from event import Event
from key import Key
from mouse import Mouse
from transform import Transform
from surfarray import Surfarray
from color import Color
from mixer import Mixer
import time
import mask
import font
import sprite
from locals import *


def init():
    """
    Initialize module.
    """
    global display, image, draw, event, key, mouse, transform, surfarray, mixer, error, initialized
    try:
        if initialized:
            return
    except NameError:
        initialized = True
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

