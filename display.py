#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from javax.swing import JFrame, JPanel
from java.awt import Color, Dimension, Toolkit
from java.awt.image import BufferedImage
from java.awt.event import MouseListener
from java.awt.event import MouseMotionListener
from java.awt.event import KeyListener
import pyj2d.event
import pyj2d.surface
import pyj2d.env

__docformat__ = 'restructuredtext'


class Frame(JFrame, MouseListener, MouseMotionListener, KeyListener):

    def __init__(self, title, size):
        JFrame.__init__(self, title)
        self.setDefaultCloseOperation(self.EXIT_ON_CLOSE)
        self.setResizable(False)
        self.setSize(size[0],size[1])
        self.setDefaultLookAndFeelDecorated(True)
        self.setBackground(Color.BLACK)
        self.jpanel = Panel(size)
        self.getContentPane().add(self.jpanel)
        self.pack()
        self.addMouseListener(self)
        self.addMouseMotionListener(self)
        self.addKeyListener(self)
        self.event = pyj2d.event

    def mousePressed(self, event):
        self.event.mousePress = event
        self.event._updateQueue(event)

    def mouseReleased(self, event):
        self.event.mousePress = None
        self.event._updateQueue(event)

    def mouseEntered(self, event):
        pass

    def mouseExited(self, event):
        self.event.mousePress = None

    def mouseClicked(self, event):
        pass

    def mouseMoved(self, event):
        self.event._updateQueue(event)

    def mouseDragged(self, event):
        pass

    def keyPressed(self, event):
        self.event._updateQueue(event)

    def keyReleased(self, event):
        self.event._updateQueue(event)

    def keyTyped(self, event):
        pass


class Panel(JPanel):

    def __init__(self, size):
        JPanel.__init__(self)
        self.setPreferredSize(Dimension(size[0],size[1]))
        self.surface = pyj2d.surface.Surface(size, BufferedImage.TYPE_INT_RGB)
        self.setBackground(Color.BLACK)

    def paintComponent(self, g2d):
        self.super__paintComponent(g2d)
        g2d.drawImage(self.surface, 0, 0, None)
        try:
            Toolkit.getDefaultToolkit().sync()
        except:
            pass


class Display(object):
    """
    **pyj2d.display**

    * pyj2d.display.init
    * pyj2d.display.set_mode
    * pyj2d.display.get_surface
    * pyj2d.display.get_frame
    * pyj2d.display.get_panel
    * pyj2d.display.quit
    * pyj2d.display.get_init
    * pyj2d.display.set_caption
    * pyj2d.display.clear
    * pyj2d.display.flip
    * pyj2d.display.update
    """

    def __init__(self):
        """
        Initialize Display module.

        Module initialization creates pyj2d.display instance.        
        """
        self._initialized = False
        self.init()

    def init(self):
        """
        Initialize display.
        """
        if not self._initialized:
            self.caption = ''
            self.icon = None
            self._nonimplemented_methods()
            self._initialized = True

    def set_mode(self, size):
        """
        Return a display Surface.
        Argument: size (x,y) of surface.
        """
        if pyj2d.env.japplet:
            self.jframe = pyj2d.env.japplet
        else:
            self.jframe = Frame(self.caption, size)
        pyj2d.env.jframe = self.jframe
        self.jpanel = self.jframe.jpanel
        self.surface = self.jpanel.surface
        self.surface._display = self
        self.surface._g2d = self.jpanel.surface.createGraphics()
        self.surface._g2d.setBackground(Color.BLACK)
        self.clear()
        self.jframe.setVisible(True)
        return self.surface

    def get_surface(self):
        """
        Return display Surface.
        """
        return self.surface

    def get_frame(self):
        """
        Return JFrame or JApplet.
        """
        return self.jframe

    def get_panel(self):
        """
        Return JPanel.
        """
        return self.jpanel

    def quit(self):
        """
        Uninitialize display.
        """
        try:
            self.surface._g2d.dispose()
        except:
            pass
        self._initialized = False
        return None

    def get_init(self):
        """
        Check that display module is initialized.
        """
        return self._initialized

    def set_caption(self, caption):
        """
        Set display caption.
        Argument: caption for JFrame.
        """
        self.caption = caption
        return None

    def clear(self):
        """
        Clear display surface.
        """
        w, h = self.surface.getWidth(), self.surface.getHeight()
        self.surface._g2d.setColor(Color.BLACK)
        self.surface._g2d.fillRect(0,0,w,h)

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.set_icon = lambda *arg: None

    def flip(self):
        """
        Repaint display.
        """
        self.jpanel.repaint()

    def update(self, rect_list=None):
        """
        Repaint display.
        An optional rect_list to specify regions to repaint.
        """
        try:
            for rect in rect_list:
                try:
                    self.jpanel.repaint(rect.x,rect.y,rect.width,rect.height)
                except AttributeError:
                    self.jpanel.repaint(rect[0],rect[1],rect[2],rect[3])
        except:
            self.jpanel.repaint()

