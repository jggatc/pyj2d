#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Rect module**

The module provides rect object to store coordinates.
"""

from java.awt import Rectangle
from java.util.concurrent import ConcurrentLinkedQueue


class Rect(Rectangle):
    """
    Rect object.
    """

    def __init__(self, *arg):
        """
        Initialize Rect object.

        Return Rect that is subclassed from java.awt.Rectangle.
        
        Alternative arguments::
        
        * x, y, width, height
        * (x, y), (width, height)
        * (x, y, width, height)
        * Rect
        * Obj with rect attribute

        Rect has the attributes::
        
        x, y, width, height
        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, w, h
        
        Module initialization places Rect in module's namespace.
        """
        def unpack(arg, lst=[]):
            for x in arg:
                if not isinstance(x, tuple):
                    lst.append(x)
                else:
                    lst = unpack(x, lst)
            return lst
        try:
            x = arg[0]
            y = arg[1]
            w = arg[2]
            h = arg[3]
        except IndexError:
            try:
                x = arg[0][0]
                y = arg[0][1]
                w = arg[0][2]
                h = arg[0][3]
            except (IndexError, TypeError, AttributeError):
                arg = unpack(arg)
                try:
                    x = arg[0]
                    y = arg[1]
                    w = arg[2]
                    h = arg[3]
                except IndexError:
                    if hasattr(arg[0], 'rect'):
                        arg[0] = arg[0].rect
                    x = arg[0].x
                    y = arg[0].y
                    w = arg[0].width
                    h = arg[0].height
        try:
            Rectangle.__init__(self, x, y, w, h)
        except TypeError:
            Rectangle.__init__(self, int(x), int(y), int(w), int(h))

    def __str__(self):
        return "<rect(%d, %d, %d, %d)>" % (self.x,
                                           self.y,
                                           self.width,
                                           self.height)

    def __repr__(self):
        return "%s(%s)" % (self.__class__, self.toString())

    def setLocation(self, x, y):
        try:
            Rectangle.move(self, x, y)
        except TypeError:
            Rectangle.move(self, int(x), int(y))
        return None

    def setSize(self, width, height):
        try:
            Rectangle.setSize(self, width, height)
        except TypeError:
            Rectangle.setSize(self, int(width), int(height))
        return None

    def __setattr__(self, attr, val):
        try:
            getattr(self, '_set_'+attr)(val)
        except AttributeError:
            msg = 'Rect object has no attribute %s' % attr
            raise AttributeError(msg)

    def __getitem__(self, key):
        return getattr(self, ('x','y','width','height')[key])

    def __setitem__(self, key, val):
        setattr(self, ('x','y','width','height')[key], val)

    def __iter__(self):
        return iter([self.x, self.y, self.width, self.height])

    def __len__(self):
        return 4

    def __bool__(self):
        return self.width and self.height

    def __nonzero__(self):
        return self.width and self.height

    def __eq__(self, other):
        try:
            return ( self.x == other.x and
                     self.y == other.y and
                     self.width == other.width and
                     self.height == other.height )
        except AttributeError:
            return ( self.x == other[0] and
                     self.y == other[1] and
                     self.width == other[2] and
                     self.height == other[3] )

    def __ne__(self, other):
        try:
            return ( self.x != other.x or
                     self.y != other.y or
                     self.width != other.width or
                     self.height != other.height )
        except AttributeError:
            return ( self.x != other[0] or
                     self.y != other[1] or
                     self.width != other[2] or
                     self.height != other[3] )

    def copy(self):
        """
        Returns Rect that is a copy of this rect.
        """
        return Rect(self.x, self.y, self.width, self.height)

    def move(self, *offset):
        """
        Return Rect of same dimension at position offset by x,y.
        """
        try:
            x, y = offset
        except ValueError:
            x, y = offset[0]
        return Rect(self.x+x, self.y+y, self.width, self.height)

    def move_ip(self, *offset):
        """
        Moves this rect to position offset by x,y.
        """
        try:
            x, y = offset
        except ValueError:
            x, y = offset[0]
        self.setLocation(self.x+x, self.y+y)
        return None

    def inflate(self, *offset):
        """
        Return Rect at same position but size offset by x,y.
        """
        try:
            x, y = offset
        except ValueError:
            x, y = offset[0]
        return Rect(self.x-x//2, self.y-y//2, self.width+x, self.height+y)

    def inflate_ip(self, *offset):
        """
        Change size of this rect offset by x,y.
        """
        try:
            x, y = offset
        except ValueError:
            x, y = offset[0]
        self.setSize(self.width+x, self.height+y)
        self.setLocation(self.x-x//2, self.y-y//2)
        return None

    def clip(self, rect):
        """
        Return Rect representing this rect clipped by rect.
        """
        clipRect = self.intersection(rect)
        if clipRect.width > 0 and clipRect.height > 0:
            return Rect(clipRect.x, clipRect.y, clipRect.width, clipRect.height)
        else:
            return Rect(0,0,0,0)

    def union(self, rect):
        """
        Return Rect representing the union of rect and this rect.
        """
        r = Rectangle.union(self, rect)
        return Rect(r.x, r.y, r.width, r.height)

    def union_ip(self, rect):
        """
        Change this rect to represent the union of rect and this rect.
        """
        r = Rectangle.union(self, rect)
        self.setLocation(r.x, r.y)
        self.setSize(r.width, r.height)
        return None

    def unionall(self, rect_list):
        """
        Return Rect representing the union of rect list and this rect.
        """
        r = self
        for rect in rect_list:
            r = Rectangle.union(r, rect)
        return Rect(r.x, r.y, r.width, r.height)

    def unionall_ip(self, rect_list):
        """
        Change this rect to represent the union of rect list and this rect.
        """
        r = self
        for rect in rect_list:
            r = Rectangle.union(r, rect)
        self.setLocation(r.x, r.y)
        self.setSize(r.width, r.height)
        return None

    def clamp(self, rect):
        """
        Return Rect of same dimension as this rect moved within rect.
        """
        if rect.contains(self):
            return Rect(self.x, self.y, self.width, self.height)
        x, y = self._clamp(rect)
        return Rect(x, y, self.width, self.height)

    def clamp_ip(self, rect):
        """
        Move this rect within rect.
        """
        if rect.contains(self):
            return None
        x, y = self._clamp(rect)
        self.setLocation(x, y)
        return None

    def _clamp(self, rect):
        if self.width < rect.width:
            if self.x < rect.x:
                x = rect.x
            elif self.x + self.width > rect.x + rect.width:
                x = rect.x + rect.width - self.width
            else:
                x = self.x
        else:
            x = rect.x - (self.width - rect.width) // 2
        if self.height < rect.height:
            if self.y < rect.y:
                y = rect.y
            elif self.y + self.height > rect.y + rect.height:
                y = rect.y + rect.height - self.height
            else:
                y = self.y
        else:
            y = rect.y - (self.height - rect.height) // 2
        return x, y

    def collidepoint(self, *point):
        """
        Return True if point is in this rect.
        """
        try:
            x, y = point[0], point[1]
        except IndexError:
            x, y = point[0]
        return self.contains(x,y)

    def colliderect(self, rect):
        """
        Return True if rect collides with this rect.
        """
        return self.intersects(rect)

    def collidelist(self, rects):
        """
        Return index of rect in list that collide with this rect, otherwise returns -1.
        """
        for i, rect in enumerate(rects):
            if self.intersects(rect):
                return i
        return -1

    def collidelistall(self, rects):
        """
        Return list of indices of rects list that collide with this rect.
        """
        collided = []
        for i, rect in enumerate(rects):
            if self.colliderect(rect):
                collided.append(i)
        return collided

    def collidedict(self, rects):
        """
        Return (key,value) of first rect from rects dict that collide with this rect, otherwise returns None.
        """
        for rect in rects:
            if self.colliderect(rects[rect]):
                return (rect,rects[rect])
        return None

    def collidedictall(self, rects):
        """
        Return list of (key,value) from rects dict that collide with this rect.
        """
        collided = []
        for rect in rects:
            if self.colliderect(rects[rect]):
                collided.append((rect,rects[rect]))
        return collided

    def _get_center(self):
        return (self.x + (self.width//2), self.y + (self.height//2))

    def _get_centerx(self):
        return self.x + (self.width//2)

    def _get_centery(self):
        return self.y + (self.height//2)

    def _get_top(self):
        return self.y

    def _get_left(self):
        return self.x

    def _get_bottom(self):
        return self.y + self.height

    def _get_right(self):
        return self.x + self.width

    def _get_topleft(self):
        return (self.x, self.y)

    def _get_bottomleft(self):
        return (self.x, self.y + self.height)

    def _get_topright(self):
        return (self.x + self.width, self.y)

    def _get_bottomright(self):
        return (self.x + self.width, self.y + self.height)

    def _get_midtop(self):
        return (self.x + (self.width//2), self.y)

    def _get_midleft(self):
        return (self.x, self.y + (self.height//2))

    def _get_midbottom(self):
        return (self.x + (self.width//2), self.y + self.height)

    def _get_midright(self):
        return (self.x + self.width, self.y + (self.height//2))

    def _get_size(self):
        return (self.width, self.height)

    def _get_w(self):
        return self.width

    def _get_h(self):
        return self.height

    def _set_x(self, val):
        self.setLocation(val, self.y)

    def _set_y(self, val):
        self.setLocation(self.x, val)

    def _set_width(self, val):
        self.setSize(val, self.height)

    def _set_height(self, val):
        self.setSize(self.width, val)

    def _set_center(self, val):
        self.setLocation(val[0] - (self.width//2), val[1] - (self.height//2))

    def _set_centerx(self, val):
        self.setLocation(val - (self.width//2), self.y)

    def _set_centery(self, val):
        self.setLocation(self.x, val - (self.height//2))

    def _set_top(self, val):
        self.setLocation(self.x, val)

    def _set_left(self, val):
        self.setLocation(val, self.y)

    def _set_bottom(self, val):
        self.setLocation(self.x, val - self.height)

    def _set_right(self, val):
        self.setLocation(val - self.width, self.y)

    def _set_topleft(self, val):
        self.setLocation(val[0], val[1])

    def _set_bottomleft(self, val):
        self.setLocation(val[0], val[1] - self.height)

    def _set_topright(self, val):
        self.setLocation(val[0] - self.width, val[1])

    def _set_bottomright(self, val):
        self.setLocation(val[0] - self.width, val[1] - self.height)

    def _set_midtop(self, val):
        self.setLocation(val[0] - (self.width//2), val[1])

    def _set_midleft(self, val):
        self.setLocation(val[0], val[1] - (self.height//2))

    def _set_midbottom(self, val):
        self.setLocation(val[0] - (self.width//2), val[1] - self.height)

    def _set_midright(self, val):
        self.setLocation(val[0] - self.width, val[1] - (self.height//2))

    def _set_size(self, val):
        self.setSize(val[0], val[1])

    def _set_w(self, val):
        self.setSize(val, self.height)

    def _set_h(self, val):
        self.setSize(self.width, val)

    size = property(_get_size, _set_size)
    center = property(_get_center, _set_center)
    centerx = property(_get_centerx, _set_centerx)
    centery = property(_get_centery, _set_centery)
    top = property(_get_top, _set_top)
    left = property(_get_left, _set_left)
    bottom = property(_get_bottom, _set_bottom)
    right = property(_get_right, _set_right)
    topleft = property(_get_topleft, _set_topleft)
    bottomleft = property(_get_bottomleft, _set_bottomleft)
    topright = property(_get_topright, _set_topright)
    bottomright = property(_get_bottomright, _set_bottomright)
    midtop = property(_get_midtop, _set_midtop)
    midleft = property(_get_midleft, _set_midleft)
    midbottom = property(_get_midbottom, _set_midbottom)
    midright = property(_get_midright, _set_midright)
    w = property(_get_w, _set_w)
    h = property(_get_h, _set_h)


class RectPool(ConcurrentLinkedQueue):
    """
    RectPool object.
    """

    def __init__(self):
        """
        Initialize RectPool object.

        Rect pool accessed by rectPool instance through append method to add Rect, extend method to add Rect list, get method to return Rect set with x,y,width,height attributes, and copy method to return copy of a given Rect. If pool is empty, return is a new Rect.
        """
        self.append = self.add
        self.extend = self.addAll

    def get(self, x, y, width, height):
        """
        Return a Rect with x,y,width,height attributes.
        """
        rect = self.poll()
        if rect is not None:
            rect.x = x
            rect.y = y
            rect.width = width
            rect.height = height
            return rect
        else:
            return Rect(x, y, width, height)

    def copy(self, r):
        """
        Return a Rect with x,y,width,height attributes of the Rect argument.
        """
        rect = self.poll()
        if rect is not None:
            rect.x = r.x
            rect.y = r.y
            rect.width = r.width
            rect.height = r.height
            return rect
        else:
            return Rect(r.x, r.y, r.width, r.height)


rectPool = RectPool()
"Module RectPool instance."

