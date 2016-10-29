#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from java.awt.event import KeyEvent
import pyj2d.event
from pyj2d import locals as Const

__docformat__ = 'restructuredtext'


class Key(object):
    """
    **pyj2d.key**
    
    * pyj2d.key.name
    * pyj2d.key.get_mods
    """

    def __init__(self):
        """
        Provides methods to access the key function.
        
        Module initialization creates pyj2d.key instance.
        """
        self.keyPress = pyj2d.event.keyPress
        self.keyMod = pyj2d.event.keyMod
        self.alt = Const.K_ALT
        self.ctrl = Const.K_CTRL
        self.shift = Const.K_SHIFT
        self._nonimplemented_methods()

    def name(self, keycode):
        """
        Return name of key of a keycode.
        """
        return KeyEvent.getKeyText(keycode)

    def get_mods(self):
        """
        Return int modifier keys alt|ctrl|shift.
        """
        return self.keyMod[self.alt][self.keyPress[self.alt]] | self.keyMod[self.ctrl][self.keyPress[self.ctrl]] | self.keyMod[self.shift][self.keyPress[self.shift]]

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.get_focused = lambda *arg: None
        self.get_pressed = lambda *arg: None
        self.set_mods = lambda *arg: None
        self.set_repeat = lambda *arg: None
        self.get_repeat = lambda *arg: True

