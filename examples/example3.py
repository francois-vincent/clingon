# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
sys.path.insert(0, '..')
from clingon import clingon

clingon.DEBUG = True

# This example shows how to use the variable parameter.
# Used together with required parameters, this allows
# to have as many parameters as one like, with a lower limit.
# But one cannot yet set an upper limit.
# Beware that variable parameter can be a catchall for
# unrecognized (mistyped) options.

@clingon.clize
def my_func(p1, p2,
            first_option='default_value',
            second_option=5,
            third_option=[4, 3],
            last_option=False,
            *args):
    """Help docstring
    """
    print('%s %s %s %s %s %s %s' % (p1, p2, args, first_option, second_option, third_option, last_option))
