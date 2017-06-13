#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from math import pi as _pi
from java.awt import BasicStroke, RenderingHints
from java.awt.geom import Ellipse2D
from pyj2d.rect import Rect
from pyj2d.color import Color

__docformat__ = 'restructuredtext'


class Draw(object):
    """
    **pyj2d.draw**
    
    * pyj2d.draw.rect
    * pyj2d.draw.circle
    * pyj2d.draw.ellipse
    * pyj2d.draw.arc
    * pyj2d.draw.polygon
    * pyj2d.draw.line
    * pyj2d.draw.lines
    * pyj2d.draw.aaline
    * pyj2d.draw.aalines
    * pyj2d.draw.set_return
    """

    def __init__(self):
        """
        Draw shapes.
        
        Module initialization creates pyj2d.draw instance.
        """
        self.rad_deg = 180/_pi
        self._return_rect = True

    def rect(self, surface, color, rect, width=0):
        """
        Draw rectangle shape, and returns bounding Rect.
        Argument include surface to draw, color, Rect.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        if not hasattr(rect, 'width'):
            rect = Rect(rect)
        g = surface.createGraphics()
        if hasattr(color, 'a'):
            g.setColor(color)
        else:
            g.setColor(Color(color))
        if width:
            g.setStroke(BasicStroke(width))
            g.drawRect(rect.x, rect.y, rect.width, rect.height)
        else:
            g.fillRect(rect.x, rect.y, rect.width, rect.height)
        g.dispose()
        if not self._return_rect:
            return None
        return surface.get_rect().clip(rect)

    def circle(self, surface, color, position, radius, width=0):
        """
        Draw circular shape, and returns bounding Rect.
        Argument include surface to draw, color, position and radius.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        rect = Rect(position[0]-radius, position[1]-radius, 2*radius, 2*radius)
        g = surface.createGraphics()
        if hasattr(color, 'a'):
            g.setColor(color)
        else:
            g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        if width:
            g.setStroke(BasicStroke(width))
            g.drawOval(rect.x, rect.y, rect.width, rect.height)
        else:
            g.fillOval(rect.x, rect.y, rect.width, rect.height)
        g.dispose()
        if not self._return_rect:
            return None
        return surface.get_rect().clip(rect)

    def ellipse(self, surface, color, rect, width=0):
        """
        Draw ellipse shape, and returns bounding Rect.
        Argument include surface to draw, color, and rect.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        if not hasattr(rect, 'width'):
            rect = Rect(rect)
        g = surface.createGraphics()
        if hasattr(color, 'a'):
            g.setColor(color)
        else:
            g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        ellipse = Ellipse2D.Double(rect.x, rect.y, rect.width, rect.height)
        if width:
            g.draw(ellipse)
        else:
            g.fill(ellipse)
        g.dispose()
        if not self._return_rect:
            return None
        return surface.get_rect().clip(rect)

    def arc(self, surface, color, rect, start_angle, stop_angle, width=1):
        """
        Draw arc shape, and returns bounding Rect.
        Argument include surface to draw, color, rect, start_angle, stop_angle.
        Optional width argument of outline.
        """
        if not hasattr(rect, 'width'):
            rect = Rect(rect)
        start_angle = int(start_angle * self.rad_deg)
        stop_angle = int(stop_angle * self.rad_deg)
        g = surface.createGraphics()
        if hasattr(color, 'a'):
            g.setColor(color)
        else:
            g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        if width:
            g.setStroke(BasicStroke(width))
            g.drawArc(rect.x, rect.y, rect.width-1, rect.height-1, start_angle, stop_angle)
        else:
            g.fillArc(rect.x, rect.y, rect.width-1, rect.height-1, start_angle, stop_angle)
        g.dispose()
        if not self._return_rect:
            return None
        return surface.get_rect().clip(rect)

    def polygon(self, surface, color, pointlist, width=0):
        """
        Draw polygon shape, and returns bounding Rect.
        Argument include surface to draw, color, and pointlist.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        g = surface.createGraphics()
        if hasattr(color, 'a'):
            g.setColor(color)
        else:
            g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        xpts = [int(pt[0]) for pt in pointlist]
        ypts = [int(pt[1]) for pt in pointlist]
        npts = len(pointlist)
        if width:
            g.setStroke(BasicStroke(width))
            g.drawPolygon(xpts,ypts,npts)
        else:
            g.fillPolygon(xpts,ypts,npts)
        g.dispose()
        if not self._return_rect:
            return None
        xmin = min(xpts)
        xmax = max(xpts)
        ymin = min(ypts)
        ymax = max(ypts)
        rect = Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1)
        return surface.get_rect().clip(rect)

    def line(self, surface, color, point1, point2, width=1):
        """
        Draw line, and returns bounding Rect.
        Argument include surface to draw, color, point1, point2.
        Optional width argument of line.
        """
        g = surface.createGraphics()
        if hasattr(color, 'a'):
            g.setColor(color)
        else:
            g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        g.setStroke(BasicStroke(width))
        g.drawLine(int(point1[0]),int(point1[1]),int(point2[0]),int(point2[1]))
        g.dispose()
        if not self._return_rect:
            return None
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
        xpoints = [int(p[0]) for p in pointlist]
        ypoints = [int(p[1]) for p in pointlist]
        if closed:
            xpoint, ypoint = xpoints[0], ypoints[0]
            xpoints.append(xpoint)
            ypoints.append(ypoint)
        npoints = len(xpoints)
        g = surface.createGraphics()
        if hasattr(color, 'a'):
            g.setColor(color)
        else:
            g.setColor(Color(color))
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        g.setStroke(BasicStroke(width))
        g.drawPolyline(xpoints, ypoints, npoints)
        g.dispose()
        if not self._return_rect:
            return None
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

    def set_return(self, setting):
        """
        Set whether draw methods return bounding Rect.
        """
        self._return_rect = setting

