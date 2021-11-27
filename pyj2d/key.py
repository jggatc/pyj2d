#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from java.awt.event import KeyEvent
from pyj2d import env
from pyj2d import constants as Const

__docformat__ = 'restructuredtext'


class Key(object):
    """
    **pyj2d.key**
    
    * pyj2d.key.name
    * pyj2d.key.get_mods
    * pyj2d.key.set_repeat
    * pyj2d.key.get_repeat
    """

    def __init__(self):
        """
        Provides methods to access the key function.
        
        Module initialization creates pyj2d.key instance.
        """
        self.keyPress = env.event.keyPress
        self.keyMod = env.event.keyMod
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

    def set_repeat(self, delay=0, interval=0):
        """
        Set key repeat delay (ms) and interval (ms) settings.
        Key repeat initially disabled.
        """
        if delay < 0 or interval < 0:
            raise ValueError('repeat settings must be positive integers')
        if not delay:
            env.event.keyRepeat[0] = 0
            env.event.keyRepeat[1] = 0
        else:
            env.event.keyRepeat[0] = delay
            if interval:
                env.event.keyRepeat[1] = interval
            else:
                env.event.keyRepeat[1] = delay
        return None

    def get_repeat(self):
        """
        Get key repeat settings.
        """
        return env.event.keyRepeat

    def _nonimplemented_methods(self):
        self.get_focused = lambda *arg: None
        self.get_pressed = lambda *arg: None
        self.set_mods = lambda *arg: None

