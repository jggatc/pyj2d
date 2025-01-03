#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from java.awt.image import BufferedImage
from pyj2d.surface import Surface

__docformat__ = 'restructuredtext'

__doc__ = 'Surface pixel manipulation'


_initialized = False


def _init():
    """
    Initialize surfarray module.
    """
    global numeric, _initialized
    from pyj2d.numeric import numeric
    if not numeric:
        raise ImportError("JNumeric module is required.")
    _initialized = True


def array2d(surface):
    """
    Return data array of the Surface argument.
    Array consists of pixel data arranged by [x,y] in integer color format.
    JNumeric required as specified in numeric module.
    """
    if not _initialized:
        _init()
    data = numeric.zeros((surface.width * surface.height), 'i')
    data = surface.getRGB(0, 0, surface.width, surface.height,
                          data, 0, surface.width)
    array = numeric.reshape(data, (surface.width, surface.height))
    return array


def array3d(surface):
    """
    Return data array of the Surface argument.
    Array consists of pixel data arranged by [x,y] in RGB format.
    JNumeric required as specified in numeric module.
    """
    if not _initialized:
        _init()
    data = surface.getRGB(0, 0, surface.width, surface.height,
                          None, 0, surface.width)
    data = numeric.array([(dat>>16 & 0xff, dat>>8 & 0xff, dat & 0xff)
                          for dat in data])
    array = numeric.reshape(data, (surface.width, surface.height,3))
    return array


def array_alpha(surface):
    """
    Return data array of the Surface argument.
    Array consists of pixel data arranged by [x,y] of pixel alpha value.
    JNumeric required as specified in numeric module.
    """
    if not _initialized:
        _init()
    data = surface.getRGB(0, 0, surface.width, surface.height,
                          None, 0, surface.width)
    data = numeric.array([dat>>24 & 0xff for dat in data], numeric.Int8)
    array = numeric.reshape(data, (surface.width, surface.height))
    return array


def make_surface(array):
    """
    Generates image pixels from array data.
    Argument array containing image data.
    Return Surface generated from array.
    JNumeric required as specified in numeric module.
    """
    if not _initialized:
        _init()
    surface = Surface((array.shape[0],array.shape[1]))
    blit_array(surface, array)
    return surface


def blit_array(surface, array):
    """
    Generates image pixels from a JNumeric array.
    Arguments include destination Surface and array of integer colors.
    JNumeric required as specified in numeric module.
    """
    if not _initialized:
        _init()
    if len(array.shape) == 2:
        data = numeric.transpose(array, (1,0))
        data = numeric.ravel(data)
    else:
        data = array[:,:,0]*0x10000 | array[:,:,1]*0x100 | array[:,:,2]
        data = numeric.transpose(data, (1,0))
        data = numeric.ravel(data)
    if not surface.getColorModel().hasAlpha():
        surface.setRGB(0, 0, surface.width, surface.height,
                       data, 0, surface.width)
    else:
        surf = Surface((surface.width, surface.height),
                       BufferedImage.TYPE_INT_RGB)
        surf.setRGB(0, 0, surface.width, surface.height,
                    data, 0, surface.width)
        g2d = surface.createGraphics()
        g2d.drawImage(surf, 0, 0, None)
        g2d.dispose()
    return None

