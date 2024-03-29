#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from java.awt import Color as _Color

__docformat__ = 'restructuredtext'


class Color(_Color):

    def __init__(self, *color):
        """
        Return Color object.
        
        Alternative arguments:
        
        * r,g,b,a
        * r,g,b
        * (r,g,b,a)
        * (r,g,b)
        * integer rgba
        * Color

        Color has the attributes::
        
            r, g, b, a

        Module initialization places pyj2d.Color in module's namespace.
        """
        if len(color) == 1:
            color = color[0]
        try:
            r = color[0]
            g = color[1]
            b = color[2]
            a = color[3]
        except IndexError:
            r = color[0]
            g = color[1]
            b = color[2]
            a = 255
        except (TypeError, AttributeError):
            r = (color>>16) & 0xff
            g = (color>>8) & 0xff
            b = color & 0xff
            a = (color>>24) & 0xff
        _Color.__init__(self, r, g, b, a)

    def __str__(self):
        return "(%d, %d, %d, %d)" % (self.getRed(),
                                     self.getGreen(),
                                     self.getBlue(),
                                     self.getAlpha())

    def __repr__(self):
        return "(%d, %d, %d, %d)" % (self.getRed(),
                                     self.getGreen(),
                                     self.getBlue(),
                                     self.getAlpha())

    def __getattr__(self, attr):
        try:
            return {'r': self.getRed,
                    'g': self.getGreen,
                    'b': self.getBlue,
                    'a': self.getAlpha}[attr]()
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, val):
        if not hasattr(self, '_color'):
            color = {'r': self.getRed(),
                     'g': self.getGreen(),
                     'b': self.getBlue(),
                     'a': self.getAlpha()}
            object.__setattr__(self, '_color', color)
            object.__setattr__(self, 'getRed', self._getRed)
            object.__setattr__(self, 'getGreen', self._getGreen)
            object.__setattr__(self, 'getBlue', self._getBlue)
            object.__setattr__(self, 'getAlpha', self._getAlpha)
        self._color[attr] = val
        return None

    def __getitem__(self, index):
        return {0: self.getRed,
                1: self.getGreen,
                2: self.getBlue,
                3: self.getAlpha}[index]()

    def __setitem__(self, index, val):
        self.__setattr__({0: 'r',
                          1: 'g',
                          2: 'b',
                          3: 'a'}[index], val)

    def __iter__(self):
        return iter([self.getRed(),
                     self.getGreen(),
                     self.getBlue(),
                     self.getAlpha()])

    def __len__(self):
        return 4

    def _getRed(self):
        return self._color['r']

    def _getGreen(self):
        return self._color['g']

    def _getBlue(self):
        return self._color['b']

    def _getAlpha(self):
        return self._color['a']

    def __eq__(self, other):
        try:
            return (self.r == other.r and
                    self.g == other.g and
                    self.b == other.b and
                    self.a == other.a)
        except AttributeError:
            try:
                return (self.a == other[3] and 
                        self.r == other[0] and
                        self.g == other[1] and
                        self.b == other[2])
            except IndexError:
                return (self.r == other[0] and
                        self.g == other[1] and
                        self.b == other[2])

    def __ne__(self, other):
        try:
            return (self.r != other.r or
                    self.g != other.g or
                    self.b != other.b or
                    self.a != other.a)
        except AttributeError:
            try:
                return (self.a != other[3] or
                        self.r != other[0] or
                        self.g != other[1] or
                        self.b != other[2])
            except IndexError:
                return (self.r != other[0] or
                        self.g != other[1] or
                        self.b != other[2])

