#PyJ2D - Copyright (C) 2011 James Garnon

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#PyJ2D version 0.22
#Download Site: http://gatc.ca

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
from color import Color     #0.23
import time
import mask
import font
import sprite
from locals import *


def init():
    """
    Initialize module.
    """
    global display, image, draw, event, key, mouse, transform, surfarray, error, initialized
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
    error = None
    return

init()


def quit():
    """
    Uninitialize module.
    """
    global display, sprite, image, draw, time, event, key, mouse, transform, font, surfarray, mask, initialized
    if not initialized:
        return
    else:
        initialized = False
    for module in (display, sprite, image, draw, time, event, key, mouse, transform, font, surfarray, mask):
        del(module)
    if not env.japplet:
        env.jframe.dispose()

