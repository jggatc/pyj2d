#PyJ2D - Copyright (C) 2011 James Garnon

from java.awt.event import KeyEvent

__docformat__ = 'restructuredtext'


class Key(object):
    """
    **pyj2d.key**
    
    * pyj2d.key.name
    """

    def __init__(self):
        """
        Provides methods to access the key function.
        
        Module initialization creates pyj2d.key instance.
        """
        self._nonimplemented_methods()

    def name(self, keycode):
        """
        Return name of key of a keycode.
        """
        return KeyEvent.getKeyText(keycode)

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.get_focused = lambda *arg: None
        self.get_pressed = lambda *arg: None
        self.get_mods = lambda *arg: 0
        self.set_mods = lambda *arg: None
        self.set_repeat = lambda *arg: None
        self.get_repeat = lambda *arg: True

