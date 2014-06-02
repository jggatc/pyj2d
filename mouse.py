#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
import env
import pyj2d.event

__docformat__ = 'restructuredtext'


class Mouse(object):
    """
    **pyj2d.mouse**
    
    * pyj2d.mouse.get_pressed
    * pyj2d.mouse.get_pos
    * pyj2d.mouse.get_rel
    """

    def __init__(self):
        """
        Provides methods to access the mouse function.
        
        Module initialization creates pyj2d.mouse instance.
        """
        self.mousePress = pyj2d.event.mousePress
        self.mousePos = {'x':0, 'y':0}
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

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.set_pos = lambda *arg: None
        self.set_visible = lambda *arg: True
        self.get_focused = lambda *arg: True
        self.set_cursor = lambda *arg: None
        self.get_cursor = lambda *arg: ()

