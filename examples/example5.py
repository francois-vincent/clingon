# encoding: utf-8

from __future__ import print_function
from clingon import clingon

# comment/uncomment/change lines 10 and 12 to explore options file definition


@clingon.clize
@clingon.set_variables(OPTIONS_FILE='options.py')
def clized_default_shorts(p1, p2,
                          options_file='',
                          first_option='default value',
                          second_option=5,
                          third_option=[4, 3],
                          last_option=False):
    """Help docstring
    found options in {options_file_path}
    """
    print('%s %s %s %s %s %s' % (p1, p2, first_option, second_option, third_option, last_option))
