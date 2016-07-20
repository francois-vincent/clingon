# encoding: utf-8

from __future__ import print_function
from clingon import clingon

# comment/uncomment lines 10 and 12 to change defaults file definition


@clingon.clize
# @clingon.set_variables(DEFAULTS_FILE='defaults.json')
def clized_default_shorts(p1, p2,
                          defaults_file='defaults.yml',
                          first_option='default value',
                          second_option=5,
                          third_option=[4, 3],
                          last_option=False):
    """Help docstring
    found defaults in {defaults_path_file}
    """
    print('%s %s %s %s %s %s' % (p1, p2, first_option, second_option, third_option, last_option))
