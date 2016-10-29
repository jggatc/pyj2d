#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from java.awt.image import BufferedImage
from pyj2d.surface import Surface

__docformat__ = 'restructuredtext'


class Surfarray(object):
    """
    **pyj2d.surfarray**
    
    * pyj2d.surfarray.blit_array
    """

    def __init__(self):
        """
        Provides image pixel manipulation method.

        Module initialization creates pyj2d.surfarray instance.
        JNumeric module is required as specified in numeric.py.
        """
        self.initialized = False
        self._nonimplemented_methods()

    def _init(self):
        """
        Initialize surfarray module.
        """
        global numeric
        from numeric import numeric
        if not numeric:
            raise ImportError("JNumeric module is required.")
        self.initialized = True

    def array2d(self, surface):
        """
        Return data array of the Surface argument.
        Array consists of pixel data arranged by [x,y] in integer color format.
        """
        if not self.initialized:
            self._init()
        data = numeric.zeros((surface.width*surface.height), 'i')
        data = surface.getRGB(0, 0, surface.width, surface.height, data, 0, surface.width)
        array = numeric.reshape(data, (surface.width,surface.height))
        return array

    def array3d(self, surface):
        """
        Return data array of the Surface argument.
        Array consists of pixel data arranged by [x,y] in RGB format.
        """
        if not self.initialized:
            self._init()
        data = surface.getRGB(0, 0, surface.width, surface.height, None, 0, surface.width)
        data = numeric.array([(dat>>16 & 0xff, dat>>8 & 0xff, dat & 0xff) for dat in data])
        array = numeric.reshape(data, (surface.width,surface.height,3))
        return array

    def array_alpha(self, surface):
        """
        Return data array of the Surface argument.
        Array consists of pixel data arranged by [x,y] of pixel alpha value.
        """
        if not self.initialized:
            self._init()
        data = surface.getRGB(0, 0, surface.width, surface.height, None, 0, surface.width)
        data = numeric.array([dat>>24 & 0xff for dat in data], numeric.Int8)
        array = numeric.reshape(data, (surface.width,surface.height))
        return array

    def make_surface(self, array):
        """
        Generates image pixels from array data.
        Argument array containing image data.
        Return Surface generated from array.
        """
        if not self.initialized:
            self._init()
        surface = Surface((array.shape[0],array.shape[1]))
        self.blit_array(surface, array)
        return surface

    def blit_array(self, surface, array):
        """
        Generates image pixels from a JNumeric array.
        Arguments include surface to generate the image, and array of integer colors.
        """
        if not self.initialized:
            self._init()
        if len(array.shape) == 2:
            data = numeric.transpose(array, (1,0))
            data = numeric.ravel(data)
        else:
            data = array[:,:,0]*0x10000 | array[:,:,1]*0x100 | array[:,:,2]
            data = numeric.transpose(data, (1,0))
            data = numeric.ravel(data)
        if not surface.getColorModel().hasAlpha():
            surface.setRGB(0, 0, surface.width, surface.height, data, 0, surface.width)
        else:
            surf = Surface((surface.width,surface.height), BufferedImage.TYPE_INT_RGB)
            surf.setRGB(0, 0, surface.width, surface.height, data, 0, surface.width)
            g2d = surface.createGraphics()
            g2d.drawImage(surf, 0, 0, None)
            g2d.dispose()
        return None

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.use_arraytype = lambda *arg: None

