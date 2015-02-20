# -*- coding: utf-8 -*-

from __future__ import print_function
from contextlib import contextmanager
import mock

try:
    # for py26
    import unittest2 as unittest
except ImportError:
    import unittest

import sys

sys.path.insert(0, '..')

from clingon import clingon
clingon.TEST = True
clingon.DEBUG = False

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from collections import OrderedDict
except ImportError:
    # for py26
    from ordereddict import OrderedDict


@contextmanager
def captured_output():
    try:
        sys.stdout, sys.stderr = StringIO(), StringIO()
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__

# ---------- here are decorated functions under test -------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@clingon.clize
def clized_default_shorts(p1, p2,
                          first_option='default_value',
                          second_option=5,
                          third_option=[4, 3],
                          last_option=False):
    """Help docstring
    """
    print('%s %s %s %s %s %s' % (p1, p2, first_option, second_option, third_option, last_option))


@clingon.clize(first_option='1', second_option=('2', 's', 'so'))
def clized_spec_shorts(p1, p2,
                       first_option='default_value',
                       second_option=5,
                       third_option=[4, 3],
                       last_option=False):
    if last_option:
        return 12
    print('%s %s %s %s %s %s' % (p1, p2, first_option, second_option, third_option, last_option))


@clingon.clize
def clized_that_raises():
    raise RuntimeError('I just raise')


@clingon.clize
def clized_varargs(p1, p2,
                   option='default_value',
                   *varargs):
    print('%s %s %s %s' % (p1, p2, option, varargs))


def version():
    return '1.2.3'


@clingon.clize
@clingon.set_variables(VERSION=version, message="you can dynamically customize help message !")
def clized_variables(p1, p2, long_name_option='default_value'):
    """Help docstring v{VERSION}
       {message}
    """
    pass

@clingon.clize
@clingon.set_variables(VERSION='1.2.3', message="you can dynamically customize help message !")
def clized_variables_one_short(p1, p2, option='default_value'):
    """Help docstring v{VERSION}
       {message}
    """
    pass


# ---------- end of decorated functions under test --------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestClinngon(unittest.TestCase):

    def test_decorator_multiple_args(self):
        with self.assertRaises(ValueError) as cm:
            clingon.clize(1, 2)
        message = cm.exception.args[0]
        self.assertEqual(message, "This decorator is for a function only")

    def test_decorator_args_not_function(self):
        with self.assertRaises(ValueError) as cm:
            clingon.clize(1)
        message = cm.exception.args[0]
        self.assertEqual(message, "This decorator is for a function only")

    def test_decorator_kwargs_not_sequence(self):
        with self.assertRaises(ValueError) as cm:
            clingon.clize(toto=1)
        message = cm.exception.args[0]
        self.assertEqual(message, "Decorator's keyword 'toto' value must be "
                                               "a string or a tuple of strings, found: 1")

    def test_kwargs(self):

        def clized(*varargs, **keywargs):
            pass

        with self.assertRaises(TypeError) as cm:
            clingon.clize(clized)
        message = cm.exception.args[0]
        self.assertEqual(message, "Keywords parameter '**keywargs' is not allowed")

    def test_bad_spec_option(self):

        def clized(option='default_value'):
            pass

        with self.assertRaises(ValueError) as cm:
            clingon.clize(bad_option='')(clized)
        message = cm.exception.args[0]
        self.assertEqual(message, "This option does not exists so can't be given an alias: bad_option")

    def test_internal_data(self):

        def clized(p1, p2,
                   first_option='default_value',
                   second_option=5,
                   third_option=[4, 3],
                   last_option=False,
                   *varargs):
            """docstring"""
            pass

        ret = clingon.clize(clized)
        self.assertEqual(ret.func.__name__, 'clized')
        self.assertEqual(ret.docstring, "docstring")
        self.assertEqual(ret.reqargs, ['p1', 'p2'])
        self.assertEqual(ret.varargs, 'varargs')
        self.assertDictEqual(ret.options, {
            '--first-option': 'default_value',
            '-f': 'default_value',
            '--second-option': 5,
            '-s': 5,
            '--third-option': [4, 3],
            '-t': [4, 3],
            '--last-option': False,
            '-l': False,
        })
        self.assertDictEqual(ret._options, {
            '--first-option': 'default_value',
            '--second-option': 5,
            '--third-option': [4, 3],
            '--last-option': False,
        })
        self.assertDictEqual(ret.options_aliases, {
            'first_option': ('f',),
            'second_option': ('s',),
            'third_option': ('t',),
            'last_option': ('l',)
        })
        self.assertDictEqual(ret.options_equ, {
            '--first-option': 'first_option',
            '-f': 'first_option',
            '--second-option': 'second_option',
            '-s': 'second_option',
            '--third-option': 'third_option',
            '-t': 'third_option',
            '--last-option': 'last_option',
            '-l': 'last_option'
        })
        self.assertEqual(ret.python_options,
                         OrderedDict([
                             ('first_option', 'default_value'),
                             ('second_option', 5),
                             ('third_option', [4, 3]),
                             ('last_option', False)
                         ]))


@mock.patch('sys.exit')
class TestDeco(unittest.TestCase):
    def test_default_no_option(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2')
        self.assertEqual(out.getvalue(),
                         "p1 p2 default_value 5 [4, 3] False\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_default_first_option(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 --first-option specific_value')
        self.assertEqual(out.getvalue(),
                         "p1 p2 specific_value 5 [4, 3] False\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_default_second_option(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 --second-option 10')
        self.assertEqual(out.getvalue(),
                         "p1 p2 default_value 10 [4, 3] False\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_default_third_option(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 --third-option 16 9')
        self.assertEqual(out.getvalue(),
                         "p1 p2 default_value 5 [16, 9] False\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_default_last_option(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 --last-option')
        self.assertEqual(out.getvalue(),
                         "p1 p2 default_value 5 [4, 3] True\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_default_all_options(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts(
                'p1 p2 --third-option 16 9 --second-option 10 --first-option specific_value --last-option')
        self.assertEqual(out.getvalue(),
                         "p1 p2 specific_value 10 [16, 9] True\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_default_all_options_short(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 -t 16 9 -s 10 -f specific_value -l')
        self.assertEqual(out.getvalue(),
                         "p1 p2 specific_value 10 [16, 9] True\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_option_bad_type(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 --second-option x')
        self.assertEqual(err.getvalue(),
                         "Argument of option --second-option has wrong type (<int> expected)\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_option_short_bad_type(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 -s x')
        self.assertEqual(err.getvalue(),
                         "Argument of option -s has wrong type (<int> expected)\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_option_list_bad_type(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 --third-option 1 y')
        self.assertEqual(err.getvalue(),
                         'Argument 2 of option --third-option has wrong type (<int> expected)\n')
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_spec_option(self, sys_exit):
        with captured_output() as (out, err):
            clized_spec_shorts('p1 p2 -1 specific_value')
        self.assertEqual(out.getvalue(),
                         "p1 p2 specific_value 5 [4, 3] False\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_spec_option_again(self, sys_exit):
        with captured_output() as (out, err):
            clized_spec_shorts('p1 p2 -1 specific_value -so 12')
        self.assertEqual(out.getvalue(),
                         "p1 p2 specific_value 12 [4, 3] False\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_unknown_parameter(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 p3')
        self.assertEqual(err.getvalue(),
                         "usage: test_clingon.py p1 p2 [options] [--help | -?]\n"
                         "Unrecognized parameter or option 'p3'\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_too_few_parameters(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1')
        self.assertEqual(err.getvalue(),
                         "usage: test_clingon.py p1 p2 [options] [--help | -?]\n"
                         "Too few parameters (2 required)\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_duplicate_option(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 -l --last-option')
        self.assertEqual(err.getvalue(),
                         "Option '--last-option' found twice\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_option_missing_value(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('p1 p2 -s')
        self.assertEqual(err.getvalue(),
                         "Option '-s' should be followed by a <int>\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_return_integer(self, sys_exit):
        with captured_output() as (out, err):
            clized_spec_shorts('p1 p2 -l')
        self.assertEqual(out.getvalue(), '')
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(12)

    def test_help_output(self, sys_exit):
        with captured_output() as (out, err):
            clized_default_shorts('-?')
        output = out.getvalue()
        self.assertIn(clized_default_shorts.docstring.strip(), output)
        self.assertIn("Options:\n"
                      "--first-option  | -f <str> (default='default_value')\n"
                      "--second-option | -s <int> (default=5)\n"
                      "--third-option  | -t <list of int> (default=[4, 3])\n"
                      "--last-option   | -l (default=False)\n"
                      "--help          | -? print this help", output)
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_raise_nodebug(self, sys_exit):
        with captured_output() as (out, err):
            clized_that_raises('')
        self.assertEqual(err.getvalue(), "I just raise\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_raise_debug(self, sys_exit):
        clingon.DEBUG = True
        try:
            with captured_output() as (out, err):
                self.assertRaises(RuntimeError, clized_that_raises, '')
        finally:
            clingon.DEBUG = False
        self.assertEqual(err.getvalue(), "I just raise\n")
        self.assertEqual(out.getvalue(), 'clize call parameters: []\n')
        sys_exit.assert_not_called()

    def test_varargs_novararg(self, sys_exit):
        with captured_output() as (out, err):
            clized_varargs('p1 p2 -o 123')
        self.assertEqual(out.getvalue(), "p1 p2 123 ()\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_varargs_varargs(self, sys_exit):
        with captured_output() as (out, err):
            clized_varargs('p1 p2 p3 p4 -o 123 --catched')
        self.assertEqual(out.getvalue(), "p1 p2 123 ('p3', 'p4', '--catched')\n")
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_varargs_too_few_parameters(self, sys_exit):
        with captured_output() as (out, err):
            clized_varargs('p1')
        self.assertEqual(err.getvalue(),
                         "usage: test_clingon.py p1 p2 [varargs] [--option | -o <str> "
                         "(default='default_value')] [--help | -?]\n"
                         "Too few parameters (2 required)\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_version_usage(self, sys_exit):
        with captured_output() as (out, err):
            clized_variables('p1')
        self.assertEqual(err.getvalue(),
                         "usage: test_clingon.py p1 p2 [options] [--help | -?]\n"
                         "Too few parameters (2 required)\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_variables_help_output(self, sys_exit):
        with captured_output() as (out, err):
            clized_variables('-?')
        output = out.getvalue()
        doc = clized_default_shorts.docstring.strip().format(VERSION='1.2.3',
                                                           message="you can dynamically customize help message !")
        self.assertIn(doc, output)
        self.assertIn("Options:\n"
                      "--long-name-option | -l <str> (default='default_value')\n"
                      "--version          | -V print version (1.2.3)\n"
                      "--help             | -? print this help", output)
        self.assertEqual(err.getvalue(), '')
        sys_exit.assert_called_with(0)

    def test_version_one_short_usage(self, sys_exit):
        with captured_output() as (out, err):
            clized_variables_one_short('p1')
        self.assertEqual(err.getvalue(),
                         "usage: test_clingon.py p1 p2 [--option | -o <str> "
                         "(default='default_value')] [--version | -V] [--help | -?]\n"
                         "Too few parameters (2 required)\n")
        self.assertEqual(out.getvalue(), '')
        sys_exit.assert_called_with(clingon.SYSTEM_EXIT_ERROR_CODE)

    def test_version_parameter(self, sys_exit):
        with captured_output() as (out, err):
            clized_variables('-V')
        self.assertEqual(out.getvalue(), '')
        error = err.getvalue()
        self.assertIn('version 1.2.3 from', error)
        sys_exit.assert_called_with(0)


if __name__ == '__main__':
    unittest.main()
