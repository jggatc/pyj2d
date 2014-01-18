#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from java.lang import Thread
from java.awt.event import MouseEvent, KeyEvent
import time
import locals as Const  #0.22

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
        self.eventQueue = [None] * 256      #max 256: Error: Event queue full
        self.eventNum = 0
        self.eventQueueTmp = [None] * 256   #used when main queue is locked
        self.eventNumTmp = 0
        self.eventAllowed = []
        self.eventBlocked = []
        self.queueLock = False
        self.queueAccess = False
        self.queue = []
        self.mousePress = None
        self.timer = time.Clock()
        self._nonimplemented_methods()
        self.eventName = {MouseEvent.MOUSE_PRESSED:'MouseButtonDown', MouseEvent.MOUSE_RELEASED:'MouseButtonUp', MouseEvent.MOUSE_MOVED:'MouseMotion', KeyEvent.KEY_PRESSED:'KeyDown', KeyEvent.KEY_RELEASED:'KeyUp'}
        self.eventType = [MouseEvent.MOUSE_PRESSED, MouseEvent.MOUSE_RELEASED, MouseEvent.MOUSE_MOVED, KeyEvent.KEY_PRESSED, KeyEvent.KEY_RELEASED]
        self.events = [MouseEvent.MOUSE_PRESSED, MouseEvent.MOUSE_RELEASED, MouseEvent.MOUSE_MOVED, KeyEvent.KEY_PRESSED, KeyEvent.KEY_RELEASED]

    def _lock(self):
        self.queueLock = True   #block next event access
        while self.queueAccess:      #complete current event access
            Thread.sleep(1)       #~should be via separate Java event thread

    def _unlock(self):
        self.queueLock = False

    def _updateQueue(self, event):
        if event.getID() not in self.events:
            return
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
        Reset event queue.
        """
        self._lock()
        self.eventNum = 0
        self._unlock()
        return None

    def get(self, eventType=None):
        """
        Return list of events, and queue is reset.
        Optional eventType argument of single or list of event type(s) to return.
        """
        self._lock()
        if not eventType:
            self.queue = [ self.JEvent(event) for event in self.eventQueue[0:self.eventNum] ]
            self.eventNum = 0
        else:
            queue = []      #0.23
            self.queue = []
            try:
                for i in range(self.eventNum):
                    if self.eventQueue[i].getID() not in eventType:
                        queue.append(self.eventQueue[i])
                    else:
                        self.queue.append( self.JEvent(self.eventQueue[i]) )
            except TypeError:
                for i in range(self.eventNum):
                    if self.eventQueue[i].getID() != eventType:
                        queue.append(self.eventQueue[i])
                    else:
                        self.queue.append( self.JEvent(self.eventQueue[i]) )
            if len(queue) != self.eventNum:
                self.eventNum = len(queue)
                for i in range(self.eventNum):
                    self.eventQueue[i] = queue[i]
        self._unlock()
        return self.queue

    def poll(self):   #0.23
        """
        Return an event from the queue, or event type NOEVENT if none present.
        """
        self._lock()
        if self.eventNum:
            evt = self.JEvent( self.eventQueue.pop(0) )
            self.eventNum -= 1
            self.eventQueue.append(None)
        else:
            evt = self.Event(Const.NOEVENT)
        self._unlock()
        return evt

    def wait(self):   #0.23
        """
        Return an event from the queue, or wait for an event if none present.
        """
        while True:
            if self.eventNum:
                self._lock()
                evt = self.JEvent( self.eventQueue.pop(0) )
                self.eventNum -= 1
                self.eventQueue.append(None)
                self._unlock()
                return evt
            else:
                self._unlock()
                Thread.sleep(10)

    def peek(self, eventType):
        """
        Check if an event of given type is present.
        The eventType argument can be a single event type or a list.
        """
        if not self.eventNum:
            return False
        self._lock()
        evt = [event.getID() for event in self.eventQueue[0:self.eventNum]]
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
            queue = []
            try:
                for i in range(self.eventNum):
                    if self.eventQueue[i].getID() not in eventType:
                        queue.append(self.eventQueue[i])
            except TypeError:
                for i in range(self.eventNum):
                    if self.eventQueue[i].getID() != eventType:
                        queue.append(self.eventQueue[i])
            if len(queue) != self.eventNum:
                self.eventNum = len(queue)
                for i in range(self.eventNum):
                    self.eventQueue[i] = queue[i]
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
                    except ValueError:
                        pass
            except TypeError:
                try:
                    self.events.remove(eventType)
                except ValueError:
                    pass
        else:
            self.events = self.eventType[:]
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue. 
        """
        if eventType is not None:
            try:
                for evtType in eventType:
                    if evtType not in self.events:
                        self.events.append(evtType)
            except TypeError:
                if eventType not in self.events:
                    self.events.append(eventType)
        else:
            self.events = []
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

    class Event(object):    #0.22

        __slots__ = ['type', 'attr']

        def __init__(self, eventType, attr=None):
            """
            Return user event.
            Argument includes eventType (USEREVENT+num).
            Optional attribute argument as dictionary ({str:val}) or keyword arg(s).
            """
            object.__setattr__(self, "type", eventType)
            object.__setattr__(self, "attr", attr)

        def __repr__(self):
            """
            Return string representation of Event object.
            """
            return "%s(%s-UserEvent %r)" % (self.__class__, self.type, self.attr)

        def __setattr__(self, attr, value):
            raise AttributeError, ("'Event' object has no attribute '%s'" % attr)


    class JEvent(object):

        __slots__ = ['event']
        _mouse_pos = (0, 0)

        def __init__(self, event):
            """
            Event object wraps Java event, created when retrieving events from queue.
            
            Event object attributes:
            
            * type: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP
            * button: mouse button pressed (1/2/3)
            * pos: mouse position (x,y)
            * rel: mouse relative position change (x,y)
            * key: keycode of key pressed (K_a-K_z...)
            * unicode: char pressed ('a'-'z'...)
            * mod: modifier pressed (KMOD_ALT | KMOD_CTRL | KMOD_SHIFT | KMOD_META)
            * location: modifier place - (KEY_LOCATION_LEFT or KEY_LOCATION_RIGHT)
            """
            object.__setattr__(self, "event", event)

        def __repr__(self):
            """
            Return string representation of Event object.
            """
            try:
                return "%s(%s)" % (self.__class__, self.event.toString())
            except AttributeError:      #User Event
                return self.event.__repr__()

        def __getattr__(self, attr):
            try:
                if attr == 'type':
                    return self.event.getID()
                elif attr == 'button':
                    return self.event.getButton()
                elif attr == 'pos':
                    return ( self.event.getX(),self.event.getY() )
                elif attr == 'rel':
                    pos =  self.event.getX(), self.event.getY()
                    rel = (pos[0]-self.__class__._mouse_pos[0], pos[1]-self.__class__._mouse_pos[1])
                    self.__class__._mouse_pos = pos
                    return rel
                elif attr == 'key':
                    return self.event.getKeyCode()
                elif attr == 'unicode':
                    char = self.event.getKeyChar()
                    if char == KeyEvent.CHAR_UNDEFINED:
                        char = ''
                    return char
                elif attr == 'mod':
                    return self.event.getModifiers()
                elif attr == 'location':
                    return self.event.getKeyLocation()
                else:
                    raise AttributeError
            except AttributeError:      #User Event     #0.22
                try:
                    return self.event.__getattribute__(attr)
                except AttributeError:
                    try:
                        return self.event.__getattribute__('attr')[attr]
                    except AttributeError:
                        raise AttributeError, ("'Event' object has no attribute '%s'" % attr)
                    except KeyError:
                        raise AttributeError, ("'Event' object has no attribute '%s'" % attr)

        def __setattr__(self, attr, value):     #0.22
            raise AttributeError, ("'Event' object has no attribute '%s'" % attr)

        def getEvent(self):
            """
            Return Java event.
            """
            return self.event

