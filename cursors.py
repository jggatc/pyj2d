#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#java.awt.Cursor API
#http://docs.oracle.com/javase/7/docs/api/java/awt/Cursor.html

#Constant Field          Value
#CROSSHAIR_CURSOR          1
#DEFAULT_CURSOR 	       0
#E_RESIZE_CURSOR 	      11
#HAND_CURSOR 	          12
#MOVE_CURSOR 	          13
#N_RESIZE_CURSOR 	       8
#NE_RESIZE_CURSOR 	       7
#NW_RESIZE_CURSOR 	       6
#S_RESIZE_CURSOR 	       9
#SE_RESIZE_CURSOR 	       5
#SW_RESIZE_CURSOR 	       4
#TEXT_CURSOR 	           2
#W_RESIZE_CURSOR 	      10
#WAIT_CURSOR 	           3
#CUSTOM_CURSOR 	          -1

from java.awt import Cursor


CROSSHAIR_CURSOR = Cursor.CROSSHAIR_CURSOR
DEFAULT_CURSOR = Cursor.DEFAULT_CURSOR
E_RESIZE_CURSOR = Cursor.E_RESIZE_CURSOR
HAND_CURSOR = Cursor.HAND_CURSOR
MOVE_CURSOR = Cursor.MOVE_CURSOR
N_RESIZE_CURSOR = Cursor.N_RESIZE_CURSOR
NE_RESIZE_CURSOR = Cursor.NE_RESIZE_CURSOR
NW_RESIZE_CURSOR = Cursor.NW_RESIZE_CURSOR
S_RESIZE_CURSOR = Cursor.S_RESIZE_CURSOR
SE_RESIZE_CURSOR = Cursor.SE_RESIZE_CURSOR
SW_RESIZE_CURSOR = Cursor.SW_RESIZE_CURSOR
TEXT_CURSOR = Cursor.TEXT_CURSOR
W_RESIZE_CURSOR = Cursor.W_RESIZE_CURSOR
WAIT_CURSOR = Cursor.WAIT_CURSOR

#cursors not implemented
arrow = diamond = broken_x = tri_left = tri_right = ()

