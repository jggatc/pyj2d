#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from java.util import BitSet

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
        i = 0
        for y in range(surface.height):
            for x in range(surface.width):
                if ((pixels[i]>>16) & 0xff) == color[0] and ((pixels[i]>>8) & 0xff) == color[1] and ((pixels[i]) & 0xff) == color[2] and ((pixels[i]>>24) & 0xff) >= threshold[3]:
                    mask.set_at((x,y))
                i += 1
    else:
        col = []
        for i in range(len(color)):
            if threshold[i]:
                l = color[i] - threshold[i]
                if l < 0: l = 0
                h = color[i] + threshold[i]
                if h > 255: h = 255
                col.append( (l,h) )
            else:
                col[i].append( (color[i],color[i]) )
        i = 0
        for y in range(surface.height):
            for x in range(surface.width):
                if ( ((pixels[i]>>16) & 0xff) >= col[0][0] and ((pixels[i]>>16) & 0xff) <= col[0][1] ) and ( ((pixels[i]>>8) & 0xff) >= col[1][0] and ((pixels[i]>>8) & 0xff) <= col[1][1] ) and ( ((pixels[i]) & 0xff) >= col[2][0] and ((pixels[i]) & 0xff) <= col[2][1] ) and ( ((pixels[i]>>24) & 0xff) >= threshold[3] ):
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
    * Mask.print_mask
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

    def print_mask(self):
        """
        Print mask.
        """
        print
        for bitset in self.bit:
            for bit in range(self.width):
                print bitset.get(bit),
            print
        print

