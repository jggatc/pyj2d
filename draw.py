#PyJ2D - Copyright (C) 2011 James Garnon

from __future__ import division
from math import pi
from java.awt import BasicStroke, RenderingHints
from rect import Rect
from color import Color

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
        rect = Rect(rect)
        g = surface.createGraphics()
        g.setColor(Color(color))
        if width:
            g.setStroke(BasicStroke(width))
            g.drawRect(rect.x, rect.y, rect.width, rect.height)
        else:
            g.fillRect(rect.x, rect.y, rect.width, rect.height)
        g.dispose()
        return surface.get_rect().clip(rect)

    def circle(self, surface, color, position, radius, width=0):
        """
        Draw circular shape, and returns bounding Rect.
        Argument include surface to draw, color, position and radius.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        rect = Rect(position[0]-radius, position[1]-radius, 2*radius, 2*radius)
        g = surface.createGraphics()
        g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        if width:
            g.setStroke(BasicStroke(width))
            g.drawOval(rect.x, rect.y, rect.width, rect.height)
        else:
            g.fillOval(rect.x, rect.y, rect.width, rect.height)
        g.dispose()
        return surface.get_rect().clip(rect)

    def arc(self, surface, color, rect, start_angle, stop_angle, width=1):
        """
        Draw arc shape, and returns bounding Rect.
        Argument include surface to draw, color, rect, start_angle, stop_angle.
        Optional width argument of outline.
        """
        rect = Rect(rect)
        start_angle = int(start_angle * self.rad_deg)
        stop_angle = int(stop_angle * self.rad_deg)
        g = surface.createGraphics()
        g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        if width:
            g.setStroke(BasicStroke(width))
            g.drawArc(rect.x-(rect.width//8), rect.y-(rect.height//8), rect.width, rect.height, start_angle, stop_angle)
        else:
            g.fillArc(rect.x-(rect.width//8), rect.y-(rect.height//8), rect.width, rect.height, start_angle, stop_angle)
        g.dispose()
        return surface.get_rect().clip(rect)

    def polygon(self, surface, color, pointlist, width=0):
        """
        Draw polygon shape, and returns bounding Rect.
        Argument include surface to draw, color, and pointlist.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        g = surface.createGraphics()
        g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
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
        rect = Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1)
        return surface.get_rect().clip(rect)

    def line(self, surface, color, point1, point2, width=1):
        """
        Draw line, and returns bounding Rect.
        Argument include surface to draw, color, point1, point2.
        Optional width argument of line.
        """
        p1x, p1y = point1
        p2x, p2y = point2
        g = surface.createGraphics()
        g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        g.setStroke(BasicStroke(width))
        g.drawLine(p1x,p1y,p2x,p2y)
        g.dispose()
        xpts = [pt[0] for pt in (point1,point2)]
        ypts = [pt[1] for pt in (point1,point2)]
        xmin = min(xpts)
        xmax = max(xpts)
        ymin = min(ypts)
        ymax = max(ypts)
        rect = Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1)
        return surface.get_rect().clip(rect)

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
        g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        g.setStroke(BasicStroke(width))
        g.drawPolyline(xpoints, ypoints, npoints)
        g.dispose()
        xmin = min(xpoints)
        xmax = max(xpoints)
        ymin = min(ypoints)
        ymax = max(ypoints)
        rect = Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1)
        return surface.get_rect().clip(rect)

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

