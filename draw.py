#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from math import pi
from java.awt import BasicStroke
from rect import Rect
from color import Color     #0.23

__docformat__ = 'restructuredtext'


class Draw(object):
    """
    **pyj2d.draw**
    
    * pyj2d.draw.rect
    * pyj2d.draw.circle
    * pyj2d.draw.arc
    * pyj2d.draw.polygon
    * pyj2d.draw.line
    * pyj2d.draw.lines
    * pyj2d.draw.aaline
    * pyj2d.draw.aalines
    """

    def __init__(self):
        """
        Draw shapes.
        
        Module initialization creates pyj2d.draw instance.        
        """
        self.rad_deg = 180/pi

    def rect(self, surface, color, rect, width=0):
        """
        Draw rectangle shape, and returns bounding Rect.
        Argument include surface to draw, color, Rect.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        try:
            x,y,w,h = rect.x, rect.y, rect.width, rect.height
        except AttributeError:
            try:
                x,y,w,h = rect
            except ValueError:
                x,y = rect[0]
                w,h = rect[1]
            rect = Rect(x,y,w,h)
        g = surface.createGraphics()
        g.setColor(Color(color))    #0.23
        if width:
            g.setStroke(BasicStroke(width))
            g.drawRect(x,y,w,h)
        else:
            g.fillRect(x,y,w,h)
        g.dispose()
        return rect

    def circle(self, surface, color, position, radius, width=0):
        """
        Draw circular shape, and returns bounding Rect.
        Argument include surface to draw, color, position and radius.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        x, y = position
        w, h = 2*radius, 2*radius
        g = surface.createGraphics()
        g.setColor(Color(color))    #0.23
        if width:
            g.setStroke(BasicStroke(width))
            g.drawOval(x-radius, y-radius, w, h)
        else:
            g.fillOval(x-radius, y-radius, w, h)
        g.dispose()
        return Rect(x,y,w,h)

    def arc(self, surface, color, rect, start_angle, stop_angle, width=1):
        """
        Draw arc shape, and returns bounding Rect.
        Argument include surface to draw, color, rect, start_angle, stop_angle.
        Optional width argument of outline.
        """
        try:
            x,y,w,h = rect.x, rect.y, rect.width, rect.height
        except AttributeError:
            try:
                x,y,w,h = rect
            except ValueError:
                x,y = rect[0]
                w,h = rect[1]
            rect = Rect(x,y,w,h)
        start_angle = int(start_angle * self.rad_deg)
        stop_angle = int(stop_angle * self.rad_deg)
        x -= w//8
        y -= h//8
        g = surface.createGraphics()
        g.setColor(Color(color))    #0.23
        if width:
            g.setStroke(BasicStroke(width))
            g.drawArc(x, y, w, h, start_angle, stop_angle)
        else:
            g.fillArc(x, y, w, h, start_angle, stop_angle)
        g.dispose()
        return rect

    def polygon(self, surface, color, pointlist, width=0):
        """
        Draw polygon shape, and returns bounding Rect.
        Argument include surface to draw, color, and pointlist.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        g = surface.createGraphics()
        g.setColor(Color(color))    #0.23
        xpts = [pt[0] for pt in pointlist]
        ypts = [pt[1] for pt in pointlist]
        npts = len(pointlist)
        xmin = min(xpts)
        xmax = max(xpts)
        ymin = min(ypts)
        ymax = max(ypts)
        if width:
            g.setStroke(BasicStroke(width))
            g.drawPolygon(xpts,ypts,npts)
        else:
            g.fillPolygon(xpts,ypts,npts)
        g.dispose()
        return Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1)

    def line(self, surface, color, point1, point2, width=1):
        """
        Draw line, and returns bounding Rect.
        Argument include surface to draw, color, point1, point2.
        Optional width argument of line.
        """
        p1x, p1y = point1
        p2x, p2y = point2
        g = surface.createGraphics()
        g.setColor(Color(color))    #0.23
        g.setStroke(BasicStroke(width))
        g.drawLine(p1x,p1y,p2x,p2y)
        g.dispose()
        xpts = [pt[0] for pt in (point1,point2)]
        ypts = [pt[1] for pt in (point1,point2)]
        xmin = min(xpts)
        xmax = max(xpts)
        ymin = min(ypts)
        ymax = max(ypts)
        w = xmax-xmin
        h = ymax-ymin
        return Rect(xmin, ymin, w, h)

    def lines(self, surface, color, closed, pointlist, width=1):
        """
        Draw interconnected lines, and returns Rect bound.
        Argument include surface to draw, color, closed, and pointlist.
        Optional width argument of line.
        """
        xpoints = [p[0] for p in pointlist]
        ypoints = [p[1] for p in pointlist]
        if closed:
            xpoint, ypoint = xpoints[0], ypoints[0]
            xpoints.append(xpoint)
            ypoints.append(ypoint)
        npoints = len(xpoints)
        g = surface.createGraphics()
        g.setColor(Color(color))    #0.23
        g.setStroke(BasicStroke(width))
        g.drawPolyline(xpoints, ypoints, npoints)
        g.dispose()
        xmin = min(xpoints)
        xmax = max(xpoints)
        ymin = min(ypoints)
        ymax = max(ypoints)
        w = xmax-xmin
        h = ymax-ymin
        return Rect(xmin, ymin, w, h)

    def aaline(self, surface, color, point1, point2, blend=1):
        """
        Calls line(), return bounding Rect.
        """
        rect = self.line(surface, color, point1, point2, blend)
        return rect

    def aalines(self, surface, color, closed, pointlist, blend=1):
        """
        Calls lines(), return bounding Rect.
        """
        rect = self.lines(surface, color, closed, pointlist, blend)
        return rect

