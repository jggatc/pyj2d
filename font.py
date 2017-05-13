#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
import os
from java.awt import Font as JFont
from java.awt import BasicStroke, RenderingHints, GraphicsEnvironment
from java.awt.font import TextAttribute
from java.text import AttributedString
from java.lang import IllegalArgumentException
from java.awt.image import BufferedImage
from java.io import File
from pyj2d.surface import Surface
from pyj2d.color import Color
from pyj2d import env

__docformat__ = 'restructuredtext'


_initialized = False
_surf = None
_g2d = None


def init():
    """
    **pyj2d.font.init**
    
    Initialize font module.
    """
    global _surf, _g2d, _initialized, match_font
    _surf = Surface((1,1), BufferedImage.TYPE_INT_RGB)
    _g2d = _surf.createGraphics()
    _initialized = True
init()


def quit():
    """
    **pyj2d.font.quit**
    
    Unintialize font module.
    """
    global _surf, _g2d, _initialized
    _g2d.dispose()
    _g2d = None
    _surf = None
    _initialized = False


def get_init():
    """
    **pyj2d.font.get_init**
    
    Check if font module is intialized.
    """
    return _initialized


def get_default_font():
    """
    **pyj2d.font.get_default_font**
    
    Return default font.
    """
    fonts = get_fonts()
    for fontfamily in Font._font_family:
        for font in fontfamily:
            if font in fonts:
                return font
    return fonts[0]


def get_fonts():
    """
    **pyj2d.font.get_fonts**
    
    Return fonts available in JVM.
    """
    return [''.join([c for c in f if c.isalnum()]).lower() for f in GraphicsEnvironment.getLocalGraphicsEnvironment().getAvailableFontFamilyNames()]


def match_font(name, *args, **kwargs):
    """
    **pyj2d.font.match_font**
    
    Argument name is a font name, or comma-delimited string of font names.
    Return font found on system, otherwise return None if none found.
    """
    font = [''.join([c for c in f if c.isalnum()]).lower() for f in name.split(',')]
    fonts = get_fonts()
    for fn in font:
        if fn in fonts:
            return fn
    return None


class Font(JFont):
    """
    **pyj2d.font.Font**
    
    * Font.render
    * Font.size
    * Font.set_underline
    * Font.get_underline
    * Font.set_bold
    * Font.get_bold
    * Font.set_italic
    * Font.get_italic
    * Font.get_height
    * Font.get_linesize
    * Font.get_ascent
    * Font.get_descent
    """

    _font = None

    _font_default = None

    _font_family = [['arial', 'helvetica', 'liberationsans',  'nimbussansl', 'freesans', 'tahoma', 'sansserif'], ['verdana', 'bitstreamverasans', 'dejavusans', 'sansserif'], ['impact', 'sansserif'], ['comicsansms', 'cursive', 'sansserif'], ['couriernew', 'courier', 'lucidaconsole', 'dejavusansmono', 'monospace'], ['timesnewroman', 'times', 'liberationserif', 'nimbusromanno9l', 'serif'], ['garamond',  'bookantiqua', 'palatino', 'liberationserif', 'nimbusromanno9l', 'serif'], ['georgia', 'bitstreamveraserif', 'lucidaserif', 'liberationserif', 'dejavuserif', 'serif']]

    def __init__(self, name, size):
        """
        Return Font subclassed of java.awt.Font.
        Arguments include name of a system font and size of font. The name argument can be a string of comma-delimited names to specify fallbacks and use a default font if none found, or specify a font file (eg. 'resource/font.ttf') with a exception if file not found.
        """
        if not Font._font:
            Font._font = get_fonts()
            Font._font_default = get_default_font()
        self.fontname, isFile = self._getFontName(name)
        self.fontsize = size
        if not hasattr(self, 'fontstyle'):
            self.fontstyle = JFont.PLAIN
        if not isFile:
            JFont.__init__(self, self.fontname, self.fontstyle, self.fontsize)
        else:
            font = self._getFont(self.fontname, self.fontstyle, self.fontsize)
            JFont.__init__(self, font)
        self.font = self
        _g2d.setFont(self.font)
        self.fontMetrics = _g2d.getFontMetrics()
        self.underline = False
        self._nonimplemented_methods()

    def __repr__(self):
        """
        Return string representation of Font object.
        """
        return "%s(%r)" % (self.__class__, self.__dict__)

    def _getFontName(self, name):
        isFile = False
        if not name:
            return Font._font_default, isFile
        if name.split('.')[-1].lower() == 'ttf':
            isFile = True
            return name, isFile
        name = [''.join([c for c in f if c.isalnum()]).lower() for f in name.split(',')]
        for fn in name:
            if fn in Font._font:
                return fn, isFile
        for fn in name:
            for ff in Font._font_family:
                if fn in ff:
                    for font in ff:
                        if font in Font._font:
                            return font, isFile
        return Font._font_default, isFile

    def _getFont(self, name, style, size):
        name = os.path.normpath(name)
        dirname, self.fontname = os.path.split(name)
        fontpath = os.path.join(dirname,self.fontname)
        if not env.japplet:
            font = self.createFont(JFont.TRUETYPE_FONT, File(fontpath))
        else:
            font = self.createFont(JFont.TRUETYPE_FONT, env.japplet.getClass().getResourceAsStream(fontpath))
            if not font:
                raise IOError
        return font.deriveFont(style, float(size))

    def render(self, text, antialias, color, background=None):
        """
        Render text onto surface.
        Arguments:
        text to render (string)
        antialias of text (bool)
        color of text (R,G,B)
        background color (R,G,B)
        """
        w,h = self.size(text)
        surf = Surface((w,h), BufferedImage.TYPE_INT_ARGB)
        g2d = surf.createGraphics()
        if background:
            g2d.setColor(Color(background))
            g2d.fillRect(0,0,w,h)
        g2d.setFont(self.font)
        if antialias:
            g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON)
        g2d.setColor(Color(color))
        y = (h//2)-((self.fontMetrics.getAscent()+self.fontMetrics.getDescent())//2)+self.fontMetrics.getAscent()
        if not self.underline:
            g2d.drawString(text,0,y)
        else:
            try:
                text = AttributedString(text)
                text.addAttribute(TextAttribute.FONT,self.font)
                text.addAttribute(TextAttribute.UNDERLINE,TextAttribute.UNDERLINE_ON)
                g2d.drawString(text.getIterator(),0,y)
            except IllegalArgumentException:
                pass
        g2d.dispose()
        return surf

    def size(self, text):
        """
        Return size (width,height) of rendered text.
        """
        width = self.fontMetrics.stringWidth(text)
        if width < 1:
            width = 1
        height = self.fontMetrics.getHeight()
        return (width, height)

    def set_underline(self, setting=True):
        """
        Set font underline style.
        Optional setting, default to True.
        """
        self.underline = setting

    def get_underline(self):
        """
        Check if font is underlined.
        """
        return self.underline

    def set_bold(self, setting=True):
        """
        Set font bold style.
        Optional setting, default to True.
        """
        if setting:
            if self.font.isItalic():
                self.font = self.deriveFont(JFont.BOLD | JFont.ITALIC)
            else:
                self.font = self.deriveFont(JFont.BOLD)
        else:
            if self.font.isItalic():
                self.font = self.deriveFont(JFont.ITALIC)
            else:
                self.font = self.deriveFont(JFont.PLAIN)
        _g2d.setFont(self.font)
        self.fontMetrics = _g2d.getFontMetrics()

    def get_bold(self):
        """
        Check if font is bold.
        """
        return self.font.isBold()

    def set_italic(self, setting=True):
        """
        Set font italic style.
        Optional setting, default to True.
        """
        if setting:
            if self.font.isBold():
                self.font = self.deriveFont(JFont.BOLD | JFont.ITALIC)
            else:
                self.font = self.deriveFont(JFont.ITALIC)
        else:
            if self.font.isBold():
                self.font = self.deriveFont(JFont.BOLD)
            else:
                self.font = self.deriveFont(JFont.PLAIN)
        _g2d.setFont(self.font)
        self.fontMetrics = _g2d.getFontMetrics()

    def get_italic(self):
        """
        Check if font is italized.
        """
        return self.font.isItalic()

    def get_height(self):
        """
        Return height of font.
        """
        return self.fontMetrics.getHeight()

    def get_linesize(self):
        """
        Return linesize of font.
        """
        return self.fontMetrics.getHeight()

    def get_ascent(self):
        """
        Return ascent of font.
        """
        return self.fontMetrics.getAscent()

    def get_descent(self):
        """
        Return descent of font.
        """
        return self.fontMetrics.getDescent()

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.metrics = lambda *arg: []


class SysFont(Font):
    """
    **pyj2d.font.SysFont**
    
    * Font subclass
    """

    def __init__(self, name, size, bold=False, italic=False):
        """
        Return SysFont subclassed of Font.
        Arguments include name of a system font and size of font, with optional bold and italic style. The name argument can be a string of comma-delimited names to specify fallbacks and use a default font if none found.
        """
        self.fontstyle = JFont.PLAIN
        if bold:
            self.fontstyle |= JFont.BOLD
        if italic:
            self.fontstyle |= JFont.ITALIC
        Font.__init__(self,name,size)

