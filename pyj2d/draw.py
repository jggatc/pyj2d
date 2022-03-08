#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from math import pi as _pi
from java.awt import BasicStroke, RenderingHints
from java.awt.geom import Ellipse2D
from pyj2d.rect import Rect
from pyj2d.color import Color

__docformat__ = 'restructuredtext'

__doc__ = 'Draw shapes'


_rad_deg = 180.0/_pi
_return_rect = True


def rect(surface, color, rect, width=0):
    """
    Draw rectangle shape, and returns bounding Rect.
    Arguments include surface to draw, color, Rect.
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
    if not _return_rect:
        return None
    return surface.get_rect().clip(rect)


def circle(surface, color, position, radius, width=0):
    """
    Draw circular shape, and returns bounding Rect.
    Arguments include surface to draw, color, position and radius.
    Optional width argument of outline, which defaults to 0 for filled shape.
    """
    rect = Rect(position[0]-radius, position[1]-radius, 2*radius, 2*radius)
    g = surface.createGraphics()
    if hasattr(color, 'a'):
        g.setColor(color)
    else:
        g.setColor(Color(color))
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                       RenderingHints.VALUE_ANTIALIAS_ON)
    if width:
        g.setStroke(BasicStroke(width))
        g.drawOval(rect.x, rect.y, rect.width, rect.height)
    else:
        g.fillOval(rect.x, rect.y, rect.width, rect.height)
    g.dispose()
    if not _return_rect:
        return None
    return surface.get_rect().clip(rect)


def ellipse(surface, color, rect, width=0):
    """
    Draw ellipse shape, and returns bounding Rect.
    Arguments include surface to draw, color, and rect.
    Optional width argument of outline, which defaults to 0 for filled shape.
    """
    if not hasattr(rect, 'width'):
        rect = Rect(rect)
    g = surface.createGraphics()
    if hasattr(color, 'a'):
        g.setColor(color)
    else:
        g.setColor(Color(color))
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                       RenderingHints.VALUE_ANTIALIAS_ON)
    ellipse = Ellipse2D.Double(rect.x, rect.y, rect.width, rect.height)
    if width:
        g.draw(ellipse)
    else:
        g.fill(ellipse)
    g.dispose()
    if not _return_rect:
        return None
    return surface.get_rect().clip(rect)


def arc(surface, color, rect, start_angle, stop_angle, width=1):
    """
    Draw arc shape, and returns bounding Rect.
    Arguments include surface to draw, color, rect, start_angle, stop_angle.
    Optional width argument of outline.
    """
    if not hasattr(rect, 'width'):
        rect = Rect(rect)
    start_angle = int(start_angle * _rad_deg)
    stop_angle = int(stop_angle * _rad_deg)
    g = surface.createGraphics()
    if hasattr(color, 'a'):
        g.setColor(color)
    else:
        g.setColor(Color(color))
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                       RenderingHints.VALUE_ANTIALIAS_ON)
    if width:
        g.setStroke(BasicStroke(width))
        g.drawArc(rect.x, rect.y, rect.width-1, rect.height-1,
                  start_angle, stop_angle)
    else:
        g.fillArc(rect.x, rect.y, rect.width-1, rect.height-1,
                  start_angle, stop_angle)
    g.dispose()
    if not _return_rect:
        return None
    return surface.get_rect().clip(rect)


def polygon(surface, color, pointlist, width=0):
    """
    Draw polygon shape, and returns bounding Rect.
    Arguments include surface to draw, color, and pointlist.
    Optional width argument of outline, which defaults to 0 for filled shape.
    """
    g = surface.createGraphics()
    if hasattr(color, 'a'):
        g.setColor(color)
    else:
        g.setColor(Color(color))
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                       RenderingHints.VALUE_ANTIALIAS_ON)
    xpts = [int(pt[0]) for pt in pointlist]
    ypts = [int(pt[1]) for pt in pointlist]
    npts = len(pointlist)
    if width:
        g.setStroke(BasicStroke(width))
        g.drawPolygon(xpts, ypts, npts)
    else:
        g.fillPolygon(xpts, ypts, npts)
    g.dispose()
    if not _return_rect:
        return None
    xmin = min(xpts)
    xmax = max(xpts)
    ymin = min(ypts)
    ymax = max(ypts)
    rect = Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1)
    return surface.get_rect().clip(rect)


def line(surface, color, point1, point2, width=1):
    """
    Draw line, and returns bounding Rect.
    Arguments include surface to draw, color, point1, point2.
    Optional width argument of line.
    """
    g = surface.createGraphics()
    if hasattr(color, 'a'):
        g.setColor(color)
    else:
        g.setColor(Color(color))
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                       RenderingHints.VALUE_ANTIALIAS_ON)
    g.setStroke(BasicStroke(width))
    g.drawLine(int(point1[0]), int(point1[1]),
               int(point2[0]), int(point2[1]))
    g.dispose()
    if not _return_rect:
        return None
    xpts = [pt[0] for pt in (point1, point2)]
    ypts = [pt[1] for pt in (point1, point2)]
    xmin = min(xpts)
    xmax = max(xpts)
    ymin = min(ypts)
    ymax = max(ypts)
    rect = Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1)
    return surface.get_rect().clip(rect)


def lines(surface, color, closed, pointlist, width=1):
    """
    Draw interconnected lines, and returns Rect bound.
    Arguments include surface to draw, color, closed, and pointlist.
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
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                       RenderingHints.VALUE_ANTIALIAS_ON)
    g.setStroke(BasicStroke(width))
    g.drawPolyline(xpoints, ypoints, npoints)
    g.dispose()
    if not _return_rect:
        return None
    xmin = min(xpoints)
    xmax = max(xpoints)
    ymin = min(ypoints)
    ymax = max(ypoints)
    rect = Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1)
    return surface.get_rect().clip(rect)


def aaline(surface, color, point1, point2, blend=1):
    """
    Draw line, and returns bounding Rect.
    Arguments include surface to draw, color, point1, point2.
    """
    rect = line(surface, color, point1, point2)
    return rect


def aalines(surface, color, closed, pointlist, blend=1):
    """
    Draw interconnected lines, and returns Rect bound.
    Arguments include surface to draw, color, closed, and pointlist.
    """
    rect = lines(surface, color, closed, pointlist)
    return rect


def bounding_rect_return(setting):
    """
    Set whether draw functions return bounding Rect.
    Setting (bool) defaults to True on module initialization.
    """
    global _return_rect
    _return_rect = setting


#depreciated
def _set_return(*args):
    msg = 'set_return depreciated, use bounding_rect_return'
    raise Exception(msg)
set_return = _set_return

