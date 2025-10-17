#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Mouse module**

The module provides mouse functionality.
"""

from java.awt.image import BufferedImage
from java.awt import Toolkit, Point, AWTError
from java.awt import Cursor
from pyj2d import cursors
from pyj2d import env


class Mouse(object):
    """
    Mouse object.
    """

    def __init__(self):
        """
        Provides methods to access the mouse function.
        
        Module initialization creates pyj2d.mouse instance.
        """
        self.mouseEvt = env.event.mouseEvt
        self.mousePress = env.event.mousePress
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
        """
        pos = env.jframe.jpanel.getMousePosition()
        if pos is not None:
            return (pos.x, pos.y)
        else:
            return (self.mouseEvt['pos']['x'], self.mouseEvt['pos']['y'])

    def get_rel(self):
        """
        Return relative x,y change of mouse position since last call.
        """
        pos = env.jframe.jpanel.getMousePosition()
        if pos:
            rel = pos.x-self.mouseEvt['rel']['x'], pos.y-self.mouseEvt['rel']['y']
            if rel[0] or rel[1]:
                self.mouseEvt['rel']['x'] = pos.x
                self.mouseEvt['rel']['y'] = pos.y
            return rel
        else:
            return (0,0)

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
                    tk = Toolkit.getDefaultToolkit()
                    self._cursorBlank = tk.createCustomCursor(image, hotspot, name)
                except AWTError:
                    return visible_pre
            env.jframe.getContentPane().setCursor(self._cursorBlank)
            self._cursorVisible = False
        return visible_pre

    def get_focused(self):
        """
        Check if mouse has focus.
        """
        return self.mouseEvt['focus']

    def set_cursor(self, *cursor):
        """
        Set mouse cursor.

        Alternative arguments:
        * JVM system cursor or cursor object
        * image or surface, hotspot (x,y), and optional name
        * size, hotspot, data, mask, and optional name
        Refer to cursors module for details.
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
            tk = Toolkit.getDefaultToolkit()
            self._cursor = tk.createCustomCursor(image, hotspot, name)
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
            tk = Toolkit.getDefaultToolkit()
            self._cursor = tk.createCustomCursor(surface, hotspot, name)
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
        self.set_pos = lambda *arg: None

