#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from java.awt import Rectangle

__docformat__ = 'restructuredtext'


class Rect(Rectangle):
    """
    **pyj2d.Rect**
    
    * Rect.copy
    * Rect.movex
    * Rect.move_ip
    * Rect.inflate
    * Rect.inflate_ip
    * Rect.unionx
    * Rect.union_ip
    * Rect.unionall
    * Rect.unionall_ip
    * Rect.clip
    * Rect.collidepoint
    * Rect.colliderect
    * Rect.collidelist
    """

    _xy = {
        'center': lambda self,val: self.setLocation( val[0]-(self.width//2), val[1]-(self.height//2) ),
        'centerx': lambda self,val: self.setLocation( val-(self.width//2), self.y ),
        'centery': lambda self,val: self.setLocation( self.x, val-(self.height//2) ),
        'top': lambda self,val: self.setLocation( self.x, val ),
        'left': lambda self,val: self.setLocation( val, self.y ),
        'bottom': lambda self,val: self.setLocation( self.x, val-self.height ),
        'right': lambda self,val: self.setLocation( val-self.width, self.y ),
        'topleft': lambda self,val: self.setLocation( val[0], val[1] ),
        'bottomleft': lambda self,val: self.setLocation( val[0], val[1]-self.height ),
        'topright': lambda self,val: self.setLocation( val[0]-self.width, val[1] ),
        'bottomright': lambda self,val: self.setLocation( val[0]-self.width, val[1]-self.height ),
        'midtop': lambda self,val: self.setLocation( val[0]-(self.width//2), val[1] ),
        'midleft': lambda self,val: self.setLocation( val[0], val[1]-(self.height//2) ),
        'midbottom': lambda self,val: self.setLocation( val[0]-(self.width//2), val[1]-self.height ),
        'midright': lambda self,val: self.setLocation( val[0]-self.width, val[1]-(self.height//2) ),
        'size': lambda self,val: self.setSize( val[0], val[1] ),
        'width': lambda self,val: self.setSize( val, self.height ),
        'height':lambda self,val: self.setSize( self.width, val ),
        'w': lambda self,val: self.setSize( val, self.height ),
        'h': lambda self,val: self.setSize( self.width, val ),
        'x': lambda self,val: self.setLocation( val, self.y ),
        'y': lambda self,val: self.setLocation( self.x, val )
          }
    _at = {
        'center': lambda self: (self.x+(self.width//2), self.y+(self.height//2)),
        'centerx': lambda self: self.x+(self.width//2),
        'centery': lambda self: self.y+(self.height//2),
        'top': lambda self: self.y,
        'left': lambda self: self.x,
        'bottom': lambda self: self.y+self.height,
        'right': lambda self: self.x+self.width,
        'topleft': lambda self: (self.x, self.y),
        'bottomleft': lambda self: (self.x, self.y+self.height),
        'topright': lambda self: (self.x+self.width, self.y),
        'bottomright': lambda self: (self.x+self.width, self.y+self.height),
        'midtop': lambda self: (self.x+(self.width//2), self.y),
        'midleft': lambda self: (self.x, self.y+(self.height//2)),
        'midbottom': lambda self: (self.x+(self.width//2), self.y+self.height),
        'midright': lambda self: (self.x+self.width, self.y+(self.height//2)),
        'w': lambda self: self.width,
        'h': lambda self: self.height
          }

    def __init__(self, *arg):
        """
        Return Rect that is subclassed from java.awt.Rectangle.
        
        Alternative arguments:
        
        * x,y,w,h
        * (x,y),(w,h)
        * (x,y,w,h)
        * Rect
        * Obj with rect attribute

        Rect has the attributes::
        
            x, y, width, height
        
        Additional Rect attributes::
        
            top, left, bottom, right, topleft, bottomleft, topright, bottomright,
            midtop, midleft, midbottom, midright, center, centerx, centery,
            size, w, h.
        
        Module initialization places pyj2d.Rect in module's namespace.
        """
        def unpack(arg, lst=[]):
            for x in arg:
                if not isinstance(x, tuple):
                    lst.append(x)
                else:
                    lst = unpack(x, lst)
            return lst
        try:
            x,y,w,h = arg[0], arg[1], arg[2], arg[3]
        except IndexError:
            try:
                x,y,w,h = arg[0][0], arg[0][1], arg[0][2], arg[0][3]
            except (IndexError, TypeError, AttributeError):
                arg = unpack(arg)
                try:
                    x,y,w,h = arg[0], arg[1], arg[2], arg[3]
                except IndexError:
                    if hasattr(arg[0], 'rect'):
                        arg[0] = arg[0].rect
                    x,y,w,h = arg[0].x, arg[0].y, arg[0].width, arg[0].height
        try:
            Rectangle.__init__(self, x, y, w, h)
        except TypeError:
            Rectangle.__init__(self, int(x), int(y), int(w), int(h))

    def __repr__(self):
        """
        Return string representation of Rect object.
        """
        return "%s(%s)" % (self.__class__, self.toString())

    def __getattr__(self, attr):
        """
        Get Rect attributes.
        """
        try:
            return Rect._at[attr](self)
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, val):
        """
        Set Rect attributes.
        """
        try:
            Rect._xy[attr](self, val)
        except TypeError:
            try:
                Rect._xy[attr](self, int(val))
            except TypeError:
                Rect._xy[attr](self, (int(val[0]), int(val[1])))
        return None

    def __getitem__(self, key):
        """
        Get Rect [x,y,width,height] attributes by index.
        """
        return [self.x, self.y, self.width, self.height][key]

    def __setitem__(self, key, val):
        """
        Set Rect [x,y,width,height] attributes by index.
        """
        val = int(val)
        [lambda val: self.__setattr__("x", val), lambda val: self.__setattr__("y", val), lambda val: self.__setattr__("width", val), lambda val: self.__setattr__("height", val)][key](val)

    def __nonzero__(self):
        """
        Rect nonzero check.
        """
        return self.width and self.height

    def __eq__(self, other):
        """
        Rects equality check.
        """
        try:
            return self.x==other.x and self.y==other.y and self.width==other.width and self.height==other.height
        except AttributeError:
            return self.x==other[0] and self.y==other[1] and self.width==other[2] and self.height==other[3]

    def __ne__(self, other):
        """
        Rects equality check.
        """
        try:
            return self.x!=other.x or self.y!=other.y or self.width!=other.width or self.height!=other.height
        except AttributeError:
            return self.x!=other[0] or self.y!=other[1] or self.width!=other[2] or self.height!=other[3]

    def copy(self):
        """
        Returns Rect that is a copy of this rect.
        """
        return Rect(self.x, self.y, self.width, self.height)

    def movex(self, x, y):      #super uses java.awt.Rectangle.move()
        """
        Return Rect of same dimension at position offset by x,y.
        """
        return Rect(self.x+x, self.y+y, self.width, self.height)

    def move_ip(self, *pos):
        """
        Moves this rect to position offset by x,y.
        """
        try:
            x, y = pos
        except ValueError:
            x, y = pos[0]
        try:
            self.setLocation(self.x+x, self.y+y)
        except TypeError:
            self.setLocation(self.x+int(x), self.y+int(y))
        return None

    def inflate(self, x, y):
        """
        Return Rect at same position but size offset by x,y.
        """
        return Rect(self.x-int(float(x)/2), self.y-int(float(y)/2), self.width+x, self.height+y)

    def inflate_ip(self, x, y):
        """
        Change size of this rect offset by x,y.
        """
        try:
            self.setSize(self.width+x, self.height+y)
        except TypeError:
            self.setSize(self.width+int(x), self.height+int(y))
        self.setLocation(self.x-int(float(x)/2), self.y-int(float(y)/2))
        return None

    def clip(self, rect):
        """
        Return Rect representing the intersection of rect and this rect.
        """
        clipRect = self.createIntersection(rect)
        if clipRect.width > 0 and clipRect.height > 0:
            return Rect(clipRect.x,clipRect.y,clipRect.width,clipRect.height)
        else:
            return Rect(0,0,0,0)

    def unionx(self, rect):     #super uses java.awt.Rectangle.union()
        """
        Return Rect representing the union of rect and this rect.
        """
        unionRect = Rect((0,0,0,0))
        self.union(self, rect, unionRect)
        return unionRect

    def union_ip(self, rect):
        """
        Change this rect to represent the union of rect and this rect.
        """
        self.union(self, rect, self)
        return None

    def unionall(self, rect_list):
        """
        Return Rect representing the union of rect list and this rect.
        """
        unionRect = Rect((self.x,self.y,self.width,self.height))
        for rect in rect_list:
            self.union(unionRect, rect, unionRect)
        return unionRect

    def unionall_ip(self, rect_list):
        """
        Change this rect to represent the union of rect list and this rect.
        """
        for rect in rect_list:
            self.union(self, rect, self)
        return None

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

