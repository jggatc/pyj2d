#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Util module**

The module provides profiling functionality.
"""

from java.lang import System


class Timer(object):
    """
    Simple profiling timer.

    Output log to terminal.
    """

    def __init__(self):
        """
        Initialize timer object.
        """
        self.time_i = self.get_time()
        self.dtime = []
        self.number = 0
        self.log_num = 0

    def get_time(self):
        """
        Get current time.
        """
        return System.nanoTime()/1000000.0

    def set_time(self):
        """
        Set current time.
        """
        self.time_i = self.get_time()

    def lap_time(self, time_i=None, time_f=None, number=100, print_result=True):
        """
        Time lapsed since previous set_time.

        Optional arguments time_i and time_f, number of calls to average, and print results to output.
        Return lapsed time on completion.
        """
        if time_i is None:
            time_i = self.time_i
        if time_f is None:
            time_f = self.get_time()
        self.dtime.append(time_f-time_i)
        self.number += 1
        if self.number >= number:
            t_ave = sum(self.dtime)/number
            self.dtime = []
            self.number = 0
            if print_result:
                self.log_num += 1
                entry = "Time %d: %0.2f" % (self.log_num, t_ave)
                print(entry)
            return t_ave


class _dict(dict):
    values = dict.itervalues
    keys = dict.iterkeys
    items = dict.iteritems


def _next(obj):
    return obj.next()


try:
    _range = xrange
except NameError:
    _range = range

