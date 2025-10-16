#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Event module**

The module manages events.
"""

from java.lang import Thread
from java.awt.event import MouseEvent
from java.awt.event import KeyEvent
from java.awt.event import FocusEvent
from java.awt.event import WindowEvent
from pyj2d import env
from pyj2d import constants as Const


class Event(object):
    """
    Event processing construct.
    """

    def __init__(self):
        """
        Initialize Event object.

        Maintain events received from JVM.
        Module initialization creates pyj2d.event instance.
        """
        self.eventQueue = [None] * 256
        self.eventNum = 0
        self.eventQueueTmp = [None] * 256
        self.eventNumTmp = 0
        self.queueLock = False
        self.queueAccess = False
        self.queue = []
        self.queueNil = []
        self.queueTmp = []
        self.mousePos = {'x':-1, 'y':-1}
        self.mousePress = {1:False, 2:False, 3:False}
        self._nonimplemented_methods()
        self.eventName = {MouseEvent.MOUSE_PRESSED: 'MouseButtonDown',
                          MouseEvent.MOUSE_RELEASED: 'MouseButtonUp',
                          MouseEvent.MOUSE_MOVED: 'MouseMotion',
                          KeyEvent.KEY_PRESSED: 'KeyDown',
                          KeyEvent.KEY_RELEASED: 'KeyUp',
                          Const.ACTIVEEVENT: 'ActiveEvent',
                          Const.WINDOWENTER: 'WindowEnter',
                          Const.WINDOWLEAVE: 'WindowLeave',
                          Const.QUIT: 'Quit'}
        self.eventType = [MouseEvent.MOUSE_PRESSED,
                          MouseEvent.MOUSE_RELEASED,
                          MouseEvent.MOUSE_MOVED,
                          KeyEvent.KEY_PRESSED,
                          KeyEvent.KEY_RELEASED,
                          Const.ACTIVEEVENT,
                          Const.WINDOWENTER,
                          Const.WINDOWLEAVE,
                          Const.QUIT]
        try:
            self.events = set(self.eventType)
            self.eventTypes = set(self.eventType)
            self.modKey = set([Const.K_ALT, Const.K_CTRL, Const.K_SHIFT])
        except NameError:
            from java.util import HashSet as set
            self.events = set(self.eventType)
            self.eventTypes = set(self.eventType)
            self.modKey = set([Const.K_ALT, Const.K_CTRL, Const.K_SHIFT])
        self.keyPress = {Const.K_ALT: False,
                         Const.K_CTRL: False,
                         Const.K_SHIFT: False}
        self.keyMod = {Const.K_ALT: {True: Const.KMOD_ALT, False: 0},
                       Const.K_CTRL: {True: Const.KMOD_CTRL, False: 0},
                       Const.K_SHIFT: {True: Const.KMOD_SHIFT, False: 0}}
        self.keyRepeat = [0, 0]
        self.keyHeld = {}
        self.Event = UserEvent

    def _lock(self):
        self.queueLock = True
        while self.queueAccess:
            Thread.sleep(1)

    def _unlock(self):
        self.queueLock = False

    def _updateQueue(self, event, eventType):
        if eventType not in self.events:
            return
        else:
            event = JEvent(event, eventType)
        self.queueAccess = True
        if not self.queueLock:
            if self.eventNumTmp:
                 self._appendMerge()
            self._append(event)
        else:
            self._appendTmp(event)
        self.queueAccess = False

    def _append(self, event):
        try:
            self.eventQueue[self.eventNum] = event
            self.eventNum += 1
        except IndexError:
            pass

    def _appendTmp(self, event):
        try:
            self.eventQueueTmp[self.eventNumTmp] = event
            self.eventNumTmp += 1
        except IndexError:
            pass

    def _appendMerge(self):
        for i in range(self.eventNumTmp):
            self._append( self.eventQueueTmp[i] )
            self.eventQueueTmp[i] = None
        self.eventNumTmp = 0

    def pump(self):
        """
        Process event queue.

        Process to reduce queue overflow, unnecessary if processing with other methods.
        """
        if self.eventNum > 250:
            self._lock()
            self._pump()
            self._unlock()
        return None

    def _pump(self):
        queue = self.eventQueue[50:self.eventNum]
        self.eventNum -= 50
        for i in range(self.eventNum):
            self.eventQueue[i] = queue[i]

    def get(self, eventType=None):
        """
        Return list of events, and queue is reset.

        Optional eventType argument of single or list of event type(s) to return.
        """
        if not self.eventNum:
            return self.queueNil
        self._lock()
        if not eventType:
            self.queue = self.eventQueue[0:self.eventNum]
            self.eventNum = 0
        else:
            self.queue = []
            try:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type not in eventType:
                        self.queueTmp.append(self.eventQueue[i])
                    else:
                        self.queue.append(self.eventQueue[i])
            except TypeError:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type != eventType:
                        self.queueTmp.append(self.eventQueue[i])
                    else:
                        self.queue.append(self.eventQueue[i])
            if not self.queueTmp:
                self.eventNum = 0
            else:
                self.eventNum = len(self.queueTmp)
                for i in range(self.eventNum):
                    self.eventQueue[i] = self.queueTmp[i]
                self.queueTmp[:] = []
            if self.eventNum > 250:
                self._pump()
        self._unlock()
        return self.queue

    def poll(self):
        """
        Return an event from the queue.

        Return event type NOEVENT if none present.
        """
        self._lock()
        if self.eventNum:
            evt = self.eventQueue.pop(0)
            self.eventNum -= 1
            self.eventQueue.append(None)
            if self.eventNum > 250:
                self._pump()
        else:
            evt = self.Event(Const.NOEVENT)
        self._unlock()
        return evt

    def wait(self):
        """
        Return an event from the queue.

        Wait for an event if none present.
        """
        while True:
            if self.eventNum:
                self._lock()
                evt = self.eventQueue.pop(0)
                self.eventNum -= 1
                self.eventQueue.append(None)
                if self.eventNum > 250:
                    self._pump()
                self._unlock()
                return evt
            else:
                self._unlock()
                Thread.sleep(10)

    def peek(self, eventType=None):
        """
        Check if an event of given type is present.

        Optional eventType argument specifies event type or list, which defaults to all.
        """
        if not self.eventNum:
            return False
        elif eventType is None:
            return True
        self._lock()
        evt = [event.type for event in self.eventQueue[0:self.eventNum]]
        if self.eventNum > 250:
            self._pump()
        self._unlock()
        try:
            for evtType in eventType:
                if evtType in evt:
                    return True
        except TypeError:
            if eventType in evt:
                return True
        return False

    def clear(self, eventType=None):
        """
        Remove events of a given type from queue.

        Optional eventType argument specifies event type or list, which defaults to all.
        """
        if not self.eventNum:
            return None
        self._lock()
        if eventType is None:
            self.eventNum = 0
        else:
            try:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type not in eventType:
                        self.queueTmp.append(self.eventQueue[i])
            except TypeError:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type != eventType:
                        self.queueTmp.append(self.eventQueue[i])
            if not self.queueTmp:
                self.eventNum = 0
            else:
                self.eventNum = len(self.queueTmp)
                for i in range(self.eventNum):
                    self.eventQueue[i] = self.queueTmp[i]
                self.queueTmp[:] = []
            if self.eventNum > 250:
                self._pump()
        self._unlock()
        return None

    def event_name(self, eventType):
        """
        Return event name of a event type.
        """
        try:
            return self.eventName[eventType]
        except KeyError:
            return None

    def set_blocked(self, eventType):
        """
        Block specified event type(s) from queue.

        If None is argument, all event types are blocked.
        """
        if eventType is not None:
            try:
                for evtType in eventType:
                    try:
                        self.events.remove(evtType)
                    except KeyError:
                        pass
            except TypeError:
                try:
                    self.events.remove(eventType)
                except KeyError:
                    pass
        else:
            self.events.clear()
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue.

        If None is argument, all event types are allowed.
        """
        if eventType is not None:
            try:
                for evtType in eventType:
                    self.events.add(evtType)
            except TypeError:
                self.events.add(eventType)
        else:
            for event in self.eventType:
                self.events.add(event)
        return None

    def get_blocked(self, eventType):
        """
        Check if specified event type is blocked from queue.
        """
        if eventType not in self.events:
            return True
        else:
            return False

    def post(self, event):
        """
        Post event to queue.
        """
        self._lock()
        if event.type in self.events:
            self._append(event)
        self._unlock()
        return None

    def _register_event(self, eventType):
        if eventType not in self.eventTypes:
            self.eventTypes.add(eventType)
            self.eventName[eventType] = 'UserEvent'
            self.events.add(eventType)

    def _nonimplemented_methods(self):
        self.set_grab = lambda *arg: None
        self.get_grab = lambda *arg: False


class UserEvent(object):
    """
    UserEvent object.
    """

    __slots__ = ['type', 'attr']

    def __init__(self, eventType, *args, **kwargs):
        """
        UserEvent event object.

        Argument includes eventType (USEREVENT+num).
        Optional attribute argument as dictionary ({str:val}) or keyword arg(s).
        Return user event.
        """
        if args:
            attr = args[0]
        else:
            attr = kwargs
        object.__setattr__(self, "type", eventType)
        object.__setattr__(self, "attr", attr)
        env.event._register_event(eventType)

    def __str__(self):
        return "<Event(%s-%s %r)>" % (self.type,
                                      self.toString(),
                                      self.attr)

    def __repr__(self):
        return "<Event(%s-%s %r)>" % (self.type,
                                      self.toString(),
                                      self.attr)

    def __getattr__(self, attr):
        try:
            return self.attr[attr]
        except KeyError:
            raise AttributeError("'Event' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self.attr[attr] = value

    def toString(self):
        return env.event.event_name(self.type)


class JEvent(object):
    """
    JEvent object.
    """

    __slots__ = ['event', 'type']
    _attr = {
            'button': lambda self: self._getButton(),
            'buttons': lambda self: self._getButtons(),
            'pos': lambda self: (self.event.getX(),self.event.getY()),
            'rel': lambda self: self._getRel(),
            'key': lambda self: self.event.getKeyCode(),
            'unicode': lambda self: self._getUnicode(),
            'mod': lambda self: self.event.getModifiers(),
            'loc': lambda self: self.event.getKeyLocation(),
            'state': lambda self: self._activeState[self.event.getID()],
            'gain': lambda self: self._activeGain[self.event.getID()]
            }
    _mouseEvent = ('button', 'pos')
    _mouseMotionEvent = ('buttons', 'pos', 'rel')
    _keyEvent = ('key', 'unicode', 'mod', 'loc')
    _mousePos = {'x':0, 'y':0}
    _mouseButton = {1:1, 2:2, 3:3, 4:6, 5:7, 6:8, 7:9}
    _mouseWheelButton = {-1:4, 1:5}
    _activeEvent = ('state', 'gain')
    _activeState = {FocusEvent.FOCUS_GAINED: Const.APPINPUTFOCUS,
                    FocusEvent.FOCUS_LOST: Const.APPINPUTFOCUS,
                    MouseEvent.MOUSE_ENTERED: Const.APPMOUSEFOCUS,
                    MouseEvent.MOUSE_EXITED: Const.APPMOUSEFOCUS,
                    WindowEvent.WINDOW_ICONIFIED: Const.APPACTIVE,
                    WindowEvent.WINDOW_DEICONIFIED: Const.APPACTIVE}
    _activeGain = {FocusEvent.FOCUS_GAINED: 1,
                   FocusEvent.FOCUS_LOST: 0,
                   MouseEvent.MOUSE_ENTERED: 1,
                   MouseEvent.MOUSE_EXITED: 0,
                   WindowEvent.WINDOW_ICONIFIED: 0,
                   WindowEvent.WINDOW_DEICONIFIED: 1}
    _enterEvent = ()
    _leaveEvent = ()
    _closeEvent = ()

    def __init__(self, event, eventType):
        """
        Event object wraps Java event.
        
        Event object attributes:
        
        * type: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP,
                ACTIVEEVENT, WINDOWENTER, WINDOWLEAVE, QUIT
        * button: mouse button pressed (1-9)
        * buttons: mouse buttons pressed (1,2,3)
        * pos: mouse position (x,y)
        * rel: mouse relative position change (x,y)
        * key: keycode of key pressed (K_a-K_z...)
        * unicode: char pressed ('a'-'z'...)
        * mod: modifier pressed (KMOD_ALT | KMOD_CTRL | KMOD_SHIFT | KMOD_META)
        * loc: key location (KEY_LOCATION_LEFT | KEY_LOCATION_RIGHT)
        * state: focus state (APPFOCUSMOUSE | APPINPUTFOCUS | APPACTIVE)
        * gain: focus gain (0,1)
        """
        object.__setattr__(self, "event", event)
        object.__setattr__(self, "type", eventType)

    def __str__(self):
        return "<Event(%s-%s %r)>" % (self.type,
                                      self.toString(),
                                      self._dict())

    def __repr__(self):
        return "<Event(%s-%s %r)>" % (self.type,
                                      self.toString(),
                                      self._dict())

    def __getattr__(self, attr):
        try:
            return self._attr[attr](self)
        except (AttributeError, KeyError):
            raise AttributeError("'Event' object has no attribute '%s'" % attr)

    def _dict(self):
        attrDict = {}
        for attr in {Const.MOUSEBUTTONDOWN: self._mouseEvent,
                     Const.MOUSEBUTTONUP: self._mouseEvent,
                     Const.MOUSEMOTION: self._mouseMotionEvent,
                     Const.KEYDOWN: self._keyEvent,
                     Const.KEYUP: self._keyEvent,
                     Const.ACTIVEEVENT: self._activeEvent,
                     Const.WINDOWENTER: self._enterEvent,
                     Const.WINDOWLEAVE: self._leaveEvent,
                     Const.QUIT: self._closeEvent}[self.type]:
            attrDict[attr] = self._attr[attr](self)
        return attrDict

    def _getButton(self):
        if self.event.getID() != MouseEvent.MOUSE_WHEEL:
            return self._mouseButton[self.event.getButton()]
        else:
            return self._mouseWheelButton[self.event.getWheelRotation()]

    def _getButtons(self):
        mod = self.event.getModifiersEx()
        return ((mod&MouseEvent.BUTTON1_DOWN_MASK) == MouseEvent.BUTTON1_DOWN_MASK,
                (mod&MouseEvent.BUTTON2_DOWN_MASK) == MouseEvent.BUTTON2_DOWN_MASK,
                (mod&MouseEvent.BUTTON3_DOWN_MASK) == MouseEvent.BUTTON3_DOWN_MASK)

    def _getRel(self):
        pos =  self.event.getX(), self.event.getY()
        rel = (pos[0] - self.__class__._mousePos['x'],
               pos[1] - self.__class__._mousePos['y'])
        if rel[0] or rel[1]:
            self.__class__._mousePos['x'] = pos[0]
            self.__class__._mousePos['y'] = pos[1]
        return rel

    def _getUnicode(self):
        try:
            char = self.event.getKeyChar()
        except:
            char = ''
        return char

    def __setattr__(self, attr, value):
        raise AttributeError("'Event' object has no attribute '%s'" % attr)

    def toString(self):
        return env.event.event_name(self.type)

    def getEvent(self):
        """
        Return Java event.
        """
        return self.event

