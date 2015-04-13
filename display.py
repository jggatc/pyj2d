#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from javax.swing import JFrame, JPanel
from java.awt import Color, Dimension, Toolkit
from java.awt.image import BufferedImage
from java.awt.event import MouseListener
from java.awt.event import MouseMotionListener
from java.awt.event import MouseWheelListener
from java.awt.event import KeyListener
from java.awt.event import MouseEvent, KeyEvent
from java.lang import Thread, Runnable, InterruptedException
from javax.swing import SwingUtilities
import pyj2d.event
import pyj2d.surface
import pyj2d.env

__docformat__ = 'restructuredtext'


class Frame(JFrame, MouseListener, MouseMotionListener, MouseWheelListener, KeyListener):

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
        self.addMouseWheelListener(self)
        self.addKeyListener(self)
        self.event = pyj2d.event
        self.modKey = pyj2d.event.modKey

    def mousePressed(self, event):
        self.event.mousePress[event.button] = True
        self.event._updateQueue(event, MouseEvent.MOUSE_PRESSED)

    def mouseReleased(self, event):
        self.event.mousePress[event.button] = False
        self.event._updateQueue(event, MouseEvent.MOUSE_RELEASED)

    def mouseEntered(self, event):
        pass

    def mouseExited(self, event):
        self.event.mousePress[1], self.event.mousePress[2], self.event.mousePress[3] = False, False, False
        for keycode in self.modKey:
            if self.event.keyPress[keycode]:
                self.event.keyPress[keycode] = False

    def mouseClicked(self, event):
        pass

    def mouseMoved(self, event):
        self.event._updateQueue(event, MouseEvent.MOUSE_MOVED)

    def mouseDragged(self, event):
        self.event._updateQueue(event, MouseEvent.MOUSE_MOVED)

    def mouseWheelMoved(self, event):
        self.event._updateQueue(event, MouseEvent.MOUSE_PRESSED)

    def keyPressed(self, event):
        if event.keyCode in self.modKey:
            self.event.keyPress[event.keyCode] = True
        self.event._updateQueue(event, KeyEvent.KEY_PRESSED)

    def keyReleased(self, event):
        if event.keyCode in self.modKey:
            self.event.keyPress[event.keyCode] = False
        self.event._updateQueue(event, KeyEvent.KEY_RELEASED)

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


class Display(Runnable):
    """
    **pyj2d.display**

    * pyj2d.display.init
    * pyj2d.display.set_mode
    * pyj2d.display.get_surface
    * pyj2d.display.get_frame
    * pyj2d.display.get_panel
    * pyj2d.display.quit
    * pyj2d.display.get_init
    * pyj2d.display.get_active
    * pyj2d.display.set_caption
    * pyj2d.display.set_icon
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
            self.jframe = None
            self.jpanel = None
            self.surface = None
            self._initialized = True

    def set_mode(self, size, *args, **kwargs):
        """
        Return a display Surface.
        Argument: size (x,y) of surface.
        """
        if pyj2d.env.japplet:
            self.jframe = pyj2d.env.japplet
        else:
            self.jframe = Frame(self.caption, size)
            if self.icon:
                self.jframe.setIconImage(self.icon)
        pyj2d.env.jframe = self.jframe
        self.jpanel = self.jframe.jpanel
        self.surface = self.jpanel.surface
        self.surface._display = self
        self._surface_rect = [self.surface.get_rect()]
        self._rect_list = None
        self.clear()
        self.jframe.setVisible(True)
        self._warmup()
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

    def _warmup(self):
        Surface = pyj2d.surface.Surface
        Sprite = pyj2d.sprite.Sprite
        Group = pyj2d.sprite.Group
        RenderUpdates = pyj2d.sprite.RenderUpdates
        OrderedUpdates = pyj2d.sprite.OrderedUpdates
        surface = [Surface(size) for size in ((5,5), (5,5), (3,3))]
        for i, color in enumerate([(0,0,0), (0,0,0), (100,100,100)]):
            surface[i].fill(color)
        for i in range(500):
            surface[0].blit(surface[2], (1,1))
        sprite = [Sprite() for i in range(3)]
        group = [Grp() for Grp in (Group, RenderUpdates, OrderedUpdates)]
        for i, grp in enumerate(group):
            sprite[i].image = surface[2]
            sprite[i].rect = sprite[i].image.get_rect(center=(2,2))
            grp.add(sprite[i])
        for grp in group:
            for i in range(500):
                grp.clear(surface[0],surface[1])
                grp.draw(surface[0])
        for grp in group:
            grp.empty()
            Group._groups.remove(grp)

    def quit(self):
        """
        Uninitialize display.
        """
        self._initialized = False
        return None

    def get_init(self):
        """
        Check that display module is initialized.
        """
        return self._initialized

    def get_active(self):
        """
        Check if display is visible.
        """
        try:
            return not (self.jframe.getExtendedState() & JFrame.ICONIFIED)
        except AttributeError:
            if self.jframe:
                return True
            else:
                return False

    def set_caption(self, caption, *args, **kwargs):
        """
        Set display caption.
        Argument: caption for JFrame title.
        """
        self.caption = caption
        try:
            self.jframe.setTitle(self.caption)
        except AttributeError:
            pass
        return None

    def set_icon(self, surface):
        """
        Set display icon.
        Argument: Surface for JFrame icon.
        """
        self.icon = surface
        try:
            self.jframe.setIconImage(self.icon)
        except AttributeError:
            pass
        return None

    def clear(self):
        """
        Clear display surface.
        """
        g2d = self.surface.createGraphics()
        g2d.setColor(Color.BLACK)
        g2d.fillRect(0,0,self.surface.getWidth(),self.surface.getHeight())
        g2d.dispose()

    def flip(self):
        """
        Repaint display.
        """
        self._rect_list = self._surface_rect
        try:
            SwingUtilities.invokeAndWait(self)
        except InterruptedException:
            Thread.currentThread().interrupt()

    def update(self, *rect_list):
        """
        Repaint display.
        An optional rect_list to specify regions to repaint.
        """
        if rect_list:
            self._rect_list = rect_list[0]
        else:
            self._rect_list = self._surface_rect
        try:
            SwingUtilities.invokeAndWait(self)
        except InterruptedException:
            Thread.currentThread().interrupt()

    def run(self):
        try:
            for rect in self._rect_list:
                try:
                    self.jpanel.repaint(rect.x,rect.y,rect.width,rect.height)
                except AttributeError:
                    try:
                        self.jpanel.repaint(rect[0],rect[1],rect[2],rect[3])
                    except TypeError:
                        if rect is None:
                            continue
                        else:
                            rect = self._rect_list
                            try:
                                self.jpanel.repaint(rect.x,rect.y,rect.width,rect.height)
                            except AttributeError:
                                self.jpanel.repaint(rect[0],rect[1],rect[2],rect[3])
                            break
        except TypeError:
            if self._rect_list is not None:
                raise ValueError

