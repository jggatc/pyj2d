#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from java.util import BitSet
from pyj2d.color import Color

__docformat__ = 'restructuredtext'


def from_surface(surface, threshold=127):
    """
    **pyj2d.mask.from_surface**
    
    Return Mask derived from surface using alpha transparency.
    Optional argument to set alpha threshold.
    """
    mask = Mask((surface.width, surface.height))
    pixels = surface.getRGB(0,0,surface.width,surface.height,None,0,surface.width)
    i = 0
    for y in range(surface.height):
        for x in range(surface.width):
            if ( (pixels[i]>>24) & 0xff ) > threshold:
                mask.set_at((x,y))
            i += 1
    return mask


def from_threshold(surface, color, threshold=(0,0,0,255)):
    """
    **pyj2d.mask.from_threshold**
    
    Return Mask from surface using a given color.
    Optional threshold argument to set color range and alpha threshold.
    """
    mask = Mask((surface.width, surface.height))
    pixels = surface.getRGB(0,0,surface.width,surface.height,None,0,surface.width)
    if threshold == (0,0,0,255):
        color = Color(color)
        if color.a != 255:
            color = Color(color.r,color.g,color.b,255)
        icolor = color.getRGB()
        i = 0
        for y in range(surface.height):
            for x in range(surface.width):
                if pixels[i] == icolor:
                    mask.set_at((x,y))
                i += 1
    else:
        color = Color(color)
        col = {}
        for i, c in enumerate(('r','g','b')):
            if threshold[i]:
                col[c+'1'] = color[i] - threshold[i] - 1
                col[c+'2'] = color[i] + threshold[i] + 1
            else:
                col[c+'1'] = color[i] - 1
                col[c+'2'] = color[i] + 1
        col['a'] = threshold[3] - 1
        i = 0
        for y in range(surface.height):
            for x in range(surface.width):
                if ( col['r1'] < ((pixels[i]>>16) & 0xff) < col['r2'] ) and ( col['g1'] < ((pixels[i]>>8) & 0xff) < col['g2'] ) and ( col['b1'] < ((pixels[i]) & 0xff) < col['b2'] ) and ( ((pixels[i]>>24) & 0xff) > col['a'] ):
                    mask.set_at((x,y))
                i += 1
    return mask


class Mask(object):
    """
    **pyj2d.mask.Mask**
    
    * Mask.get_size
    * Mask.get_at
    * Mask.set_at
    * Mask.fill
    * Mask.clear
    * Mask.invert
    * Mask.count
    * Mask.overlap
    * Mask.toString
    """

    def __init__(self, (width, height)):
        """
        Return a Mask of an image.
        The arguments include width and height of the image.
        The mask uses java.util.BitSet, and stored in the bit attribute as a list of bitset for each pixel row in the image.
        """
        self.width = int(width)
        self.height = int(height)
        self.bit = []
        for bitset in range(self.height):
            self.bit.append(BitSet(self.width))

    def __repr__(self):
        """
        Return string representation of Mask object.
        """
        return "%s(%r)" % (self.__class__, self.__dict__)

    def get_size(self):
        """
        Return width, height of mask.
        """
        return (self.width, self.height)

    def get_at(self, pos):
        """
        Return bit setting for given pos.
        """
        return self.bit[pos[1]].get(pos[0])

    def set_at(self, pos, value=1):
        """
        Set bit for given pos.
        Optional value to set bit, eith 1 or 0, defaults to 1.
        """
        if value:
            self.bit[pos[1]].set(pos[0])
        else:
            self.bit[pos[1]].clear(pos[0])
        return None

    def fill(self):
        """
        Fill mask.
        """
        for bitset in self.bit:
            bitset.set(0,self.width)
        return None

    def clear(self):
        """
        Clear mask.
        """
        for bitset in self.bit:
            bitset.clear()
        return None

    def invert(self):
        """
        Invert bit value in mask.
        """
        for bitset in self.bit:
            bitset.flip(0,self.width)
        return None

    def count(self):
        """
        Return count of true bits in mask.
        """
        true_bits = 0
        for bitset in self.bit:
            true_bits += bitset.cardinality()
        return true_bits

    def overlap(self, mask, offset):
        """
        Return True if mask at offset position overlap with this mask.
        """
        if offset[0] > 0:
            x1 = offset[0]
            x2 = 0
        else:
            x1 = 0
            x2 = -offset[0]
        if offset[1] > 0:
            y1 = offset[1]
            y2 = 0
        else:
            y1 = 0
            y2 = -offset[1]
        w = min(self.width-x1, mask.width-x2)
        h = min(self.height-y1, mask.height-y2)
        if w > 0 and h > 0:
            for y in range(h):
                if self.bit[y1+y].get(x1, x1+w).intersects(mask.bit[y2+y].get(x2, x2+w)):
                    return True
        return None

    def toString(self, bit=('1','0')):
        """
        Return string representation of mask.
        Optional bit argument specify bit character.
        """
        cbit = {True:bit[0], False:bit[1]}
        cbitset = []
        for bitset in self.bit:
            cbitset.append('\n')
            cbitset.extend([cbit[bitset.get(i)] for i in range(self.width)])
        bitstr = ''.join(cbitset)
        return bitstr

