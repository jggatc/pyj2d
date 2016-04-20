#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from java.awt.image import BufferedImage, RasterFormatException
from java.util import Hashtable
from java.lang import Thread
from rect import Rect
from color import Color
import locals as Const

__docformat__ = 'restructuredtext'


class Surface(BufferedImage):
    """
    **pyj2d.Surface**
    
    * Surface.get_size
    * Surface.get_width
    * Surface.get_height
    * Surface.get_rect
    * Surface.copy
    * Surface.subsurface
    * Surface.subarea
    * Surface.blit
    * Surface.blits
    * Surface.set_colorkey
    * Surface.get_colorkey
    * Surface.replace_color
    * Surface.get_at
    * Surface.set_at
    * Surface.fill
    * Surface.get_parent
    * Surface.get_offset
    """

    def __init__(self, *arg):
        """
        Return Surface that is subclassed from java.awt.image.BufferedImage.
        
        Alternative arguments:
        
        * Size (w,h) of surface, optional second argument of flags (SRCALPHA)
        * Bufferedimage to convert to Surface
        
        Module initialization places pyj2d.Surface in module's namespace.
        """
        try:
            width, height = arg[0]
            try:
                if arg[1] & (BufferedImage.TYPE_INT_ARGB | Const.SRCALPHA):
                    BufferedImage.__init__(self, width, height, BufferedImage.TYPE_INT_ARGB)
                else:
                    BufferedImage.__init__(self, width, height, BufferedImage.TYPE_INT_RGB)
            except IndexError:
                BufferedImage.__init__(self, width, height, BufferedImage.TYPE_INT_ARGB)
                graphics2D = BufferedImage.createGraphics(self)
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
                        properties.put(key,arg[0].getProperty(key))
            except AttributeError:
                cm, raster, isRasterPremultiplied, properties = arg
            BufferedImage.__init__(self, cm, raster, isRasterPremultiplied, properties)
        self._display = None    #display surface
        self._super_surface = None
        self._offset = (0,0)
        self._colorkey = None
        self._nonimplemented_methods()

    def __repr__(self):
        """
        Return string representation of Surface object.
        """
        return "%s(%s, %r)" % (self.__class__, self.toString(), self.__dict__)

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
            rect.__setattr__(key,attr[key])
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
                    img_properties.put(key,self.getProperty(key))
            surface = Surface(
                              self.getColorModel(),
                              self.getData(),
                              self.isAlphaPremultiplied(),
                              img_properties
                             )
            surface._colorkey = self._colorkey
        else:
            surface = Surface((self.width,self.height), BufferedImage.TYPE_INT_ARGB)
            g2d = surface.createGraphics()
            g2d.drawImage(self, 0, 0, None)
            g2d.dispose()
            surface._colorkey = self._colorkey
        return surface

    def subsurface(self, rect):
        """
        Return Surface that represents a subsurface that shares data with this surface.
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
            except:     #rect outside surface
                return None
        surface = Surface(subsurf)
        surface._super_surface = self
        surface._offset = (rect.x,rect.y)
        surface._colorkey = self._colorkey
        return surface

    def subarea(self, rect):
        """
        Return Surface and Rect that represents a subsurface that shares data with this surface.
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
                clip = self.get_rect().intersection(rect)
                rect = Rect(clip.x, clip.y, clip.width, clip.height)
                subsurf = self.getSubimage(rect.x, rect.y, rect.width, rect.height)
            except:     #rect outside surface
                rect = Rect(0,0,0,0)
                subsurf = None
        return subsurf, rect

    def blit(self, surface, position, area=None):
        """
        Draw given surface on this surface at position.
        Optional area delimitates the region of given surface to draw.
        """
        if not area:
            rect = self.get_rect().intersection( Rect(position[0], position[1], surface.width, surface.height) )
            surface_rect = Rect(rect.x, rect.y, rect.width, rect.height)
        else:
            surface, rect = surface.subarea(area)
            rect.x, rect.y = int(position[0]), int(position[1])
            rect = self.get_rect().intersection(rect)
            surface_rect = Rect(rect.x, rect.y, rect.width, rect.height)
        if surface_rect.width < 1 or surface_rect.height < 1:
            surface_rect.width = surface_rect.height = 0
        g2d = self.createGraphics()
        try:
            g2d.drawImage(surface, position[0], position[1], None)
        except TypeError:
            g2d.drawImage(surface, int(position[0]), int(position[1]), None)
        g2d.dispose()
        return surface_rect

    def blits(self, surfaces):
        """
        Draw list of (surface, rect) on this surface.
        """
        g2d = self.createGraphics()
        for surface, rect in surfaces:
            g2d.drawImage(surface, rect.x, rect.y, None)
        g2d.dispose()
        return None

    def set_colorkey(self, color, flags=None):
        """
        Set surface colorkey.
        """
        if self._colorkey:
            r,g,b = self._colorkey.r,self._colorkey.g,self._colorkey.b
            self.replace_color((r,g,b,0),(r,g,b,255))
            self._colorkey = None
        if color:
            color = Color(color)
            self._colorkey = color
            self.replace_color((color.r,color.g,color.b))
        return None

    def get_colorkey(self):
        """
        Return surface colorkey.
        """
        try:
            return self._colorkey.r, self._colorkey.g, self._colorkey.b, 255
        except AttributeError:
            return None

    def replace_color(self, color, new_color=None):
        """
        Replace color with with new_color or with alpha.
        """
        pixels = self.getRGB(0,0,self.width,self.height,None,0,self.width)
        color1 = Color(color)
        if new_color:
            color2 = Color(new_color)
        else:
            color2 = Color(color1.r,color1.g,color1.b,0)
        for i, pixel in enumerate(pixels):
            if pixel == color1.getRGB():
                pixels[i] = color2.getRGB()
        self.setRGB(0,0,self.width,self.height,pixels,0,self.width)
        return None

    def get_at(self, pos):
        """
        Return color of a surface pixel.
        The pos argument represents x,y position of pixel.
        """
        x,y = pos       #*tuple unpack error in jython applet
        try:
            color = Color(self.getRGB(x,y))
        except:     #ArrayOutOfBoundsException
            raise IndexError
        return color

    def set_at(self, pos, color):
        """
        Set color of a surface pixel.
        The arguments represent position x,y and color of pixel.
        """
        color = Color(color)
        try:
            self.setRGB(pos[0],pos[1],color.getRGB())
        except:     #ArrayOutOfBoundsException
            raise IndexError
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
        """
        Non-implemented methods.
        """
        self.convert = lambda *arg: self
        self.convert_alpha = lambda *arg: self
        self.set_alpha = lambda *arg: None
        self.get_alpha = lambda *arg: None
        self.lock = lambda *arg: None
        self.unlock = lambda *arg: None
        self.mustlock = lambda *arg: False
        self.get_locked = lambda *arg: False
        self.get_locks = lambda *arg: ()

