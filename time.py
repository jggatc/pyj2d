#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from java.lang import Thread, System, InterruptedException
from javax.swing import Timer
from java.awt.event import ActionListener
from java.util.concurrent.atomic import AtomicBoolean
from pyj2d import env

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
        Call once per program cycle, returns ms since last call.
        An optional framerate will add pause to limit rate.
        """
        return self.tick(framerate)

    def get_fps(self):
        """
        Return fps.
        """
        return 1000.0/(sum(self._time_diff)/10)


class Time(object):
    """
    **pyj2d.time**
    
    * time.get_ticks
    * time.delay
    * time.wait
    * time.set_timer
    * time.time
    * time.timeout
    * time.Clock
    """

    def __init__(self):
        self._time_init = System.nanoTime()//1000000
        self.Clock = Clock
        self.Clock._repaint_sync = AtomicBoolean(False)
        self._timers = {}

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
        
        Pause for given time (in ms). Return ms paused.
        """
        return self.delay(time)

    def set_timer(self, event, time, once=False):
        """
        **pyj2d.time.set_timer**

        Post event on queue at time (ms) intervals.
        Optional argument once set no timer repeat, defaults to False.
        Disable timer with time of 0. 
        """
        if hasattr(event, 'type'):
            eventType = event.type
            if eventType not in self._timers:
                self._timers[eventType] = _EventTimer(event)
        else:
            eventType = event
            if eventType not in self._timers:
                evt = env.event.Event(eventType)
                self._timers[eventType] = _EventTimer(evt)
        repeat = not once
        self._timers[eventType].set_timer(time, repeat)
        return None

    def _stop_timers(self):
        for eventType in self._timers:
            self._timers[eventType].set_timer(0, False)


class _EventTimer(ActionListener):

    def __init__(self, event):
        self.event = event
        self.timer = Timer(0, self)
        self.repeat = True

    def set_timer(self, time, repeat):
        if self.timer.isRunning():
            self.timer.stop()
        if time:
            self.repeat = repeat
            self.timer.setInitialDelay(time)
            self.timer.setDelay(time)
            self.timer.start()

    def actionPerformed(self, evt):
        env.event.post(self.event)
        if not self.repeat:
            self.timer.stop()

