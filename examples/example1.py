# -*- coding: utf-8 -*-

from __future__ import print_function
from clingon import clingon

# the decorator has no parameter.
# each option of the decorated function
# receives a default shortcut that is the first letter of its name.
# in case of conflict between 2 parameters with same first letter,
# an arbitrary choice is made and one of the parameter will
# not have a shortcut

@clingon.clize
def clized_default_shorts(p1, p2,
                          first_option='default_value',
                          second_option=5,
                          third_option=[4, 3],
                          last_option=False):
    """Help docstring
    """
    print('%s %s %s %s %s %s' % (p1, p2, first_option, second_option, third_option, last_option))
