========
Usage
========

To use clingon in a project::

    from clingon import clingon

    @clingon.clize
    def your_function(p1, p2,
                      first_option='default_value',
                      second_option=5,
                      third_option=[4, 3],
                      last_option=False):
        """Help docstring
        """
