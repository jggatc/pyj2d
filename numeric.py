#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#JNumeric module:
#http://jnumerical.sourceforge.net/
#JNumeric does not work with Jython2.2.1
#JNumeric was updated to work with Jython2.5.2:
#http://search.maven.org/#browse|-1501684728 - jnumeric-0.1.jar
#Place JNumeric in Java classpath:
#java -cp jython.jar:jnumeric-0.1.jar:$CLASSPATH org.python.util.jython script.py
#For a different JNumeric package, modify import statement or use set_numeric_module.

numeric = None

if not numeric:
    try:
        from com.github.tbekolay.jnumeric import JNumeric as numeric
    except ImportError:
        try:
            import Numeric as numeric
        except ImportError:
            pass


def set_numeric_module(module):
    """
    Set numeric module if imported a different numeric package.
    """
    global numeric
    numeric = module


def get_numeric_module():
    """
    Get numeric module. Return None if module not present.
    """
    return numeric

