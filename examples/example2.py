# -*- coding: utf-8 -*-

from __future__ import print_function
from clingon import clingon
clingon.DEBUG = True

# the decorator has parameters
# each option of the decorated function
# will have its default short alias overridden by the decorator
# shortcuts (you can define more than one for each parameter)

# Also, a second decorator allows to define variables that can be
# used to generate the help text from your docstring.
# Special variable CLINGON_PREFIX defines the environ prefix that
# can be used to override options defaults.
# In this example, you can export EXAMPLE2_THIRD_OPTION='[16, 9]'
# to redefine the default value of option third_option.


# version can be a string or a function
def version():
    return '1.2.3'

@clingon.clize(first_option='1', second_option=('2', 's', 'so'))
@clingon.set_variables(VERSION=version,
                       message="you can dynamically customize help message !",
                       CLINGON_PREFIX="EXAMPLE2")
def my_func(p1, p2,
            first_option='default_value',
            second_option=5,
            third_option=[4, 3],
            last_option=False):
    """Help docstring. v{VERSION}
       {message}
    """
    if last_option:
        raise RuntimeError("Test of DEBUG")
    print('%s %s %s %s %s %s' % (p1, p2, first_option, second_option, third_option, last_option))
