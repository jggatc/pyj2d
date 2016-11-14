#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from java.lang import Thread, System, InterruptedException
from javax.swing import Timer
from java.awt.event import ActionListener
from java.util.concurrent.atomic import AtomicBoolean
from pyj2d import env
import pyj2d.event

__docformat__ = 'restructuredtext'


class Clock(object):
    """
    **pyj2d.time.Clock**
    
    * Clock.get_time
    * Clock.tick
    * Clock.tick_busy_loop
    * Clock.get_fps
    """

    _repaint_sync = None

    def __init__(self):
        """
        Return Clock.
        """
        self._time = System.nanoTime()//1000000
        self._time_init = self._time
        self._time_diff = [33 for i in range(10)]
        self._pos = 0
        self._thread = Thread()

    def get_time(self):
        """
        Return time (in ms) between last two calls to tick().
        """
        return self._time_diff[self._pos]

    def tick(self, framerate=0):
        """
        Call once per program cycle, returns ms since last call.
        An optional framerate will add pause to limit rate.
        """
        while self._repaint_sync.get():
            try:
                self._thread.sleep(1)
            except InterruptedException:
                Thread.currentThread().interrupt()
                break
        self._time = System.nanoTime()//1000000
        if framerate:
            time_pause = (1000//framerate) - (self._time-self._time_init)
            if time_pause > 0:
                try:
                    self._thread.sleep(time_pause)
                except InterruptedException:
                    Thread.currentThread().interrupt()
                self._time = System.nanoTime()//1000000
        if self._pos:
            self._pos -= 1
        else:
            self._pos = 9
        self._time_diff[self._pos] = self._time-self._time_init
        self._time_init = self._time
        return self._time_diff[self._pos]

    def tick_busy_loop(self, framerate=0):
        """
        Calls tick() with optional framerate.
        Returns ms since last call.
        """
        return self.tick(framerate)

    def get_fps(self):
        """
        Return fps.
        """
        return 1000/(sum(self._time_diff)/10)


class Time(object):

    def __init__(self):
        self._time_init = System.nanoTime()//1000000
        self.Clock = Clock
        self.Clock._repaint_sync = AtomicBoolean(False)

    def get_ticks(self):
        """
        **pyj2d.time.get_ticks**
        
        Return ms since program start.
        """
        return (System.nanoTime()//1000000) - self._time_init

    def delay(self, time):
        """
        **pyj2d.time.delay**
        
        Pause for given time (in ms). Return ms paused.
        """
        start = System.nanoTime()//1000000
        try:
            Thread.sleep(time)
        except InterruptedException:
            Thread.currentThread().interrupt()
        return (System.nanoTime()//1000000) - start

    def wait(self, time):
        """
        **pyj2d.time.wait**
        
        Calls delay(). Return ms paused.
        """
        return self.delay(time)

    def set_timer(self, eventid, time):
        """
        **pyj2d.time.set_timer**
        
        Events of type eventid placed on queue at time (ms) intervals.
        Disable by time of 0.
        """
        if eventid not in _EventTimer.timers:
            _EventTimer.timers[eventid] = _EventTimer(eventid)
        _EventTimer.timers[eventid].set_timer(time)
        return None


class _EventTimer(ActionListener):
    timers = {}

    def __init__(self, eventid):
        self.event = pyj2d.event.Event(eventid)
        self.timer = Timer(0, self)

    def set_timer(self, time):
        if self.timer.isRunning():
            self.timer.stop()
        if time:
            self.timer.setInitialDelay(time)
            self.timer.setDelay(time)
            self.timer.start()

    def actionPerformed(self, evt):
        pyj2d.event.post(self.event)

