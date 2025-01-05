#PyJ2D - Copyright (C) 2011 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
JNumeric module is required for Numeric functionality.
Obtain JNumeric:
https://central.sonatype.com/artifact/com.github.tbekolay.jnumeric/jnumeric
JNumeric from this repository works with Jython 2.5.3.
Use one of following options:
-place jnumeric-0.1.jar in pyj2d folder.
 (optionally named jnumeric.jar or numeric.jar)
-place in sys path:
 'sys.path.append(<jnumeric-0.1.jar path>)'.
-run script with classpath option:
 'java -cp jython.jar:jnumeric-0.1.jar:$CLASSPATH org.python.util.jython script.py'.
"""

import os, sys


def _get_numeric_path():
    module_path = os.path.dirname(__file__)
    for jar_file in ('jnumeric-0.1.jar', 'jnumeric.jar', 'numeric.jar'):
        path = os.path.join(module_path, jar_file)
        if os.path.isfile(path):
            return path
    return None


_path = _get_numeric_path()
if _path:
    sys.path.append(_path)


numeric = None


if not numeric:
    try:
        from com.github.tbekolay.jnumeric import JNumeric as numeric
    except ImportError:
        pass


def set_numeric_module(module):
    """
    Set numeric module.
    The argument is module path or imported module.
    """
    global numeric
    if isinstance(module, str):
        sys.path.append(module)
        try:
            from com.github.tbekolay.jnumeric import JNumeric as numeric
        except ImportError:
            pass
    else:
        numeric = module


def get_numeric_module():
    """
    Get numeric module.
    Return None if module not present.
    """
    return numeric

