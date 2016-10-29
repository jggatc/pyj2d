#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from java.awt.image import BufferedImage
from java.awt import Toolkit, Point, AWTError
from java.awt import Cursor
from pyj2d import cursors
from pyj2d import env
import pyj2d.event

__docformat__ = 'restructuredtext'


class Mouse(object):
    """
    **pyj2d.mouse**
    
    * pyj2d.mouse.get_pressed
    * pyj2d.mouse.get_pos
    * pyj2d.mouse.get_rel
    * pyj2d.mouse.set_visible
    * pyj2d.mouse.set_cursor
    * pyj2d.mouse.get_cursor
    """

    def __init__(self):
        """
        Provides methods to access the mouse function.
        
        Module initialization creates pyj2d.mouse instance.
        """
        self.mousePress = pyj2d.event.mousePress
        self.mousePos = {'x':0, 'y':0}
        self._cursorVisible = True
        self._cursorBlank = None
        self._cursor = None
        self._nonimplemented_methods()

    def get_pressed(self):
        """
        Return state of mouse buttons as a tuple of bool for button1,2,3.
        """
        return (self.mousePress[1], self.mousePress[2], self.mousePress[3])

    def get_pos(self):
        """
        Return x,y of mouse pointer.
        If the pointer is not in frame, returns -1,-1.
        """
        pos = env.jframe.jpanel.getMousePosition()
        try:
            return (pos.x, pos.y)
        except AttributeError:
            return (-1,-1)

    def get_rel(self):
        """
        Return relative x,y change of mouse position since last call.
        """
        pos = env.jframe.jpanel.getMousePosition()
        if pos:
            rel = pos.x-self.mousePos['x'], pos.y-self.mousePos['y']
            if rel[0] or rel[1]:
                self.mousePos['x'], self.mousePos['y'] = pos.x, pos.y
        else:
            rel = (0,0)
        return rel

    def set_visible(self, visible):
        """
        Set mouse cursor visibility according to visible bool argument.
        Return previous cursor visibility state.
        """
        visible_pre = self._cursorVisible
        if visible:
            if not self._cursor:
                self._cursor = Cursor(Cursor.DEFAULT_CURSOR)
            env.jframe.getContentPane().setCursor(self._cursor)
            self._cursorVisible = True
        else:
            if not self._cursorBlank:
                image = BufferedImage(16, 16, BufferedImage.TYPE_INT_ARGB)
                hotspot = Point(0,0)
                name = 'Blank Cursor'
                try:
                    self._cursorBlank = Toolkit.getDefaultToolkit().createCustomCursor(image, hotspot, name)
                except AWTError:
                    return visible_pre
            env.jframe.getContentPane().setCursor(self._cursorBlank)
            self._cursorVisible = False
        return visible_pre

    def set_cursor(self, *cursor):
        """
        Set mouse cursor.
        Alternative arguments:
        * JVM system cursor or cursor object
        * image or surface, hotspot (x,y), and optional name
        * size, hotspot, data, mask, and optional name
        Refer to pyj2d.cursors for details.
        """
        args = len(cursor)
        if len(cursor) == 1:
            if isinstance(cursor[0], int):
                self._cursor = Cursor(cursor[0])
            else:
                self._cursor = cursor[0]
        elif args in (2,3):
            image = cursor[0]
            hotspot = Point(*cursor[1])
            if args == 2:
                name = 'Custom Cursor'
            else:
                name = cursor[2]
            self._cursor = Toolkit.getDefaultToolkit().createCustomCursor(image, hotspot, name)
        elif args in (4,5):
            size = cursor[0]
            hotspot = Point(*cursor[1])
            data = cursor[2]
            mask = cursor[3]
            if args == 4:
                name = 'Custom Cursor'
            else:
                name = cursor[4]
            surface = cursors.create_cursor(size, data, mask)
            self._cursor = Toolkit.getDefaultToolkit().createCustomCursor(surface, hotspot, name)
        else:
            self._cursor = Cursor(Cursor.DEFAULT_CURSOR)
        if self._cursorVisible:
            env.jframe.getContentPane().setCursor(self._cursor)

    def get_cursor(self):
        """
        Return cursor object.
        Cursor type and name accessed with object getType and getName methods.
        """
        if not self._cursor:
            self._cursor = Cursor(Cursor.DEFAULT_CURSOR)
        return self._cursor

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.set_pos = lambda *arg: None
        self.get_focused = lambda *arg: True

