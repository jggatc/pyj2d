#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from java.awt import Font as JFont
from java.awt import BasicStroke, RenderingHints, GraphicsEnvironment   #0.23
from java.awt.image import BufferedImage
import surface
from color import Color     #0.23

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
    _surf = surface.Surface((1,1), BufferedImage.TYPE_INT_RGB)
    _g2d = _surf.createGraphics()
    match_font = lambda *arg: None      #nonimplemented_methods
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
    return 'Arial'


def get_fonts():
    """
    **pyj2d.font.get_fonts**
    
    Return fonts available in JVM.
    """
    GraphicsEnv = GraphicsEnvironment.getLocalGraphicsEnvironment()
    return GraphicsEnv.getAvailableFontFamilyNames()


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
    """

    def __init__(self, name, size):
        """
        Return Font subclassed of java.awt.Font.
        Arguments include name and size of font.
        Currently font name limited to 'Arial'.
        """
        self.fontname = 'Arial'
        self.fontsize = size
        try:
            self.fontstyle = self._style
        except AttributeError:
            self.fontstyle = JFont.PLAIN
        JFont.__init__(self,self.fontname,self.fontstyle,self.fontsize)
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
        surf = surface.Surface((w,h), BufferedImage.TYPE_INT_ARGB)
        g2d = surf.createGraphics()
        if background:
            g2d.setColor(Color(background))     #0.23
            g2d.fillRect(0,0,w,h)
        g2d.setFont(self.font)
        if antialias:
            g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON)
        g2d.setColor(Color(color))      #0.23
        g2d.drawString(text,0,(h//2)+(self.fontMetrics.getAscent()//2))    #0.22
        if self.underline:
            g2d.setStroke(BasicStroke(1))
            g2d.drawLine(0,h-1,w-1,h-1)     #0.22
        g2d.dispose()
        return surf

    def size(self, text):       #use getBounds
        """
        Return size x,y of a surface for of given text.
        """
        x = self.fontMetrics.stringWidth(text)      #0.22
        if x < 1:
            x = 1
        y = self.fontMetrics.getHeight()
        return (x, y)

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
                self.font = self

    def get_bold(self):
        """
        Check if font is bold.
        """
        return self.font.isBold()

    def set_italic(self, setting=True):     #redo metrics
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
                self.font = self

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

    def get_linesize(self):     #0.22
        """
        Return linesize of font.
        """
        return self.fontMetrics.getHeight()

    def get_ascent(self):     #0.22     ###
        """
        Return ascent of font.
        """
        return self.fontMetrics.getAscent()

    def get_descent(self):     #0.22
        """
        Return descent of font.
        """
        return self.fontMetrics.getDescent()

    def _nonimplemented_methods(self):      #0.22
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
        Arguments include name and size of font, with optional bold and italic style.
        Currently font name limited to 'Arial'.
        """
        self._style = JFont.PLAIN
        if bold:
            self._style |= JFont.BOLD
        if italic:
            self._style |= JFont.ITALIC
        Font.__init__(self,name,size)

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
                if self._style:
                    self.font = self.deriveFont(JFont.PLAIN)
                else:
                    self.font = self

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
                if self._style:
                    self.font = self.deriveFont(JFont.PLAIN)
                else:
                    self.font = self

