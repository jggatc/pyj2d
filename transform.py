#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from java.awt.image import BufferedImage, AffineTransformOp
from java.awt import RenderingHints
from java.awt.geom import AffineTransform
from java.lang import IllegalArgumentException
import math
from surface import Surface

__docformat__ = 'restructuredtext'


class Transform(object):
    """
    **pyj2d.transform**
    
    * pyj2d.transform.rotate
    * pyj2d.transform.rotozoom
    * pyj2d.transform.scale
    * pyj2d.transform.smoothscale
    * pyj2d.transform.scale2x
    * pyj2d.transform.flip
    """

    def __init__(self):
        """
        Provides image transformation methods.

        Module initialization creates pyj2d.transform instance.
        """
        self.deg_rad = math.pi/180

    def rotate(self, surface, angle):
        """
        Return Surface rotated by the given angle.
        """
        theta = angle*self.deg_rad
        width_i = surface.getWidth()
        height_i = surface.getHeight()
        cos_theta = math.fabs( math.cos(theta) )
        sin_theta = math.fabs( math.sin(theta) )
        width_f = int( (width_i*cos_theta)+(height_i*sin_theta) )
        height_f = int( (width_i*sin_theta)+(height_i*cos_theta) )
        surf = Surface((width_f,height_f), BufferedImage.TYPE_INT_ARGB)
        at = AffineTransform()
        at.rotate(-theta, width_f/2, height_f/2)
        g2d = surf.createGraphics()
        ot = g2d.getTransform()
        g2d.setTransform(at)
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR)
        g2d.drawImage(surface, (width_f-width_i)//2, (height_f-height_i)//2, None)
        g2d.setTransform(ot)
        g2d.dispose()
        return surf

    def rotozoom(self, surface, angle, size):
        """
        Return Surface rotated and resized by the given angle and size.
        """
        surf = self.rotate(surface, angle)
        if size != 1.0:
            try:
                surf = self.scale(surf, (int(surface.getWidth()*size), int(surface.getHeight()*size)))
            except IllegalArgumentException:    #dim < 1
                surf = self.scale(surf, (int(math.ceil(surface.getWidth()*size)), int(math.ceil(surface.getHeight()*size))))
        return surf

    def scale(self, surface, size, dest=None):
        """
        Return Surface resized by the given size.
        An optional destination surface can be provided.
        """
        if not dest:
            surf = Surface(size, BufferedImage.TYPE_INT_ARGB)
        else:
            surf = dest
        g2d = surf.createGraphics()
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR)
        g2d.drawImage(surface, 0, 0, size[0], size[1], None)
        g2d.dispose()
        return surf

    def smoothscale(self, surface, size):
        """
        Calls scale().
        Return Surface resized by the given size.
        """
        return self.scale(surface, size)

    def scale2x(self, surface, dest=None):
        """
        Return Surface resized to twice its size.
        An optional destination surface can be provided.
        """
        return self.scale(surface, (surface.getWidth()*2,surface.getHeight()*2), dest)

    def flip(self, surface, xbool=True, ybool=False):
        """
        Return Surface that is flipped horizontally, vertically, or both.
        """
        if xbool and ybool:
            at = AffineTransform.getScaleInstance(-1, -1)
            at.translate(-surface.getHeight(), -surface.getHeight())
        elif xbool:
            at = AffineTransform.getScaleInstance(-1, 1)
            at.translate(-surface.getWidth(), 0)
        elif ybool:
            at = AffineTransform.getScaleInstance(1, -1)
            at.translate(0, -surface.getHeight())
        else:
            return surface
        op = AffineTransformOp(at, AffineTransformOp.TYPE_BILINEAR)
        bimage = op.filter(surface, None)
        surf = Surface(bimage)
        return surf

