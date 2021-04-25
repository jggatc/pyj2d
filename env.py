#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

import os, sys


if os.name != 'java':
    print('Use Jython to run script')
    sys.exit()


jframe = None

japplet = None

event = None

