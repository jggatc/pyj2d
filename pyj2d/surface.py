#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Surface module**

The module provides surface object.
"""

from java.awt.image import BufferedImage, RasterFormatException
from java.awt import AlphaComposite
from java.lang import ArrayIndexOutOfBoundsException
from java.util import Hashtable
from pyj2d.rect import Rect
from pyj2d.color import Color
from pyj2d import constants as Const


_return_rect = True


class Surface(BufferedImage):
    """
    Surface object.
    """

    _alpha_composite = {
        1.0: AlphaComposite.getInstance(
                AlphaComposite.SRC_OVER, 1.0)}

    def __init__(self, *arg):
        """
        Initialize Surface object.

        Surface object is subclassed from java.awt.image.BufferedImage.
        
        Alternative arguments:
        
        * Size (width, height) of surface, optional argument of flags (SRCALPHA)
        * Bufferedimage to convert to Surface
        
        Module initialization places Surface in module's namespace.
        """
        try:
            width, height = arg[0]
            try:
                if arg[1] & (BufferedImage.TYPE_INT_ARGB | Const.SRCALPHA):
                    BufferedImage.__init__(self, width, height,
                                           BufferedImage.TYPE_INT_ARGB)
                else:
                    BufferedImage.__init__(self, width, height,
                                           BufferedImage.TYPE_INT_RGB)
            except IndexError:
                BufferedImage.__init__(self, width, height,
                                       BufferedImage.TYPE_INT_ARGB)
                graphics2D = self.createGraphics()
                graphics2D.setColor(Color(0,0,0))
                graphics2D.fillRect(0, 0, width, height)
                graphics2D.dispose()
        except TypeError:
            try:
                cm = arg[0].getColorModel()
                raster = arg[0].getRaster()
                isRasterPremultiplied = arg[0].isAlphaPremultiplied()
                properties = Hashtable()
                keys = arg[0].getPropertyNames()
                if keys != None:
                    for key in keys:
                        properties.put(key, arg[0].getProperty(key))
            except AttributeError:
                cm, raster, isRasterPremultiplied, properties = arg
            BufferedImage.__init__(self, cm, raster,
                                   isRasterPremultiplied, properties)
        self._super_surface = None
        self._offset = (0,0)
        self._colorkey = None
        self._alpha = 1.0
        self._nonimplemented_methods()

    def __str__(self):
        s = '<%s(%dx%d)>'
        return s % (self.__class__.__name__, self.width, self.height)

    def __repr__(self):
        return self.__str__()

    def get_size(self):
        """
        Return width and height of surface.
        """
        return (self.width, self.height)

    def get_width(self):
        """
        Return width of surface.
        """
        return self.width

    def get_height(self):
        """
        Return height of surface.
        """
        return self.height

    def get_rect(self, **attr):
        """
        Return rect of the surface.

        An optional keyword argument of the rect position.
        """
        rect = Rect(0, 0, self.width, self.height)
        for key in attr:
            getattr(rect, '_set_'+key)(attr[key])
        return rect

    def copy(self):
        """
        Return Surface that is a copy of this surface.
        """
        if not self._super_surface:
            img_properties = Hashtable()
            keys = self.getPropertyNames()
            if keys != None:
                for key in keys:
                    img_properties.put(key, self.getProperty(key))
            surface = Surface(
                              self.getColorModel(),
                              self.getData(),
                              self.isAlphaPremultiplied(),
                              img_properties
                             )
        else:
            surface = Surface((self.width, self.height),
                              BufferedImage.TYPE_INT_ARGB)
            g2d = surface.createGraphics()
            g2d.drawImage(self, 0, 0, None)
            g2d.dispose()
        surface._colorkey = self._colorkey
        surface._alpha = self._alpha
        return surface

    def subsurface(self, rect):
        """
        Return subsurface.

        Subsurface shares data with this surface.
        The rect argument is the area of the subsurface.
        """
        try:
            try:
                subsurf = self.getSubimage(rect.x, rect.y, rect.width, rect.height)
            except AttributeError:
                rect = Rect(rect)
                subsurf = self.getSubimage(rect.x, rect.y, rect.width, rect.height)
        except RasterFormatException:
            try:
                rect = self.get_rect().intersection(rect)
                subsurf = self.getSubimage(rect.x, rect.y, rect.width, rect.height)
            except:
                raise ValueError('subsurface outside surface area')
        surface = Surface(subsurf)
        surface._super_surface = self
        surface._offset = (rect.x,rect.y)
        surface._colorkey = self._colorkey
        surface._alpha = self._alpha
        return surface

    def blit(self, surface, position, area=None):
        """
        Draw given surface on this surface at position.

        Optional area delimitates the region of given surface to draw.
        """
        g2d = self.createGraphics()
        g2d.setComposite(self._alpha_composite[surface._alpha])
        if not area:
            g2d.drawImage(surface,
                          position[0], position[1], None)
            g2d.dispose()
            if _return_rect:
                rect = Rect(position[0], position[1],
                            surface.width, surface.height)
            else:
                return None
        else:
            g2d.drawImage(surface,
                    position[0], position[1],
                    position[0]+area[2], position[1]+area[3],
                    area[0], area[1],
                    area[0]+area[2], area[1]+area[3], None)
            g2d.dispose()
            if _return_rect:
                rect = Rect(position[0], position[1],
                            area[2], area[3])
            else:
                return None
        return self.get_rect().clip(rect)

    def blits(self, blit_sequence, doreturn=True):
        """
        Draw a sequence of surfaces on this surface.

        Argument blit_sequence of (source, dest) or (source, dest, area).
        Optional doreturn (defaults to True) to return list of rects.
        """
        g2d = self.createGraphics()
        if doreturn:
            rects = []
        else:
            rects = None
        for blit in blit_sequence:
            surface = blit[0]
            position = blit[1]
            if len(blit) > 2:
                area = blit[2]
            else:
                area = None
            g2d.setComposite(self._alpha_composite[surface._alpha])
            if not area:
                g2d.drawImage(surface, position[0], position[1], None)
                if doreturn:
                    rect = Rect(position[0], position[1],
                                surface.width, surface.height)
                    rects.append(self.get_rect().clip(rect))
            else:
                g2d.drawImage(surface,
                        position[0], position[1],
                        position[0]+area[2], position[1]+area[3],
                        area[0], area[1],
                        area[0]+area[2], area[1]+area[3], None)
                if doreturn:
                    rect = Rect(position[0], position[1],
                                area[2], area[3])
                    rects.append(self.get_rect().clip(rect))
        g2d.dispose()
        return rects

    def _blits(self, surfaces):
        g2d = self.createGraphics()
        for surface, rect in surfaces:
            g2d.setComposite(self._alpha_composite[surface._alpha])
            g2d.drawImage(surface, rect.x, rect.y, None)
        g2d.dispose()

    def _blit_clear(self, surface, rect_list):
        g2d = self.createGraphics()
        g2d.setComposite(self._alpha_composite[surface._alpha])
        for r in rect_list:
            g2d.drawImage(surface,
                          r.x, r.y, r.x+r.width, r.y+r.height,
                          r.x, r.y, r.x+r.width, r.y+r.height, None)
        g2d.dispose()

    def set_alpha(self, alpha):
        """
        Set surface alpha.

        Surface alpha can have values of 0 to 255, disabled by passing None.
        """
        if alpha is not None:
            alpha = alpha/255.0
            if alpha < 0.0:
                alpha = 0.0
            elif alpha > 1.0:
                alpha = 1.0
            self._alpha = alpha
            if self._alpha not in self._alpha_composite:
                composite = AlphaComposite.getInstance(
                    AlphaComposite.SRC_OVER, self._alpha)
                self._alpha_composite[self._alpha] = composite
        else:
            self._alpha = 1.0

    def get_alpha(self):
        """
        Get surface alpha value.
        """
        return int(self._alpha*255)

    def set_colorkey(self, color, flags=None):
        """
        Set surface colorkey.
        """
        if self._colorkey:
            r = self._colorkey.r
            g = self._colorkey.g
            b = self._colorkey.b
            self.replace_color((r,g,b,0), self._colorkey)
            self._colorkey = None
        if color:
            self._colorkey = Color(color)
            self.replace_color(self._colorkey)
        return None

    def get_colorkey(self):
        """
        Return surface colorkey.
        """
        if self._colorkey:
            return ( self._colorkey.r,
                     self._colorkey.g,
                     self._colorkey.b,
                     self._colorkey.a )
        else:
            return None

    def replace_color(self, color, new_color=None):
        """
        Replace color with with new_color or with alpha.
        """
        pixels = self.getRGB(0, 0, self.width, self.height,
                             None,0,self.width)
        if hasattr(color, 'a'):
            color1 = color
        else:
            color1 = Color(color)
        if new_color is None:
            color2 = Color(color1.r, color1.g, color1.b, 0)
        else:
            if hasattr(new_color, 'a'):
                color2 = new_color
            else:
                color2 = Color(new_color)
        for i, pixel in enumerate(pixels):
            if pixel == color1.getRGB():
                pixels[i] = color2.getRGB()
        self.setRGB(0, 0, self.width, self.height,
                    pixels, 0, self.width)
        return None

    def get_at(self, pos):
        """
        Get color of a surface pixel.

        The pos argument represents x,y position of pixel.
        """
        try:
            return Color(self.getRGB(pos[0], pos[1]))
        except ArrayIndexOutOfBoundsException:
            raise IndexError('pixel index out of range')

    def set_at(self, pos, color):
        """
        Set color of a surface pixel.

        The arguments represent position x,y and color of pixel.
        """
        color = Color(color)
        try:
            self.setRGB(pos[0], pos[1], color.getRGB())
        except ArrayIndexOutOfBoundsException:
            raise IndexError('pixel index out of range')
        return None

    def fill(self, color=(0,0,0), rect=None):
        """
        Fill surface with color.
        """
        g2d = self.createGraphics()
        color = Color(color)
        g2d.setColor(color)
        if not rect:
            rect = Rect(0, 0, self.width, self.height)
        else:
            rect = Rect(rect)
        g2d.fillRect(rect.x, rect.y, rect.width, rect.height)
        g2d.dispose()
        return rect

    def get_parent(self):
        """
        Return parent Surface of subsurface.
        """
        return self._super_surface   #if delete, delete subsurface...

    def get_offset(self):
        """
        Return offset of subsurface in surface.
        """
        return self._offset

    def _nonimplemented_methods(self):
        self.convert = lambda *arg: self
        self.convert_alpha = lambda *arg: self
        self.lock = lambda *arg: None
        self.unlock = lambda *arg: None
        self.mustlock = lambda *arg: False
        self.get_locked = lambda *arg: False
        self.get_locks = lambda *arg: ()


def bounding_rect_return(setting):
    """
    Bounding rect return.

    Set whether surface blit function returns bounding Rect.
    Setting (bool) defaults to True on module initialization.
    """
    global _return_rect
    _return_rect = setting

