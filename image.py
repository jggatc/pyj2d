#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from javax.imageio import ImageIO
from java.io import File, ByteArrayInputStream
from pyj2d.surface import Surface
from pyj2d import env

__docformat__ = 'restructuredtext'


class Image(object):
    """
    **pyj2d.image**
    
    * pyj2d.image.load
    """

    def __init__(self):
        """
        Initialize Image module.
        
        Module initialization creates pyj2d.image instance.
        """
        pass

    def load(self, img_file, namehint=None):
        """
        Load image from file as a java.awt.image.BufferedImage.
        The img_file can be a filename or file-like object.
        Return the bufferedimage as a Surface.
        """
        if isinstance(img_file, str):
            try:
                f = env.japplet.getClass().getResource(img_file.replace('\\','/'))
                if not f:
                    raise
            except:
                f = File(img_file)
            bimage = ImageIO.read(f)
        else:
            bimage = ImageIO.read(ByteArrayInputStream(img_file.getvalue()))
            img_file.close()
        surf = Surface(bimage)
        return surf

