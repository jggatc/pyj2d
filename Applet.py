from javax.swing import JApplet, JPanel
from java.awt import Color, Dimension, Toolkit
from java.awt.image import BufferedImage
from java.lang import Runnable
from java.lang import Thread
import pyj2d.event
import pyj2d.surface
import pyj2d.env

##############################
#Applet configuration:
# Script name to import
# Applet size
# Program setup
# Program execution

import script as app    #import script

_app_size = ()          #applet size (w,h)

class Program(object):

    def __init__(self):
        """
        Python script to run in applet.
        """
        self.size = _app_size
        self.quit = False
        self.setup()

    def setup(self):
        """
        Program setup.
        """
        app.program_setup(self.size)        #program setup

    def update(self):
        """
        Program update.
        """
        while not self.quit:
            self.quit = app.program_exec()  #program execution

##############################


class Applet(JApplet, Runnable):

    def init(self):
        self.setBackground(Color.BLACK)
        self.jpanel = Panel(_app_size)
        self.getContentPane().add(self.jpanel)
        pyj2d.env.japplet = self
        self.event = pyj2d.event
        self.mousePressed = self.mousePress
        self.mouseReleased = self.mouseRelease
        self.mouseEntered = self.mouseEnter
        self.mouseExited = self.mouseExit
        self.mouseMoved = self.mouseMove
        self.keyPressed = self.keyPress
        self.keyReleased = self.keyRelease
        self.setFocusable(True)
        self.program = Program()
        self.thread = Thread(self)
        self.thread.start()

    def mousePress(self, event):
        self.event.mousePress = event
        self.event._updateQueue(event)

    def mouseRelease(self, event):
        self.event.mousePress = None
        self.event._updateQueue(event)

    def mouseEnter(self, event):
        self.requestFocus()

    def mouseExit(self, event):
        self.event.mousePress = None

    def mouseMove(self, event):
        self.event._updateQueue(event)

    def keyPress(self, event):
        self.event._updateQueue(event)

    def keyRelease(self, event):
        self.event._updateQueue(event)

    def run(self):
        self.program.update()
        self.stop()

    def stop(self):
        self.program.quit = True
        self.thread = None


class Panel(JPanel):

    def __init__(self, size):
        JPanel.__init__(self)
        self.setPreferredSize(Dimension(size[0],size[1]))
        self.surface = pyj2d.surface.Surface(size, BufferedImage.TYPE_INT_RGB)
        self.setBackground(Color.BLACK)

    def paintComponent(self, g2d):
        self.super__paintComponent(g2d)
        g2d.drawImage(self.surface, 0, 0, None)
        try:
            Toolkit.getDefaultToolkit().sync()
        except:
            pass


if __name__ == '__main__':
    import pawt
    pawt.test(Applet(), size=_app_size)

