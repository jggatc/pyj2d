#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

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
from pyj2d.surface import Surface
from pyj2d.rect import Rect
from pyj2d.time import Clock
from pyj2d.sprite import Sprite, Group, RenderUpdates, OrderedUpdates
from pyj2d import env

__docformat__ = 'restructuredtext'


class Frame(JFrame):

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

    def stop(self):
        self.dispose()


class Panel(JPanel, MouseListener, MouseMotionListener, MouseWheelListener, KeyListener):

    def __init__(self, size):
        JPanel.__init__(self)
        self.setPreferredSize(Dimension(size[0],size[1]))
        self.surface = Surface(size, BufferedImage.TYPE_INT_RGB)
        self.setBackground(Color.BLACK)
        self.addMouseListener(self)
        self.addMouseMotionListener(self)
        self.addMouseWheelListener(self)
        self.addKeyListener(self)
        self.setFocusable(True)
        self.requestFocusInWindow()
        self.event = env.event
        self.modKey = env.event.modKey
        self._repainting = Clock._repaint_sync

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

    def paintComponent(self, g2d):
        self.super__paintComponent(g2d)
        g2d.drawImage(self.surface, 0, 0, None)
        try:
            Toolkit.getDefaultToolkit().sync()
        except:
            pass
        self._repainting.set(False)


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
        if env.japplet:
            self.jframe = env.japplet
        else:
            self.jframe = Frame(self.caption, size)
            if self.icon:
                self.jframe.setIconImage(self.icon)
        env.jframe = self.jframe
        self.jpanel = self.jframe.jpanel
        self.surface = self.jpanel.surface
        self.surface._display = self
        self._surfaceRect = self.surface.get_rect()
        self._surface_rect = [self._surfaceRect]
        self._rect_list = None
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
        Return JFrame.
        """
        return self.jframe

    def get_panel(self):
        """
        Return JPanel.
        """
        return self.jpanel

    def _warmup(self):
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

    def flip(self):
        """
        Repaint display.
        """
        self._rect_list = self._surface_rect
        try:
            SwingUtilities.invokeAndWait(self)
        except InterruptedException:
            Thread.currentThread().interrupt()

    def update(self, rect_list=None):
        """
        Repaint display.
        Optional rect or rect list to specify regions to repaint.
        """
        if isinstance(rect_list, list):
            self._rect_list = rect_list
        elif rect_list:
            self._rect_list = [rect_list]
        else:
            self._rect_list = self._surface_rect
        try:
            SwingUtilities.invokeAndWait(self)
        except InterruptedException:
            Thread.currentThread().interrupt()

    def run(self):
        repaint = False
        for rect in self._rect_list:
            if isinstance(rect, Rect):
                if self._surfaceRect.intersects(rect):
                    self.jpanel.repaint(rect)
                    repaint = True
            elif rect:
                if self._surfaceRect.intersects(rect[0],rect[1],rect[2],rect[3]):
                    self.jpanel.repaint(rect[0],rect[1],rect[2],rect[3])
                    repaint = True
        if repaint:
            self.jpanel._repainting.set(True)

