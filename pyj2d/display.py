#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Display module**

The module controls display surface updates and registers interaction events.
"""

from javax.swing import JFrame, JPanel
from java.awt import Color, Dimension, Toolkit
from java.awt.image import BufferedImage
from java.awt.event import MouseListener
from java.awt.event import MouseMotionListener
from java.awt.event import MouseWheelListener
from java.awt.event import KeyListener
from java.awt.event import MouseEvent, KeyEvent
from java.awt.event import FocusEvent
from java.awt.event import FocusListener
from java.awt.event import WindowEvent
from java.awt.event import WindowListener
from java.lang import System
from java.lang import Thread, Runnable, InterruptedException
from javax.swing import SwingUtilities
from pyj2d.surface import Surface
from pyj2d.rect import Rect
from pyj2d.time import Clock
from pyj2d.sprite import Sprite, Group, RenderUpdates, OrderedUpdates
from pyj2d.event import JEvent
from pyj2d import env
from pyj2d import constants as Const


class Frame(JFrame, WindowListener):

    def __init__(self, title, size):
        JFrame.__init__(self, title)
        self.setDefaultCloseOperation(self.DO_NOTHING_ON_CLOSE)
        self.setResizable(False)
        self.setSize(size[0],size[1])
        self.setDefaultLookAndFeelDecorated(True)
        self.setBackground(Color.BLACK)
        self.addWindowListener(self)
        self.event = env.event
        self.jpanel = Panel(size)
        self.getContentPane().add(self.jpanel)
        self.pack()

    def windowIconified(self, event):
        self.event._updateQueue(event, Const.ACTIVEEVENT)

    def windowDeiconified(self, event):
        self.event._updateQueue(event, Const.ACTIVEEVENT)

    def windowOpened(self, event):
        pass

    def windowActivated(self, event):
        pass

    def windowDeactivated(self, event):
        pass

    def windowClosing(self, event):
        self.event._updateQueue(event, Const.QUIT)

    def windowClosed(self, event):
        pass

    def stop(self):
        self.dispose()


class Panel(JPanel, MouseListener,
                    MouseMotionListener,
                    MouseWheelListener,
                    KeyListener,
                    FocusListener):

    def __init__(self, size):
        JPanel.__init__(self)
        self.setPreferredSize(Dimension(size[0],size[1]))
        self.surface = Surface(size, BufferedImage.TYPE_INT_RGB)
        self.canvas = Canvas(self.surface)
        self.display = None
        self.setBackground(Color.BLACK)
        self.addMouseListener(self)
        self.addMouseMotionListener(self)
        self.addMouseWheelListener(self)
        self.addKeyListener(self)
        self.addFocusListener(self)
        self.setFocusable(True)
        self.requestFocusInWindow()
        self.event = env.event
        self.modKey = self.event.modKey
        self.keyRepeat = self.event.keyRepeat
        self.keyHeld = self.event.keyHeld
        self._repainting = Clock._repaint_sync

    def mousePressed(self, event):
        self.event.mousePress[event.button] = True
        self.event._updateQueue(event, MouseEvent.MOUSE_PRESSED)

    def mouseReleased(self, event):
        self.event.mousePress[event.button] = False
        self.event._updateQueue(event, MouseEvent.MOUSE_RELEASED)

    def mouseEntered(self, event):
        self.event.mouseEvt['pos']['x'] = event.getX()
        self.event.mouseEvt['pos']['y'] = event.getY()
        self.event.mouseEvt['rel']['x'] = event.getX()
        self.event.mouseEvt['rel']['y'] = event.getY()
        JEvent._mousePos['x'] = event.getX()
        JEvent._mousePos['y'] = event.getY()
        self.event._updateQueue(event, Const.ACTIVEEVENT)
        self.event._updateQueue(event, Const.WINDOWENTER)

    def mouseExited(self, event):
        self.event.mouseEvt['pos']['x'] = event.getX()
        self.event.mouseEvt['pos']['y'] = event.getY()
        self.event.mousePress[1] = False
        self.event.mousePress[2] = False
        self.event.mousePress[3] = False
        for keycode in self.modKey:
            if self.event.keyPress[keycode]:
                self.event.keyPress[keycode] = False
        self.event._updateQueue(event, Const.ACTIVEEVENT)
        self.event._updateQueue(event, Const.WINDOWLEAVE)

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
        if not self._isPaused(event.keyCode):
            self.event._updateQueue(event, KeyEvent.KEY_PRESSED)

    def keyReleased(self, event):
        if event.keyCode in self.modKey:
            self.event.keyPress[event.keyCode] = False
        self.keyHeld[event.keyCode]['pressed'] = False
        self.event._updateQueue(event, KeyEvent.KEY_RELEASED)

    def focusGained(self, event):
        self.event.mouseEvt['focus'] = True
        self.event._updateQueue(event, Const.ACTIVEEVENT)

    def focusLost(self, event):
        self.event.mouseEvt['focus'] = False
        self.event._updateQueue(event, Const.ACTIVEEVENT)

    def _isPaused(self, keycode):
        if keycode not in self.keyHeld:
            self.keyHeld[keycode] = {'pressed':False,
                                     'delay':False,
                                     'time':0}
        key = self.keyHeld[keycode]
        if not key['pressed']:
            key['pressed'] = True
            paused = False
            if self.keyRepeat[0]:
                key['delay'] = True
                key['time'] = System.nanoTime()//1000000
        else:
            paused = True
            if self.keyRepeat[0]:
                time = System.nanoTime()//1000000
                if key['delay']:
                    if time - key['time'] > self.keyRepeat[0]:
                        key['time'] = time
                        key['delay'] = False
                        paused = False
                elif time - key['time'] > self.keyRepeat[1]:
                    key['time'] = time
                    paused = False
        return paused

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


class Canvas(object):

    def __init__(self, surface):
        self._surface = surface

    def _set_surface(self, surface):
        self._surface = surface

    def __getattr__(self, name):
        return getattr(self._surface, name)

    def __str__(self):
        return self._surface.__str__()

    def __repr__(self):
        return self._surface.__repr__()

    def __dir__(self):
        return dir(self._surface)


class Display(Runnable):
    """
    Display object.
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
        Initialize display module.
        """
        if not self._initialized:
            self.caption = ''
            self.icon = None
            self.jframe = None
            self.jpanel = None
            self.canvas = None
            self._initialized = True

    def set_mode(self, size, *args, **kwargs):
        """
        Return a display Surface.

        Argument: size (width, height) of surface.
        """
        if env.japplet:
            self.jframe = env.japplet
        else:
            self.jframe = Frame(self.caption, size)
            if self.icon:
                self.jframe.setIconImage(self.icon)
        env.jframe = self.jframe
        self.jpanel = self.jframe.jpanel
        self.canvas = self.jpanel.canvas
        self.jpanel.display = self
        self._surfaceRect = self.canvas.get_rect()
        self._surface_rect = [self._surfaceRect]
        self._rect_list = None
        self.jframe.setLocationRelativeTo(None)
        self.jframe.setVisible(True)
        self._warmup()
        return self.canvas

    def get_surface(self):
        """
        Return display Surface.
        """
        return self.canvas

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
        Check if display is initialized.
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

    def set_caption(self, caption, *args):
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

