#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from java.lang import Thread, System, InterruptedException
try:
    from threading import Timer
except ImportError:
    pass
import pyj2d.event
import pyj2d.env

__docformat__ = 'restructuredtext'


_time_init = System.nanoTime()/1000000


class Clock(object):
    """
    **pyj2d.time.Clock**
    
    * Clock.get_time
    * Clock.tick
    * Clock.tick_busy_loop
    * Clock.get_fps
    """

    def __init__(self):
        """
        Return Clock.
        """
        self.time = System.nanoTime()/1000000
        self.time_init = self.time
        self.time_diff = [25]*10
        self.pos = 0
        self.tick = self._tick_init
        self.thread = Thread()

    def get_time(self):
        """
        Return time (in ms) between last two calls to tick().
        """
        return self.time_diff[self.pos]

    def _tick_init(self, framerate=0):
        if self.pos < 9:
            self.pos += 1
        else:
            self.pos = 0
            self.tick = self._tick
        self.time = System.nanoTime()/1000000
        self.time_diff[self.pos] = (self.time-self.time_init)
        self.time_init = self.time
        if framerate:
            if self.time_diff[self.pos] > ((1.0/framerate)*1000):
                self.time_diff[self.pos] = ((1.0/framerate)*1000)
                return sum(self.time_diff)/10
            time_diff = self.time_diff[self.pos]
            time_pause = long( ((1.0/framerate)*1000) - time_diff )
            if time_pause > 0:
                try:
                    self.thread.sleep(time_pause)
                except InterruptedException:
                    Thread.currentThread().interrupt()
        return self.time_diff[self.pos]

    def _tick(self, framerate=0):
        """
        Call once per program cycle, returns ms since last call.
        An optional framerate will add pause to limit rate.
        """
        if self.pos < 9:
            self.pos += 1
        else:
            self.pos = 0
        self.time = System.nanoTime()/1000000
        self.time_diff[self.pos] = (self.time-self.time_init)
        self.time_init = self.time
        if framerate:
            time_diff = sum(self.time_diff)/10
            time_pause = long( ((1.0/framerate)*1000) - time_diff )
            if time_pause > 0:
                try:
                    self.thread.sleep(time_pause)
                except InterruptedException:
                    Thread.currentThread().interrupt()
        while pyj2d.env.jframe.jpanel._repainting.get():
            try:
                self.thread.sleep(1)
            except InterruptedException:
                Thread.currentThread().interrupt()
                break
        return self.time_diff[self.pos]

    def tick_busy_loop(self, framerate=0):
        """
        Calls tick() with optional framerate.
        Returns ms since last call.
        """
        time_diff = self.tick(framerate)
        return time_diff

    def get_fps(self):
        """
        Return fps.
        """
        return 1000/(sum(self.time_diff)/10)


def get_ticks():
    """
    **pyj2d.time.get_ticks**
    
    Return ms since program start.
    """
    return (System.nanoTime()/1000000) - _time_init


def delay(time):
    """
    **pyj2d.time.delay**
    
    Pause for given time (in ms). Return ms paused.
    """
    start = System.nanoTime()/1000000
    try:
        Thread.sleep(time)
    except InterruptedException:
        Thread.currentThread().interrupt()
    return (System.nanoTime()/1000000) - start


def wait(time):
    """
    **pyj2d.time.wait**
    
    Calls delay(). Return ms paused.
    """
    pause = delay(time)
    return pause

def set_timer(eventid, time):
    """
    **pyj2d.time.set_timer**

    Events of type eventid placed on queue at time (ms) intervals.
    Disable by time of 0.
    """
    if eventid not in _EventTimer.timers:
        _EventTimer.timers[eventid] = _EventTimer(eventid)
    if time:
        _EventTimer.timers[eventid].start(time)
    else:
        _EventTimer.timers[eventid].cancel()
    return None

class _EventTimer:
    timers = {}

    def __init__(self, eventid):
        self.eventid = eventid
        self.time = 0
        self.timer = None
        self.repeat = True

    def run(self):
        pyj2d.event.post( pyj2d.event.Event(self.eventid) )
        if self.repeat:
            self.timeout()

    def timeout(self):
        self.timer = Timer(self.time/1000.0, self.run, ([]))
        self.timer.start()

    def start(self, time):
        if self.timer:
            self.cancel()
        self.time = time
        self.repeat = True
        self.timeout()

    def cancel(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.repeat = False

