#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from java.awt import Color as _Color
from java.lang import IllegalArgumentException

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
        * integer argb
        * Color

        Color has the attributes::
        
            r, g, b, a

        Module initialization places pyj2d.Color in module's namespace.
        """
        ln = len(color)
        if ln == 1:
            _color = color[0]
            if hasattr(_color, '__len__'):
                ln = len(_color)
        else:
            _color = color
        if ln == 4:
            r = _color[0]
            g = _color[1]
            b = _color[2]
            a = _color[3]
        elif ln == 3:
            r = _color[0]
            g = _color[1]
            b = _color[2]
            a = 255
        else:
            if not hasattr(_color, 'startswith'):
                r = (_color>>16) & 0xff
                g = (_color>>8) & 0xff
                b = _color & 0xff
                a = (_color>>24) & 0xff
            else:
                _color = _color.lower()
                if _color.startswith('#'):
                    _color = _color.lstrip('#')
                elif _color.startswith('0x'):
                    _color = _color.lstrip('0x')
                if len(_color) == 6:
                    _color += 'ff'
                r = int(_color[0:2], 16)
                g = int(_color[2:4], 16)
                b = int(_color[4:6], 16)
                a = int(_color[6:8], 16)
        try:
            _Color.__init__(self, r, g, b, a)
        except IllegalArgumentException:
            raise ValueError('invalid color argument')

    def __str__(self):
        return "(%d, %d, %d, %d)" % (self.r, self.g, self.b, self.a)


    def __repr__(self):
        return "(%d, %d, %d, %d)" % (self.r, self.g, self.b, self.a)

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
        return self._dat['r']

    def _getGreen(self):
        return self._dat['g']

    def _getBlue(self):
        return self._dat['b']

    def _getAlpha(self):
        return self._dat['a']

    def _set_activate(self):
        self._dat = {'r': self.getRed(),
                     'g': self.getGreen(),
                     'b': self.getBlue(),
                     'a': self.getAlpha()}
        self.getRed = self._getRed
        self.getGreen = self._getGreen
        self.getBlue = self._getBlue
        self.getAlpha = self._getAlpha

    def __eq__(self, other):
        if hasattr(other, 'getAlpha'):
            return (self.getRed() == other.getRed() and
                    self.getGreen() == other.getGreen() and
                    self.getBlue() == other.getBlue() and
                    self.getAlpha() == other.getAlpha())
        else:
            if len(other) == 4:
                return (self.getAlpha() == other[3] and
                        self.getRed() == other[0] and
                        self.getGreen() == other[1] and
                        self.getBlue() == other[2])
            else:
                return (self.getRed() == other[0] and
                        self.getGreen() == other[1] and
                        self.getBlue() == other[2])

    def __ne__(self, other):
        if hasattr(other, 'getAlpha'):
            return (self.getRed() != other.getRed() or
                    self.getGreen() != other.getGreen() or
                    self.getBlue() != other.getBlue() or
                    self.getAlpha() != other.getAlpha())
        else:
            if len(other) == 4:
                return (self.getAlpha() != other[3] or
                        self.getRed() != other[0] or
                        self.getGreen() != other[1] or
                        self.getBlue() != other[2])
            else:
                return (self.getRed() != other[0] or
                        self.getGreen() != other[1] or
                        self.getBlue() != other[2])

    def __add__(self, other):
        r = self.getRed() + other.getRed()
        if r > 255: r = 255
        g = self.getGreen() + other.getGreen()
        if g > 255: g = 255
        b = self.getBlue() + other.getBlue()
        if b > 255: b = 255
        a = self.getAlpha() + other.getAlpha()
        if a > 255: a = 255
        return self.__class__(r,g,b,a)

    def __sub__(self, other):
        r = self.getRed() - other.getRed()
        if r < 0: r = 0
        g = self.getGreen() - other.getGreen()
        if g < 0: g = 0
        b = self.getBlue() - other.getBlue()
        if b < 0: b = 0
        a = self.getAlpha() - other.getAlpha()
        if a < 0: a = 0
        return self.__class__(r,g,b,a)

    def __mul__(self, other):
        r = self.getRed() * other.getRed()
        if r > 255: r = 255
        g = self.getGreen() * other.getGreen()
        if g > 255: g = 255
        b = self.getBlue() * other.getBlue()
        if b > 255: b = 255
        a = self.getAlpha() * other.getAlpha()
        if a > 255: a = 255
        return self.__class__(r,g,b,a)

    def __floordiv__(self, other):
        if other.getRed() != 0: r = int(self.getRed() // other.getRed())
        else: r = 0
        if other.getGreen() != 0: g = int(self.getGreen() // other.getGreen())
        else: g = 0
        if other.getBlue() != 0: b = int(self.getBlue() // other.getBlue())
        else: b = 0
        if other.getAlpha() != 0: a = int(self.getAlpha() // other.getAlpha())
        else: a = 0
        return self.__class__(r,g,b,a)

    def __mod__(self, other):
        if other.getRed() != 0: r = self.getRed() % other.getRed()
        else: r = 0
        if other.getGreen() != 0: g = self.getGreen() % other.getGreen()
        else: g = 0
        if other.getBlue() != 0: b = self.getBlue() % other.getBlue()
        else: b = 0
        if other.getAlpha() != 0: a = self.getAlpha() % other.getAlpha()
        else: a = 0
        return self.__class__(r,g,b,a)

    def __iadd__(self, other):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['r'] += other.getRed()
        if self._dat['r'] > 255: self._dat['r'] = 255
        self._dat['g'] += other.getGreen()
        if self._dat['g'] > 255: self._dat['g'] = 255
        self._dat['b'] += other.getBlue()
        if self._dat['b'] > 255: self._dat['b'] = 255
        self._dat['a'] += other.getAlpha()
        if self._dat['a'] > 255: self._dat['a'] = 255
        return self

    def __isub__(self, other):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['r'] -= other.getRed()
        if self._dat['r'] < 0: self._dat['r'] = 0
        self._dat['g'] -= other.getGreen()
        if self._dat['g'] < 0: self._dat['g'] = 0
        self._dat['b'] -= other.getBlue()
        if self._dat['b'] < 0: self._dat['b'] = 0
        self._dat['a'] -= other.getAlpha()
        if self._dat['a'] < 0: self._dat['a'] = 0
        return self

    def __imul__(self, other):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['r'] *= other.getRed()
        if self._dat['r'] > 255: self._dat['r'] = 255
        self._dat['g'] *= other.getGreen()
        if self._dat['g'] > 255: self._dat['g'] = 255
        self._dat['b'] *= other.getBlue()
        if self._dat['b'] > 255: self._dat['b'] = 255
        self._dat['a'] *= other.getAlpha()
        if self._dat['a'] > 255: self._dat['a'] = 255
        return self

    def __ifloordiv__(self, other):
        if not hasattr(self, '_dat'):
            self._set_activate()
        if other.getRed() != 0: self._dat['r'] //= other.getRed()
        else: self._dat['r'] = 0
        if other.getGreen() != 0: self._dat['g'] //= other.getGreen()
        else: self._dat['g'] = 0
        if other.getBlue() != 0: self._dat['b'] //= other.getBlue()
        else: self._dat['b'] = 0
        if other.getAlpha() != 0: self._dat['a'] //= other.getAlpha()
        else: self._dat['a'] = 0
        return self

    def __imod__(self, other):
        if not hasattr(self, '_dat'):
            self._set_activate()
        if other.getRed() != 0: self._dat['r'] %= other.getRed()
        else: self._dat['r'] = 0
        if other.getGreen() != 0: self._dat['g'] %= other.getGreen()
        else: self._dat['g'] = 0
        if other.getBlue() != 0: self._dat['b'] %= other.getBlue()
        else: self._dat['b'] = 0
        if other.getAlpha() != 0: self._dat['a'] %= other.getAlpha()
        else: self._dat['a'] = 0
        return self

    def __invert__(self):
        return self.__class__(~self.getRed() + 256,
                              ~self.getGreen() + 256,
                              ~self.getBlue() + 256,
                              ~self.getAlpha() + 256)

    def normalize(self):
        """
        Return normalized color values.
        """
        return (self.getRed() / 255.0,
                self.getGreen() / 255.0,
                self.getBlue() / 255.0,
                self.getAlpha() / 255.0)

    def correct_gamma(self, gamma):
        """
        Return gamma-corrected Color.
        """
        return self.__class__(int(round((((self.getRed()) / 255.0)**gamma) * 255.0)),
                              int(round((((self.getGreen()) / 255.0)**gamma) * 255.0)),
                              int(round((((self.getBlue()) / 255.0)**gamma) * 255.0)),
                              int(round((((self.getAlpha()) / 255.0)**gamma) * 255.0)))

    def premul_alpha(self):
        """
        Return alpha-multipled Color.
        """
        return self.__class__(int(round(self.getRed() * (self.a/255.0))),
                              int(round(self.getGreen() * (self.a/255.0))),
                              int(round(self.getBlue() * (self.a/255.0))),
                              self.a)

    def lerp(self, color, t):
        """
        Return a Color linear interpolated by t to the given color.
        """
        if t < 0.0 or t > 1.0:
            raise ValueError('Argument t must be in range 0 to 1')
        if hasattr(color, 'a'):
            return self.__class__(int(round(self.getRed() * (1-t) + color.getRed() * t)),
                                  int(round(self.getGreen() * (1-t) + color.getGreen() * t)),
                                  int(round(self.getBlue() * (1-t) + color.getBlue() * t)),
                                  int(round(self.getAlpha() * (1-t) + color.getAlpha() * t)))
        else:
            if len(color) == 3:
                return self.__class__(int(round(self.getRed() * (1-t) + color[0] * t)),
                                      int(round(self.getGreen() * (1-t) + color[1] * t)),
                                      int(round(self.getBlue() * (1-t) + color[2] * t)),
                                      int(round(self.getAlpha() * (1-t) + 255 * t)))
            elif len(color) == 4:
                return self.__class__(int(round(self.getRed() * (1-t) + color[0] * t)),
                                      int(round(self.getGreen() * (1-t) + color[1] * t)),
                                      int(round(self.getBlue() * (1-t) + color[2] * t)),
                                      int(round(self.getAlpha() * (1-t) + color[3] * t)))
            else:
                raise ValueError('invalid color argument')

    def update(self, *color):
        """
        Update color values.
        """
        if not hasattr(self, '_dat'):
            self._set_activate()
        ln = len(color)
        if ln == 1:
            _color = color[0]
            if hasattr(_color, '__len__'):
                ln = len(_color)
        else:
            _color = color
        if ln == 4:
            self._dat['r'] = _color[0]
            self._dat['g'] = _color[1]
            self._dat['b'] = _color[2]
            self._dat['a'] = _color[3]
        elif ln == 3:
            self._dat['r'] = _color[0]
            self._dat['g'] = _color[1]
            self._dat['b'] = _color[2]
            self._dat['a'] = 255
        else:
            if not hasattr(_color, 'startswith'):
                self._dat['r'] = (_color>>16) & 0xff
                self._dat['g'] = (_color>>8) & 0xff
                self._dat['b'] = _color & 0xff
                self._dat['a'] = (_color>>24) & 0xff
            else:
                _color = _color.lower()
                if _color.startswith('#'):
                    _color = _color.lstrip('#')
                elif _color.startswith('0x'):
                    _color = _color.lstrip('0x')
                if len(_color) == 6:
                    _color += 'ff'
                self._dat['r'] = int(_color[0:2], 16)
                self._dat['g'] = int(_color[2:4], 16)
                self._dat['b'] = int(_color[4:6], 16)
                self._dat['a'] = int(_color[6:8], 16)

    def _get_r(self):
        return self.getRed()

    def _get_g(self):
        return self.getGreen()

    def _get_b(self):
        return self.getBlue()

    def _get_a(self):
        return self.getAlpha()

    def _set_r(self, val):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['r'] = val

    def _set_g(self, val):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['g'] = val

    def _set_b(self, val):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['b'] = val

    def _set_a(self, val):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['a'] = val

    def _get_cmy(self):
        return _rgb_to_cmy(self.getRed(), self.getGreen(), self.getBlue())

    def _set_cmy(self, val):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['r'], self._dat['g'], self._dat['b'] = _cmy_to_rgb(*val)

    def _get_hsva(self):
        return _rgba_to_hsva(self.getRed(), self.getGreen(), self.getBlue(), self.getAlpha())

    def _set_hsva(self, val):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['r'], self._dat['g'], self._dat['b'], self._dat['a'] = _hsva_to_rgba(*val)

    def _get_hsla(self):
        return _rgba_to_hsla(self.getRed(), self.getGreen(), self.getBlue(), self.getAlpha())

    def _set_hsla(self, val):
        if not hasattr(self, '_dat'):
            self._set_activate()
        self._dat['r'], self._dat['g'], self._dat['b'], self._dat['a'] = _hsla_to_rgba(*val)

    r = property(_get_r, _set_r)
    "Red color value."

    g = property(_get_g, _set_g)
    "Green color value."

    b = property(_get_b, _set_b)
    "Blue color value."

    a = property(_get_a, _set_a)
    "Alpha color value."

    cmy = property(_get_cmy, _set_cmy)
    "CMY color."

    hsva = property(_get_hsva, _set_hsva)
    "HSVA color."

    hsla = property(_get_hsla, _set_hsla)
    "HSLA color."


def _rgb_to_cmy(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    c, m, y = 1-r, 1-g, 1-b
    return (c, m, y)


def _cmy_to_rgb(c, m, y):
    r, g, b = 1-c, 1-m, 1-y
    return (int(r*255), int(g*255), int(b*255))


def _rgba_to_hsva(r, g, b, a):
    r, g, b, a = r/255.0, g/255.0, b/255.0, a/255.0
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min
    if delta == 0:
        h = 0.0
    elif c_max == r:
        h = (60 * ((g - b) / delta) + 360) % 360.0
    elif c_max == g:
        h = (60 * ((b - r) / delta) + 120) % 360.0
    elif c_max == b:
        h = (60 * ((r - g) / delta) + 240) % 360.0
    if c_max == 0:
        s = 0.0
    else:
        s = (delta / c_max)
    v = c_max
    return h, s*100.0, v*100.0, a*100.0


def _hsva_to_rgba(h, s, v, a):
    h, s, v, a = h/360.0, s/100.0, v/100.0, a/100.0
    i = int(h*6.0)
    f = (h*6.0) - i
    p = (v * (1.0 - s))
    q = (v * (1.0 - s * f))
    t = (v * (1.0 - (s * (1.0-f))))
    i %= 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    elif i == 5:
        r, g, b = v, p, q
    return int(r*255), int(g*255), int(b*255), int(a*255)


def _rgba_to_hsla(r, g, b, a):
    r, g, b, a = r/255.0, g/255.0, b/255.0, a/255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin
    l = (cmax + cmin) / 2.0
    if delta == 0:
        s = 0.0
    else:
        s = delta / (1-abs(2*l-1))
    if delta == 0:
        h = 0.0
    elif cmax == r:
        h = (60 * ((g - b) / delta) + 360) % 360.0
    elif cmax == g:
        h = (60 * ((b - r) / delta) + 120) % 360.0
    elif cmax == b:
        h = (60 * ((r - g) / delta) + 240) % 360.0
    return h, s*100.0, l*100.0, a*100.0


def _hsla_to_rgba(h, s, l, a):
    h, s, l, a = h/360.0, s/100.0, l/100.0, a/100.0
    if l < 0.5:
        q = l * (1+s)
    else:
        q = l + s - l * s
    p = 2 * l - q
    t = h + 1.0/3.0
    if t < 0.0: t += 1.0
    elif t > 1.0: t -= 1.0
    if t < 1.0/6.0:
        r = p + (q - p) * 6.0 * t
    elif t < 1.0/2.0:
        r = q
    elif t < 2.0/3.0:
        r = p + (q - p) * (2.0/3.0-t) * 6.0
    else:
        r = p
    t = h
    if t < 0.0: t += 1.0
    elif t > 1.0: t -= 1.0
    if t < 1.0/6.0:
        g = p + (q - p) * 6.0 * t
    elif t < 1.0/2.0:
        g = q
    elif t < 2.0/3.0:
        g = p + (q - p) * (2.0/3.0-t) * 6.0
    else:
        g = p
    t = h - 1.0/3.0
    if t < 0.0: t += 1.0
    elif t > 1.0: t -= 1.0
    if t < 1.0/6.0:
        b = p + (q - p) * 6.0 * t
    elif t < 1.0/2.0:
        b = q
    elif t < 2.0/3.0:
        b = p + (q - p) * (2.0/3.0-t) * 6.0
    else:
        b = p
    return int(r*255), int(g*255), int(b*255), int(a*255)

