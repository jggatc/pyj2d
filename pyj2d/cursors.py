#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from java.awt import Cursor
from pyj2d.surface import Surface
from pyj2d.color import Color
from pyj2d import constants as Const


DEFAULT_CURSOR = Cursor.DEFAULT_CURSOR
CROSSHAIR_CURSOR = Cursor.CROSSHAIR_CURSOR
E_RESIZE_CURSOR = Cursor.E_RESIZE_CURSOR
HAND_CURSOR = Cursor.HAND_CURSOR
MOVE_CURSOR = Cursor.MOVE_CURSOR
N_RESIZE_CURSOR = Cursor.N_RESIZE_CURSOR
NE_RESIZE_CURSOR = Cursor.NE_RESIZE_CURSOR
NW_RESIZE_CURSOR = Cursor.NW_RESIZE_CURSOR
S_RESIZE_CURSOR = Cursor.S_RESIZE_CURSOR
SE_RESIZE_CURSOR = Cursor.SE_RESIZE_CURSOR
SW_RESIZE_CURSOR = Cursor.SW_RESIZE_CURSOR
TEXT_CURSOR = Cursor.TEXT_CURSOR
W_RESIZE_CURSOR = Cursor.W_RESIZE_CURSOR
WAIT_CURSOR = Cursor.WAIT_CURSOR
CUSTOM_CURSOR = Cursor.CUSTOM_CURSOR


#cursors not implemented
arrow = diamond = broken_x = tri_left = tri_right = ()


def compile(strings, black='X', white='.', xor='o'):
    """
    Compile binary data from cursor string.
    Arguments cursor string, and optional symbols representing colors.
    Data represents black and white pixels, xor color defaulting to black.
    Data should be a string list of width divisible by 8.
    Return cursor data and mask, can be used with mouse.set_cursor.
    """
    data = []
    mask = []
    dbit = {black:1, white:0, xor:1}
    mbit = {black:1, white:1, xor:0}
    string = ''.join(strings)
    for i in range(0, len(string), 8):
        s = string[i:i+8]
        db = mb = 0
        if s != '        ':
            for j in range(8):
                c = s[j]
                if c == ' ':
                    continue
                if dbit[c]:
                    db |= 0x01<<7-j
                if mbit[c]:
                    mb |= 0x01<<7-j
        data.append(db)
        mask.append(mb)
    return tuple(data), tuple(mask)


def create_cursor(size, data, mask):
    """
    Create cursor image from binary data.
    Arguments cursor size and its binary data and mask.
    Return surface, can be used with mouse.set_cursor.
    """
    surface = Surface(size, Const.SRCALPHA)
    black = Color(0,0,0,255).getRGB()
    white = Color(255,255,255,255).getRGB()
    x = y = 0
    for i in range(len(data)):
        if data[i] or mask[i]:
            for j in range(8):
                if data[i] & 0x01<<7-j:
                    surface.setRGB(x+j, y, black)
                elif mask[i] & 0x01<<7-j:
                    surface.setRGB(x+j, y, white)
        x += 8
        if x >= size[0]:
            x = 0
            y += 1
    return surface


def get_cursor_types():
    #https://docs.oracle.com/javase/8/docs/api/java/awt/Cursor.html
    """
    Return list of cursor type names from java.awt.Cursor API.
    """
    types = ['DEFAULT_CURSOR', 'CROSSHAIR_CURSOR', 'E_RESIZE_CURSOR', 'HAND_CURSOR', 'MOVE_CURSOR', 'N_RESIZE_CURSOR', 'NE_RESIZE_CURSOR', 'NW_RESIZE_CURSOR', 'S_RESIZE_CURSOR', 'SE_RESIZE_CURSOR', 'SW_RESIZE_CURSOR', 'TEXT_CURSOR', 'W_RESIZE_CURSOR', 'WAIT_CURSOR', 'CUSTOM_CURSOR']
    return types

