#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from java.lang import Thread
from java.awt.event import MouseEvent, KeyEvent
from pyj2d import locals as Const

__docformat__ = 'restructuredtext'


class Event(object):
    """
    **pyj2d.event**
    
    * pyj2d.event.pump
    * pyj2d.event.get
    * pyj2d.event.poll
    * pyj2d.event.wait
    * pyj2d.event.peek
    * pyj2d.event.clear
    * pyj2d.event.event_name
    * pyj2d.event.set_blocked
    * pyj2d.event.set_allowed
    * pyj2d.event.get_blocked
    * pyj2d.event.post
    * pyj2d.event.Event
    """

    def __init__(self):
        """
        Maintain events received from JVM.
        
        Module initialization creates pyj2d.event instance.
        """
        self.eventQueue = [None] * 256      #max 256
        self.eventNum = 0
        self.eventQueueTmp = [None] * 256   #used when main queue is locked
        self.eventNumTmp = 0
        self.queueLock = False
        self.queueAccess = False
        self.queue = []
        self.queueNil = []
        self.queueTmp = []
        self.mousePress = {1:False, 2:False, 3:False}
        self._nonimplemented_methods()
        self.eventName = {MouseEvent.MOUSE_PRESSED:'MouseButtonDown', MouseEvent.MOUSE_RELEASED:'MouseButtonUp', MouseEvent.MOUSE_MOVED:'MouseMotion', KeyEvent.KEY_PRESSED:'KeyDown', KeyEvent.KEY_RELEASED:'KeyUp'}
        self.eventType = [MouseEvent.MOUSE_PRESSED, MouseEvent.MOUSE_RELEASED, MouseEvent.MOUSE_MOVED, KeyEvent.KEY_PRESSED, KeyEvent.KEY_RELEASED]
        try:
            self.events = set(self.eventType)
            self.modKey = set([Const.K_ALT, Const.K_CTRL, Const.K_SHIFT])
        except NameError:
            from java.util import HashSet as set
            self.events = set(self.eventType)
            self.modKey = set([Const.K_ALT, Const.K_CTRL, Const.K_SHIFT])
        self.keyPress = {Const.K_ALT:False, Const.K_CTRL:False, Const.K_SHIFT:False}
        self.keyMod = {Const.K_ALT:{True:Const.KMOD_ALT,False:0}, Const.K_CTRL:{True:Const.KMOD_CTRL,False:0}, Const.K_SHIFT:{True:Const.KMOD_SHIFT,False:0}}
        self.Event = UserEvent

    def _lock(self):
        self.queueLock = True   #block next event access
        while self.queueAccess:      #complete current event access
            Thread.sleep(1)       #~should be via separate Java event thread

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
        Process events to reduce queue overflow, unnecessary if processing with other methods.
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
        Return an event from the queue, or event type NOEVENT if none present.
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
        Return an event from the queue, or wait for an event if none present.
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
            for event in self.eventType:
                self.events.add(event)
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue. 
        """
        if eventType is not None:
            try:
                for evtType in eventType:
                    self.events.add(evtType)
            except TypeError:
                self.events.add(eventType)
        else:
            self.events.clear()
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
        self._append(event)
        self._unlock()
        return None

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.set_grab = lambda *arg: None
        self.get_grab = lambda *arg: False


class UserEvent(object):

    __slots__ = ['type', 'attr']

    def __init__(self, eventType, *args, **kwargs):
        """
        Return user event.
        Argument includes eventType (USEREVENT+num).
        Optional attribute argument as dictionary ({str:val}) or keyword arg(s).
        """
        if args:
            attr = args[0]
        else:
            attr = kwargs
        object.__setattr__(self, "type", eventType)
        object.__setattr__(self, "attr", attr)

    def __repr__(self):
        """
        Return string representation of Event object.
        """
        return "%s(%s-UserEvent %r)" % (self.__class__, self.type, self.attr)

    def __getattr__(self, attr):
        try:
            return self.attr[attr]
        except KeyError:
            raise AttributeError("'Event' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        raise AttributeError("'Event' object has no attribute '%s'" % attr)


class JEvent(object):

    __slots__ = ['event', 'type']
    _attr = {
            'button': lambda self: self._getButton(),
            'buttons': lambda self: self._getButtons(),
            'pos': lambda self: ( self.event.getX(),self.event.getY() ),
            'rel': lambda self: self._getRel(),
            'key': lambda self: self.event.getKeyCode(),
            'unicode': lambda self: self._getUnicode(),
            'mod': lambda self: self.event.getModifiers(),
            'loc': lambda self: self.event.getKeyLocation(),
            'dict': lambda self: self._dict()
            }
    _mouseEvent = ('button', 'pos')
    _mouseMotionEvent = ('buttons', 'pos', 'rel')
    _keyEvent = ('key', 'unicode', 'mod', 'loc')
    _mousePos = {'x':0, 'y':0}
    _mouseRel = {'x':0, 'y':0}
    _mouseButton = {1:1, 2:2, 3:3, 4:6, 5:7}
    _mouseWheelButton = {-1:4, 1:5}

    def __init__(self, event, eventType):
        """
        Event object wraps Java event.
        
        Event object attributes:
        
        * type: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP
        * button: mouse button pressed (1-7)
        * buttons: mouse buttons pressed (1,2,3)
        * pos: mouse position (x,y)
        * rel: mouse relative position change (x,y)
        * key: keycode of key pressed (K_a-K_z...)
        * unicode: char pressed ('a'-'z'...)
        * mod: modifier pressed (KMOD_ALT | KMOD_CTRL | KMOD_SHIFT | KMOD_META)
        * loc: key location (KEY_LOCATION_LEFT | KEY_LOCATION_RIGHT)
        """
        object.__setattr__(self, "event", event)
        object.__setattr__(self, "type", eventType)

    def __repr__(self):
        """
        Return string representation of Event object.
        """
        return "%s(%s)" % (self.__class__, self.event.toString())

    def __getattr__(self, attr):
        try:
            return self._attr[attr](self)
        except (AttributeError, KeyError):
            raise AttributeError("'Event' object has no attribute '%s'" % attr)

    def _dict(self):
        attrDict = {}
        for attr in {Const.MOUSEBUTTONDOWN:self._mouseEvent, Const.MOUSEBUTTONUP:self._mouseEvent, Const.MOUSEMOTION:self._mouseMotionEvent, Const.KEYDOWN:self._keyEvent, Const.KEYUP:self._keyEvent}[self.type]:
            attrDict[attr] = self._attr[attr](self)
        return attrDict

    def _getButton(self):
        if self.event.getID() != MouseEvent.MOUSE_WHEEL:
            return self._mouseButton[self.event.getButton()]
        else:
            return self._mouseWheelButton[self.event.getWheelRotation()]

    def _getButtons(self):
        mod = self.event.getModifiersEx()
        return ((mod&MouseEvent.BUTTON1_DOWN_MASK) == MouseEvent.BUTTON1_DOWN_MASK, (mod&MouseEvent.BUTTON2_DOWN_MASK) == MouseEvent.BUTTON2_DOWN_MASK, (mod&MouseEvent.BUTTON3_DOWN_MASK) == MouseEvent.BUTTON3_DOWN_MASK)

    def _getRel(self):
        pos =  self.event.getX(), self.event.getY()
        rel = (pos[0]-self.__class__._mousePos['x'], pos[1]-self.__class__._mousePos['y'])
        if rel[0] or rel[1]:
            self.__class__._mousePos['x'], self.__class__._mousePos['y'] = pos[0], pos[1]
            self.__class__._mouseRel['x'], self.__class__._mouseRel['y'] = rel[0], rel[1]
        else:
            rel = (self.__class__._mouseRel['x'], self.__class__._mouseRel['y'])
        return rel

    def _getUnicode(self):
        char = self.event.getKeyChar()
        if char == KeyEvent.CHAR_UNDEFINED:
            char = ''
        return char

    def __setattr__(self, attr, value):
        raise AttributeError("'Event' object has no attribute '%s'" % attr)

    def getEvent(self):
        """
        Return Java event.
        """
        return self.event

