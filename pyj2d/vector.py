#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from __future__ import generators
from math import sqrt, sin, cos, atan2, pi


class Vector2(object):
    """
    Vector2 - 2-dimensional vector.
    """

    __slots__ = ['_x', '_y']

    def __init__(self, x=None, y=None):
        if y is not None:
            self._x = float(x)
            self._y = float(y)
        elif x is not None:
            self._x = float(x[0])
            self._y = float(x[1])
        else:
            self._x = 0.0
            self._y = 0.0

    def _get_x(self):
        return self._x

    def _set_x(self, val):
        try:
            self._x = float(val)
        except ValueError:
            raise TypeError('float is required')

    def _del_x(self):
        raise TypeError('Cannot delete the x attribute')

    def _get_y(self):
        return self._y

    def _set_y(self, val):
        try:
            self._y = float(val)
        except ValueError:
            raise TypeError('float is required')

    def _del_y(self):
        raise TypeError('Cannot delete the y attribute')

    x = property(_get_x, _set_x, _del_x)
    y = property(_get_y, _set_y, _del_y)

    def __str__(self):
        return '[%g, %g]' % (self._x, self._y)

    def __repr__(self):
        return '<%s(%g, %g)>' % (self.__class__.__name__, self._x, self._y)

    def __getitem__(self, index):
        if index in (0, -2):
            return self._x
        elif index in (1, -1):
            return self._y
        elif isinstance(index, slice):
            return [self._x, self._y][index]
        else:
            raise IndexError

    def __setitem__(self, index, val):
        if index == 0:
            try:
                self._x = float(val)
            except ValueError:
                raise TypeError
        elif index == 1:
            try:
                self._y = float(val)
            except ValueError:
                raise TypeError
        elif isinstance(index, slice):
            l = [self._x, self._y]
            l[index] = val
            if len(l) != 2:
                raise ValueError
            self._x = float(l[0])
            self._y = float(l[1])
        else:
            raise IndexError

    def __delitem__(self, index):
        raise TypeError(
            'Deletion of vector components is not supported')

    def __getslice__(self, start, stop):
        return [self._x, self._y][start:stop]

    def __setslice__(self, lower, upper, val):
        l = [self._x, self._y]
        l[lower:upper] = val
        if len(l) != 2:
            raise ValueError
        self._x = float(l[0])
        self._y = float(l[1])

    def __iter__(self):
        for val in (self._x, self._y):
            yield val

    def __len__(self):
        return 2

    def __bool__(self):
        return bool(self._x or self._y)

    def __nonzero__(self):
        return bool(self._x or self._y)

    def dot(self, vector):
        """
        Return dot product with other vector.
        """
        return (self._x * vector[0]) + (self._y * vector[1])

    def cross(self, vector):
        """
        Return cross product with other vector.
        """
        return (self._x * vector[1]) - (self._y * vector[0])

    def magnitude(self):
        """
        Return magnitude of vector.
        """
        return sqrt((self._x**2) + (self._y**2))

    def magnitude_squared(self):
        """
        Return squared magnitude of vector.
        """
        return ((self._x**2) + (self._y**2))

    def length(self):
        """
        Return length of vector.
        """
        return sqrt((self._x**2) + (self._y**2))

    def length_squared(self):
        """
        Return squared length of vector.
        """
        return ((self._x**2) + (self._y**2))

    def normalize(self):
        """
        Return normalized vector.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError('Cannot normalize vector of zero length')
        return self.__class__(self._x / mag, self._y / mag)

    def normalize_ip(self):
        """
        Normalized this vector.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError('Cannot normalize vector of zero length')
        self._x /= mag
        self._y /= mag
        return None

    def is_normalized(self):
        """
        Check whether vector is normalized.
        """
        return self.magnitude() == 1

    def scale_to_length(self, length):
        """
        Scale vector to length.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError('Cannot scale vector of zero length')
        self._x = (self._x / mag) * length
        self._y = (self._y / mag) * length
        return None

    def reflect(self, vector):
        """
        Return reflected vector at given vector.
        """
        vn = (self._x * vector[0]) + (self._y * vector[1])
        nn = (vector[0] * vector[0]) + (vector[1] * vector[1])
        if nn == 0:
            raise ValueError('Cannot reflect from normal of zero length')
        c = 2 * vn / nn
        return self.__class__(self._x - (vector[0] * c),
                              self._y - (vector[1] * c))

    def reflect_ip(self, vector):
        """
        Derive reflected vector at given vector in place.
        """
        vn = (self._x * vector[0]) + (self._y * vector[1])
        nn = (vector[0] * vector[0]) + (vector[1] * vector[1])
        if nn == 0:
            raise ValueError('Cannot reflect from normal of zero length')
        c = 2 * vn / nn
        self._x -= (vector[0] * c)
        self._y -= (vector[1] * c)
        return None

    def distance_to(self, vector):
        """
        Return distance to given vector.
        """
        return sqrt((self._x - vector[0])**2
                  + (self._y - vector[1])**2)

    def distance_squared_to(self, vector):
        """
        Return squared distance to given vector.
        """
        return ((self._x - vector[0])**2
              + (self._y - vector[1])**2)

    def lerp(self, vector, t):
        """
        Return vector linear interpolated by t to the given vector.
        """
        if t < 0.0 or t > 1.0:
            raise ValueError('Argument t must be in range 0 to 1')
        return self.__class__(self._x * (1-t) + vector[0] * t,
                              self._y * (1-t) + vector[1] * t)

    def slerp(self, vector, t):
        """
        Return vector spherical interpolated by t to the given vector.
        """
        if t < -1.0 or t > 1.0:
            raise ValueError('Argument t must be in range -1 to 1')
        if not hasattr(vector, '__len__') or len(vector) != 2:
            raise TypeError('The first argument must be a vector')
        smag = sqrt((self._x**2) + (self._y**2))
        vmag = sqrt((vector[0]**2) + (vector[1]**2))
        if smag==0 or vmag==0:
            raise ValueError('Cannot use slerp with zero-vector')
        sx = self._x / smag
        sy = self._y / smag
        vx = vector[0] / vmag
        vy = vector[1] / vmag
        theta = atan2(vy, vx) - atan2(sy, sx)
        _theta = abs(theta)
        if _theta-pi > 0.000001:
            theta -= (2*pi) * (theta / _theta)
        elif -0.000001 < _theta-pi < 0.000001:
            raise ValueError('Cannot use slerp on 180 degrees')
        if t < 0.0:
            t = -t
            theta -= (2*pi) * (theta / abs(theta))
        sin_theta = sin(theta)
        if sin_theta:
            a = sin((1.0-t) * theta) / sin_theta
            b = sin(t * theta) / sin_theta
        else:
            a = 1.0
            b = 0.0
        v = self.__class__((sx * a) + (vx * b),
                           (sy * a) + (vy * b))
        smag = ((1.0-t) * smag) + (t * vmag)
        v.x *= smag
        v.y *= smag
        return v

    def elementwise(self):
        """
        Elementwice operation.
        """
        return VectorElementwiseProxy(self)

    def rotate(self, angle):
        """
        Return vector rotated by angle in degrees.
        """
        rad = angle / 180.0 * pi
        c = round(cos(rad), 6)
        s = round(sin(rad), 6)
        return self.__class__((c * self._x) - (s * self._y),
                              (s * self._x) + (c * self._y))

    def rotate_rad(self, angle):
        """
        Return vector rotated by angle in radians.
        """
        c = cos(angle)
        s = sin(angle)
        return self.__class__((c * self._x) - (s * self._y),
                              (s * self._x) + (c * self._y))

    def rotate_ip(self, angle):
        """
        Rotate vector by angle in degrees.
        """
        r = angle / 180.0 * pi
        c = round(cos(r), 6)
        s = round(sin(r), 6)
        x = self._x
        y = self._y
        self._x = (c * x) - (s * y)
        self._y = (s * x) + (c * y)
        return None

    def rotate_ip_rad(self, angle):
        """
        Rotate vector by angle in radians.
        """
        c = cos(angle)
        s = sin(angle)
        x = self._x
        y = self._y
        self._x = (c * x) - (s * y)
        self._y = (s * x) + (c * y)
        return None

    def angle_to(self, vector):
        """
        Return angle to given vector.
        """
        return (atan2(vector[1], vector[0])
                - atan2(self._y, self._x)) * (180.0 / pi)

    def as_polar(self):
        """
        Return radial distance and azimuthal angle.
        """
        r = self.magnitude()
        phi = atan2(self._y, self._x) * (180.0 / pi)
        return (r, phi)

    def from_polar(self, coordinate):
        """
        Set vector with polar coordinate tuple.
        """
        if len(coordinate) != 2:
            raise TypeError('coodinate must be of length 2')
        r = coordinate[0]
        phi = coordinate[1] * (pi / 180.0)
        self._x = round(r * cos(phi), 6)
        self._y = round(r * sin(phi), 6)
        return None

    def copy(self):
        """
        Return copy of vector.
        """
        return self.__class__(self._x, self._y)

    def update(self, x=None, y=None):
        """
        Update vector.
        """
        if y is not None:
            self._x = float(x)
            self._y = float(y)
        elif x is not None:
            self._x = float(x[0])
            self._y = float(x[1])
        else:
            self._x = 0.0
            self._y = 0.0

    def __pos__(self):
        return self.__class__(self._x, self._y)

    def __neg__(self):
        return self.__class__(-self._x, -self._y)

    def __add__(self, other):
        if hasattr(other, '__len__'):
            return self.__class__(self._x + other[0], self._y + other[1])
        else:
            raise TypeError('unsupported operand')

    def __sub__(self, other):
        if hasattr(other, '__len__'):
            return self.__class__(self._x - other[0], self._y - other[1])
        else:
            raise TypeError('unsupported operand')

    def __mul__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                return (self._x * other[0]) + (self._y * other[1])
            else:
                return self.__class__(self._x * other[0], self._y * other[1])
        else:
            return self.__class__(self._x * other, self._y * other)

    def __div__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                raise TypeError('unsupported operand')
            else:
                return self.__class__(self._x / other[0], self._y / other[1])
        else:
            return self.__class__(self._x / other, self._y / other)

    def __truediv__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                raise TypeError('unsupported operand')
            else:
                return self.__class__(self._x / other[0], self._y / other[1])
        else:
            return self.__class__(self._x / other, self._y / other)

    def __floordiv__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                raise TypeError('unsupported operand')
            else:
                return self.__class__(self._x // other[0], self._y // other[1])
        else:
            return self.__class__(self._x // other, self._y // other)

    def __eq__(self, other):
        if hasattr(other, '__len__'):
            return ( abs(self._x - other[0]) < 0.000001 and
                     abs(self._y - other[1]) < 0.000001 )
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, '__len__'):
            return ( abs(self._x - other[0]) > 0.000001 or
                     abs(self._y - other[1]) > 0.000001 )
        else:
            return True

    def __gt__(self, other):
        if not hasattr(other, '_v'):
            raise TypeError('operation not supported')
        return NotImplemented

    def __ge__(self, other):
        if not hasattr(other, '_v'):
            raise TypeError('operation not supported')
        return NotImplemented

    def __lt__(self, other):
        if not hasattr(other, '_v'):
            raise TypeError('operation not supported')
        return NotImplemented

    def __le__(self, other):
        if not hasattr(other, '_v'):
            raise TypeError('operation not supported')
        return NotImplemented

    def __radd__(self, other):
        if hasattr(other, '__len__'):
            return self.__class__(self._x + other[0], self._y + other[1])
        else:
            raise TypeError('unsupported operand')

    def __rsub__(self, other):
        if hasattr(other, '__len__'):
            return self.__class__(other[0] - self._x, other[1] - self._y)
        else:
            raise TypeError('unsupported operand')

    def __rmul__(self, other):
        if hasattr(other, '__len__'):
            return (self._x * other[0]) + (self._y * other[1])
        else:
            return self.__class__(self._x * other, self._y * other)

    def __rdiv__(self, other):
        if not hasattr(other, '_v'):
            raise TypeError('unsupported operand')
        else:
            return self.__class__(other[0] / self._x, other[1] / self._y)

    def __rtruediv__(self, other):
        if not hasattr(other, '_v'):
            raise TypeError('unsupported operand')
        else:
            return self.__class__(other[0] / self._x, other[1] / self._y)

    def __rfloordiv__(self, other):
        if not hasattr(other, '_v'):
            raise TypeError('unsupported operand')
        else:
            return self.__class__(other[0] // self._x, other[1] // self._y)

    def __iadd__(self, other):
        if hasattr(other, '__len__'):
            self._x += other[0]
            self._y += other[1]
        else:
            raise TypeError('unsupported operand')
        return self

    def __isub__(self, other):
        if hasattr(other, '__len__'):
            self._x -= other[0]
            self._y -= other[1]
        else:
            raise TypeError('unsupported operand')
        return self

    def __imul__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                return (self._x * other[0]) + (self._y * other[1])
            else:
                self._x *= other[0]
                self._y *= other[1]
        else:
            self._x *= other
            self._y *= other
        return self

    def __idiv__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                raise TypeError('unsupported operand')
            else:
                self._x /= other[0]
                self._y /= other[1]
        else:
            self._x /= other
            self._y /= other
        return self

    def __itruediv__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                raise TypeError('unsupported operand')
            else:
                self._x /= other[0]
                self._y /= other[1]
        else:
            self._x /= other
            self._y /= other
        return self

    def __ifloordiv__(self, other):
        if hasattr(other, '__len__'):
            if not hasattr(other, '_v'):
                raise TypeError('unsupported operand')
            else:
                self._x //= other[0]
                self._y //= other[1]
        else:
            self._x //= other
            self._y //= other
        return self


class VectorElementwiseProxy(object):

    def __init__(self, vector):
        self._v = vector

    def __getitem__(self, index):
        if index in (0, -2):
            return self._v._x
        elif index in (1, -1):
            return self._v._y

    def __iter__(self):
        for val in (self._v._x, self._v._y):
            yield val

    def __len__(self):
        return 2

    def __bool__(self):
        return bool(self._v._x or self._v._y)

    def __nonzero__(self):
        return bool(self._v._x or self._v._y)

    def __pos__(self):
        return self._v.__class__(self._v._x, self._v._y)

    def __neg__(self):
        return self._v.__class__(-self._v._x, -self._v._y)

    def __abs__(self):
        return (abs(self._v._x), abs(self._v._y))

    def __add__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x + other[0], self._v._y + other[1])
        else:
            return self._v.__class__(self._v._x + other, self._v._y + other)

    def __sub__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x - other[0], self._v._y - other[1])
        else:
            return self._v.__class__(self._v._x - other, self._v._y - other)

    def __mul__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x * other[0], self._v._y * other[1])
        else:
            return self._v.__class__(self._v._x * other, self._v._y * other)

    def __div__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x / other[0], self._v._y / other[1])
        else:
            return self._v.__class__(self._v._x / other, self._v._y / other)

    def __truediv__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x / other[0], self._v._y / other[1])
        else:
            return self._v.__class__(self._v._x / other, self._v._y / other)

    def __floordiv__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x // other[0], self._v._y // other[1])
        else:
            return self._v.__class__(self._v._x // other, self._v._y // other)

    def __pow__(self, other):
        if hasattr(other, '__len__'):
            if (other[0]%1 and self._v._x<0) or (other[1]%1 and self._v._y<0):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return self._v.__class__(self._v._x ** other[0], self._v._y ** other[1])
        else:
            if other%1 and (self._v._x<0 or self._v._y<0):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return self._v.__class__(self._v._x ** other, self._v._y ** other)

    def __mod__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x % other[0], self._v._y % other[1])
        else:
            return self._v.__class__(self._v._x % other, self._v._y % other)

    def __eq__(self, other):
        if hasattr(other, '__len__'):
            return ( abs(self._v._x - other[0]) < 0.000001 and
                     abs(self._v._y - other[1]) < 0.000001 )
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, '__len__'):
            return ( abs(self._v._x - other[0]) > 0.000001 or
                     abs(self._v._y - other[1]) > 0.000001 )
        else:
            return True

    def __gt__(self, other):
        if hasattr(other, '__len__'):
            return bool(self._v._x > other[0] and self._v._y > other[1])
        else:
            return bool(self._v._x > other and self._v._y > other)

    def __ge__(self, other):
        if hasattr(other, '__len__'):
            return bool(self._v._x >= other[0] and self._v._y >= other[1])
        else:
            return bool(self._v._x >= other and self._v._y >= other)

    def __lt__(self, other):
        if hasattr(other, '__len__'):
            return bool(self._v._x < other[0] and self._v._y < other[1])
        else:
            return bool(self._v._x < other and self._v._y < other)

    def __le__(self, other):
        if hasattr(other, '__len__'):
            return bool(self._v._x <= other[0] and self._v._y <= other[1])
        else:
            return bool(self._v._x <= other and self._v._y <= other)

    def __radd__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x + other[0], self._v._y + other[1])
        else:
            return self._v.__class__(self._v._x + other, self._v._y + other)

    def __rsub__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(other[0] - self._v._x, other[1] - self._v._y)
        else:
            return self._v.__class__(other - self._v._x, other - self._v._y)

    def __rmul__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(self._v._x * other[0], self._v._y * other[1])
        else:
            return self._v.__class__(self._v._x * other, self._v._y * other)

    def __rdiv__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(other[0] / self._v._x, other[1] / self._v._y)
        else:
            return self._v.__class__(other / self._v._x, other / self._v._y)

    def __rtruediv__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(other[0] / self._v._x, other[1] / self._v._y)
        else:
            return self._v.__class__(other / self._v._x, other / self._v._y)

    def __rfloordiv__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(other[0] // self._v._x, other[1] // self._v._y)
        else:
            return self._v.__class__(other // self._v._x, other // self._v._y)

    def __rpow__(self, other):
        if hasattr(other, '__len__'):
            if (other[0]<0 and self._v._x%1) or (other[1]<0 and self._v._y%1):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return self._v.__class__(other[0] ** self._v._x, other[1] ** self._v._y)
        else:
            if other<0 and (self._v._x%1 or self._v._y%1):
                raise ValueError(
                    'negative number cannot be raised to a fractional power')
            return self._v.__class__(other ** self._v._x, other ** self._v._y)

    def __rmod__(self, other):
        if hasattr(other, '__len__'):
            return self._v.__class__(other[0] % self._v._x, other[1] % self._v._y)
        else:
            return self._v.__class__(other % self._v._x, other % self._v._y)

