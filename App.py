#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from javax.swing import JApplet, JPanel
from java.awt import Color, Dimension, Toolkit
from java.awt.image import BufferedImage
from java.lang import Runnable
from java.lang import Thread
from java.awt.event import MouseEvent, KeyEvent
from java.util.concurrent.atomic import AtomicBoolean
import pyj2d.event
import pyj2d.surface
import pyj2d.env


##############################
#App configuration:
# Refer to instructions at end of file
# Copy App.py to script folder
# Edit App.py for your script
#  -Script name to import
#  -App size
#  -Program setup
#  -Program execution

import script as app    #import script

_app_size = ()          #app size (w,h)

class Program(object):

    def __init__(self):
        """
        Python script to run in app.
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


class App(JApplet, Runnable):

    def init(self):
        self.setBackground(Color.BLACK)
        self.jpanel = Panel(_app_size)
        self.getContentPane().add(self.jpanel)
        pyj2d.env.japplet = self
        self.event = pyj2d.event
        self.modKey = pyj2d.event.modKey
        self.mousePressed = self.mousePress
        self.mouseReleased = self.mouseRelease
        self.mouseEntered = self.mouseEnter
        self.mouseExited = self.mouseExit
        self.mouseMoved = self.mouseMove
        self.mouseDragged = self.mouseDrag
        self.mouseWheelMoved = self.mouseWheelMove
        self.keyPressed = self.keyPress
        self.keyReleased = self.keyRelease
        self.setFocusable(True)
        self.program = Program()
        self.thread = Thread(self)
        self.thread.start()

    def mousePress(self, event):
        self.event.mousePress[event.button] = True
        self.event._updateQueue(event, MouseEvent.MOUSE_PRESSED)

    def mouseRelease(self, event):
        self.event.mousePress[event.button] = False
        self.event._updateQueue(event, MouseEvent.MOUSE_RELEASED)

    def mouseEnter(self, event):
        self.requestFocus()

    def mouseExit(self, event):
        self.event.mousePress[1], self.event.mousePress[2], self.event.mousePress[3] = False, False, False
        for keycode in self.modKey:
            if self.event.keyPress[keycode]:
                self.event.keyPress[keycode] = False

    def mouseMove(self, event):
        self.event._updateQueue(event, MouseEvent.MOUSE_MOVED)

    def mouseDrag(self, event):
        self.event._updateQueue(event, MouseEvent.MOUSE_MOVED)

    def mouseWheelMove(self, event):
        self.event._updateQueue(event, MouseEvent.MOUSE_PRESSED)

    def keyPress(self, event):
        if event.keyCode in self.modKey:
            self.event.keyPress[event.keyCode] = True
        self.event._updateQueue(event, KeyEvent.KEY_PRESSED)

    def keyRelease(self, event):
        if event.keyCode in self.modKey:
            self.event.keyPress[event.keyCode] = False
        self.event._updateQueue(event, KeyEvent.KEY_RELEASED)

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
        self._repainting = AtomicBoolean(False)

    def paintComponent(self, g2d):
        self.super__paintComponent(g2d)
        g2d.drawImage(self.surface, 0, 0, None)
        try:
            Toolkit.getDefaultToolkit().sync()
        except:
            pass
        self._repainting.set(False)


if __name__ == '__main__':
    import pawt
    pawt.test(App(), size=_app_size)


"""

This information can be used to deploy a Java app online. Copy App.py to the script folder with PyJ2D on the path. Edit App.py to import your Python script, set app size, and code to link the app thread to the script application, including script setup that will be called upon app initialization and script execution statements that will update during the app thread loop. Alternatively, use App.py as a guide and edit your Python script accordingly. To test, the edited App.py script can be run directly on the desktop JVM using the command 'jython App.py', which executes the app code with the pawt module in main(). To create an app jar that can be deployed online, use jythonc available for Jython 2.2.1, with the command 'jythonc --core --deep --jar Pyj2d_App.jar App.py' to package together with Jython dependencies, or 'jythonc --jar Pyj2d_App.jar App.py' to package alone in which case jython.jar must be included. The mixer function requires Mixer.class (compiled with 'javac Mixer.java') and should be included in the jar with 'jar uvf Pyj2d_App.jar pyj2d/Mixer.class'. To update the app jar with a resources folder containing image and audio files, use command 'jar uvf Pyj2d_App.jar resources'. Note that Java apps do not start from main() rather launch from japplet subclass with the same name as the script.

To run the app on desktop before deployment online, use appletviewer included with JDK package, which tests execution and whether the app conforms to the security profile. Using this method with Java 6 unsigned apps were created successfully, but if code is required that violates the security profile such as disk access, the app needs to be signed for permission. Current versions of Java requires all online apps to be signed, unless security configuration is changed. The functionality of online deployment using PyJ2D has not been maintained, creation of unsigned apps was verified using PyJ2D 0.23 (http://s3.gatc.ca/files/PyJ2D_0.23.zip). Code that can be used to launch the app is provided at the end of this file. To use appletviewer, place an edited App.html together with the app jar(s), and use command 'appletviewer App.html'. To deploy online, place the app jar(s) on a Web server and use an edited App.js and the HTML code that calls the JavaScript function to launch the app from the Web browser.


Example code to launch app packaged in Pyj2d_App.jar with separate jython.jar:
(edit the Pyj2d_App name and app size)

HTML code for App.html file:
<HTML>
<BODY>
<OBJECT CODE="App.class" WIDTH="400" HEIGHT="300"
	ARCHIVE="Pyj2d_App.jar,jython.jar" 
	NAME="PyJ2D App"
	ALIGN="BOTTOM" 
	alt="To use this app, you need a JVM plug-in.">
 <H3>Unable to load app.</H3>
</OBJECT>
</BODY>
</HTML>


Example code for JavaScript launchable app packaged in Pyj2d_App.jar with separate jython.jar:
(edit the Pyj2d_App name, app size, and site URL)

JavaScript code for App.js file:
<script type="text/javascript">
function appLauncher (appArchive,appCode,appWidth,appHeight)
{
  var appID = appArchive;
  var appArchive = appArchive + ".jar,jython.jar";
  var appCodebase = "http://website.com/apps/";
  var appCode = appCode || "App.class";
  var appWidth = appWidth || "400";
  var appHeight = appHeight || "300";
  document.getElementById(appID).innerHTML = '<applet width=' + appWidth + ' height=' + appHeight + ' codebase=' + appCodebase + ' code=' + appCode + ' archive=' + appArchive + ' alt="App requires JVM to run">';
}
</script>

HTML code embedded on the Web page:

<div id="Pyj2d_App" title="App: Pyj2d_App" style="width:400px; height:300px; border:1px solid #333; background-color:#000; position:relative; left:100px;">
<input type='button' value='Launch App' onClick='appLauncher("Pyj2d_App")'/>
<div style="position:absolute; top:138px; width:400px; font-size:24px; color:#646464; text-align:center;">App</div>
</div>

"""

