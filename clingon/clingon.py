#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLINGON
Command Line INterpreter Generator for pythON
Compatible python 2 and 3
(c) François Vincent, https://github.com/francois-vincent
"""

from __future__ import print_function, absolute_import
from future.utils import listitems, iteritems
from past.builtins import basestring

from collections import Sequence

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import inspect
import os
import sys
import textwrap

__version__ = '0.1.3'
DEBUG = False
TEST = False
SYSTEM_EXIT_ERROR_CODE = 1


class ClingonError(RuntimeError):
    pass


class RunnerError(ClingonError):
    pass


class RunnerErrorWithUsage(ClingonError):
    pass


class Clizer(object):
    """
    This virtual class extracts args off the run() method of any derived subclass
    Then it extracts cmd line arguments and launches run() with matched args
    """
    _help_options = ('--help', '-?')
    _version_options = ('--version', '-V')

    @staticmethod
    def _write_error(*args, **kwargs):
        sys.stderr.write(kwargs.get('sep', ' ').join(args) + kwargs.get('end', '\n'))

    @staticmethod
    def _get_type(arg):
        return type(arg).__name__

    @classmethod
    def _sys_exit(cls, code=SYSTEM_EXIT_ERROR_CODE):
        if cls.SYSTEM_EXIT:
            if type(code) is not int:
                code = 0
            if DEBUG:
                print("Exit with code %d" % code)
            sys.exit(code)
        return code

    @classmethod
    def check_deco_parameters(cls, *args, **kwargs):
        if (args and kwargs) or len(args) > 1:
            raise ValueError("This decorator is for a function only")
        if args and not inspect.isfunction(args[0]):
            raise ValueError("This decorator is for a function only")
        if kwargs:
            for k, v in kwargs.items():
                if not isinstance(v, Sequence):
                    raise ValueError(
                        "Decorator's keyword '%s' value must be a string or a tuple of strings, found: %s" % (k, v))

    def __init__(self, func):
        self.func = func
        self.docstring = func.__doc__
        self.file = inspect.getfile(func)
        self.variables = getattr(func, 'variables', {})
        argspec = inspect.getargspec(self.func)
        # do not allow keywords
        if argspec.keywords:
            raise TypeError("Keywords parameter '**%s' is not allowed" % argspec.keywords)
        defaults = argspec.defaults or ()
        # get varargs
        self.varargs = argspec.varargs
        # get required args as a list and optional args as a dict (with default values)
        nb_args, len_defaults = len(argspec.args), len(defaults)
        self.reqargs = argspec.args[:nb_args - len_defaults]
        options = OrderedDict(zip((x.lower() for x in argspec.args[nb_args - len_defaults:]), defaults))
        for k, v in iteritems(options):
            if v is True:
                raise ValueError("Default value for boolean %r must be 'False'" % k)
            # make a copy of options for later call of user's decorated function
        self.python_options = OrderedDict(options)
        # make an equivalence dict from line cmd style (--file-name) to python style (file_name) args
        self.options_equ = dict([('-' + x if len(x) == 1 else '--' + '-'.join(x.split('_')), x) for x in options])
        # make a dict of cmd line style arg names to their types
        self.options = OrderedDict(
            [('-' + x if len(x) == 1 else '--' + '-'.join(x.split('_')), options[x]) for x in options])
        # take a copy of original (no aliases yet) optional args for print_help()
        self._options = OrderedDict(self.options)
        # create automatic short options aliases from long options
        self.options_aliases = getattr(self, 'options_aliases', {})
        mismatch = set(self.options_aliases) - set(options)
        if mismatch:
            raise ValueError("This option does not exists so can't be given an alias: " + mismatch.pop())
        for k in options:
            if k not in self.options_aliases and len(k) > 1:
                self.options_aliases[k] = (k[0],)
                # inject aliases into dicts
        for x, t in options.items():
            if x in self.options_aliases:
                alias = self.options_aliases[x]
                if isinstance(alias, basestring):
                    alias = self.options_aliases[x] = (alias,)
                new_alias = []
                for a in alias:
                    k = '-' + a
                    if k in self.options or k in self._version_options:
                        # silently ignore duplicate short alias
                        continue
                    self.options[k] = t
                    self.options_equ[k] = x
                    new_alias.append(a)
                self.options_aliases[x] = new_alias

    def _eval_global(self):
        for k, v in listitems(self.variables):
            self.variables[k] = v() if hasattr(v, '__call__') else v

    def _get_global(self, key):
        return self.variables.get(key)

    def _print_version(self):
        source = os.path.dirname(self.file)
        source = ' from ' + source if source else ''
        Clizer._write_error('version %s%s (Python %s)' % (self._get_global('VERSION'), source,
                                                          sys.version.split()[0]), help='')

    def start(self, param_string=None):
        optargs = {}
        reqargs, varargs = [], []
        # first, search cmd line options and their args
        # and collect them in optargs.
        # along this process, required and optional args are also collected
        # in reqargs and varargs
        if param_string is None:
            argv = sys.argv[1:]
        else:
            import shlex

            argv = shlex.split(param_string)
        self._eval_global()
        i = 0
        while i < len(argv):
            x = argv[i]
            if x in self._help_options:
                self._print_help()
                return
            if x in self._version_options and self._get_global('VERSION'):
                self._print_version()
                return
            if x in self.options:
                if self.options_equ[x] in optargs:
                    raise RunnerError("Option '%s' found twice" % x)
                if isinstance(self.options[x], (list, tuple)):
                    argpos = i
                    optargs[self.options_equ[x]] = []
                    i += 1
                    while i < len(argv) and argv[i] not in self.options:
                        try:
                            optargs[self.options_equ[x]].append(type(self.options[x][0])(argv[i]))
                        except ValueError:
                            raise RunnerErrorWithUsage("Argument %d of option %s has wrong type (%s expected)" %
                                                       (i - argpos, x, self._format_type(self.options[x][0])))
                        except IndexError:
                            optargs[self.options_equ[x]].append(argv[i])
                        i += 1
                    if not len(optargs[self.options_equ[x]]):
                        raise RunnerErrorWithUsage("Option '%s' should be followed by a list of %s" %
                                                   (x, self._format_type(self.options[x][0])))
                    if len(self.options[x]) and len(optargs[self.options_equ[x]]) != len(self.options[x]):
                        raise RunnerErrorWithUsage("Option '%s' should be followed by exactly %d parameters, "
                                                   "found %d" %
                                                   (x, len(self.options[x]), len(optargs[self.options_equ[x]])))
                elif type(self.options[x]) is bool:
                    optargs[self.options_equ[x]] = True
                    i += 1
                else:
                    i += 1
                    if i >= len(argv) or argv[i] in self.options:
                        raise RunnerErrorWithUsage("Option '%s' should be followed by a %s" %
                                                   (x, self._format_type(self.options[x])))
                    try:
                        optargs[self.options_equ[x]] = type(self.options[x])(argv[i])
                    except ValueError:
                        raise RunnerErrorWithUsage("Argument of option %s has wrong type (%s expected)" %
                                                   (x, self._format_type(self.options[x])))
                    i += 1
            else:
                if x.startswith('-'):
                    raise RunnerErrorWithUsage("Unrecognized option '%s'" % argv[i])
                elif len(reqargs) < len(self.reqargs):
                    reqargs.append(argv[i])
                elif self.varargs:
                    varargs.append(argv[i])
                else:
                    raise RunnerErrorWithUsage("Unrecognized parameter '%s'" % argv[i])
                i += 1
        if self.reqargs and len(reqargs) < len(self.reqargs):
            raise RunnerErrorWithUsage("Too few parameters (%d required)" % len(self.reqargs))
            # merge required, optional args and options in allargs
        options = OrderedDict(self.python_options)
        options.update(optargs)
        allargs = reqargs
        allargs.extend(options.values())
        allargs.extend(varargs)
        if DEBUG:
            print('clize call parameters:', allargs)
            # all parameters are filled
        return self.func(*allargs)

    def __call__(self, param_string=None):
        try:
            code = self.start(param_string)
        except RunnerErrorWithUsage as e:
            self._print_usage(file=sys.stderr)
            Clizer._write_error(str(e), help='')
        except RunnerError as e:
            Clizer._write_error(str(e))
        except Exception as e:
            Clizer._write_error(str(e), help='')
            if DEBUG:
                raise
        else:
            return self.__class__._sys_exit(code)
        return self.__class__._sys_exit()

    def _format_type(self, arg, post=''):
        if isinstance(arg, list):
            try:
                return '<list of %s>' % self._get_type(arg[0]) + post
            except IndexError:
                return '<list of str>' + post
        elif isinstance(arg, bool):
            return ''
        else:
            return '<%s>' % self._get_type(arg) + post

    def _format_aliases(self, option):
        option = self.options_equ[option]
        if option in self.options_aliases and self.options_aliases[option]:
            return '| -' + ' | -'.join(self.options_aliases[option]) + ' '
        return ''

    def _format_option(self, option, opt_type, width=1):
        option_format = "{option:{width}} {shorts}{opt_type}{default}"
        option_dict = dict(
            option=option,
            width=width,
            shorts=self._format_aliases(option),
            opt_type=self._format_type(opt_type, ' '),
            default='(default=%r)' % opt_type
        )
        return option_format.format(**option_dict)

    def _print_usage(self, prepend='usage: ', file=sys.stdout):
        usage_format = "{prepend}{basename} {reqargs}{varargs}{options}{version}{help}"
        usage_dict = dict(
            prepend=prepend,
            basename=(os.path.basename(self.file)),
            reqargs=' '.join(self.reqargs) + ' ',
            varargs='[varargs] ' if self.varargs else '',
            version='[' + ' | '.join(self._version_options) + '] ' if self._get_global('VERSION') else '',
            help='[' + ' | '.join(self._help_options) + ']'
        )
        many_options = False
        if len(self._options) == 1 and len(list(self._options)[0]) < 9:
            # if only one option with a 'short' name: put everything in one line
            usage_dict.update(
                options='[' + self._format_option(*listitems(self._options)[0]) + '] ',
            )
        elif len(self._options) > 0:
            # else defer options description at the end of help output
            usage_dict.update(
                options='[options] ',
                version=''
            )
            many_options = True
        else:
            usage_dict.update(
                options='',
            )
        print(usage_format.format(**usage_dict), file=file)
        return many_options

    def _print_help(self):
        """
        Help is automatically generated from the __doc__ of the subclass if present
        and from the names of the args of run(). Therefore args names selection
        is more important than ever here !
        """
        options = self._print_usage('\n  ', file=sys.stdout)
        if self.docstring:
            print()
            doc_string = self.docstring.format(**self.variables)
            for doc in doc_string.split('\n'):
                doc = doc.strip()
                if len(doc) > 2:
                    print(textwrap.fill(textwrap.dedent(doc).strip(),
                                        width=80, initial_indent='  ',
                                        subsequent_indent='   '))
        print()
        if options:
            print('Options:')
            width = max(len(k) for k in self._options)
            for x, t in self._options.items():
                print(self._format_option(x, t, width))
            if self._get_global('VERSION'):
                print('{0:{1}}'.format(self._version_options[0], width), end=' ')
                print('| ' + ' | '.join(self._version_options[1:]), 'print version',
                      '(%s)' % self._get_global('VERSION'))
            print('{0:{1}}'.format(self._help_options[0], width), end=' ')
            print('| ' + ' | '.join(self._help_options[1:]), 'print this help')
            print()


def clize(*args, **kwargs):
    """
    Decorator has 2 usages:
    @clize
    def decorated(params):
       ...
    optional parameters aliases are autogenerated, conflicts are silently ignored

    @clize(aliases)
    def decorated(params)
       ...
    where aliases is a dictionary, key=python parameter of decorated function, value=tuple of aliases
    """

    kwargs = dict((k.lower(), v) for k, v in iteritems(kwargs))

    class mycli(Clizer):
        SYSTEM_EXIT = True
        options_aliases = kwargs

    mycli.check_deco_parameters(*args, **kwargs)

    def runner(function):
        return mycli(function) if TEST else mycli(function)()

    if args:
        return runner(args[0])
    else:
        return runner


def set_variables(**kwargs):
    def f(x):
        x.variables = kwargs
        return x

    return f


def make_script(python_script, target_path='', target_name='', user=False, make_link=False,
                force=False, remove=False, no_check_shebang=False, no_check_path=False):
    """v{VERSION}
    This script makes a command line script out of a python file.
    For example, 'clingon script.py' will copy or symlink script.py
    (without the .py extension) to:
    - <python-exe-path>/script (default),
    - <target-path>/script if --target-path is specfied,
    - ~/bin/script if --user is specified,
    and then set the copy / symlink as executable.
    """
    if user and target_path:
        raise RunnerErrorWithUsage("You cannot specify --path and --user at the same time")
    source = os.path.abspath(python_script)
    dest_dir = os.path.normpath(os.path.expanduser('~/bin' if user else target_path or os.path.dirname(sys.executable)))
    target = os.path.join(dest_dir, target_name if target_name
    else os.path.splitext(os.path.basename(source))[0])
    target_exists = os.path.exists(target)
    if remove:
        if target_exists:
            os.unlink(target)
            print("Script '%s' removed" % target)
        else:
            print("Script '%s' not found, nothing to do" % target)
        return
    if not os.path.exists(source):
        raise RunnerError("Could not find source '%s', aborting" % source)
    if DEBUG:
        print('Source, target:', source, target)

    if target_exists:
        def same_file_same_type(source, target):
            if os.path.islink(target):
                return make_link and os.path.samefile(source, target)
            else:
                return not make_link and (open(source, 'rb').read() == open(target, 'rb').read())

        if same_file_same_type(source, target):
            print("Target '%s' already created, nothing to do" % target)
            return
        elif not force:
            raise RunnerError("Target '%s' already exists, aborting" % target)

    if not os.path.isdir(dest_dir):
        # Create directory but only if father dir exists and user has rights
        if os.access(os.path.basename(dest_dir), os.W_OK):
            os.system("mkdir %s" % dest_dir)
        else:
            raise RunnerError("Target folder '%s' does not exist, and cannot create it, aborting" % dest_dir)

    if not no_check_shebang:
        # Check that file starts with python shebang (#!/usr/bin/env python)
        first_line = open(source).readline()
        if not ('#!' in first_line and 'python' in first_line):
            raise RunnerError("Your script's first line should start with '#!' and contain 'python', aborting")

    # Now it's time to copy or symlink file
    if target_exists:
        os.unlink(target)
    import stat

    perms = stat.S_IXUSR | stat.S_IXGRP
    if os.getuid() == 0:
        perms |= stat.S_IXOTH
    if make_link:
        st = os.stat(source)
        if st.st_mode & perms != perms:
            os.chmod(source, st.st_mode | perms)
        os.symlink(source, target)
        st = os.stat(target)
        os.chmod(target, st.st_mode | perms)
        print('Script %s has been symlinked to %s' % (source, target))
    else:
        import shutil

        shutil.copyfile(source, target)
        st = os.stat(target)
        os.chmod(target, st.st_mode | perms)
        print('Script %s has been copied to %s' % (source, target))
        # check PATH and advise user to update it if relevant
    path_env = os.environ.get('PATH')
    if not no_check_path and (not path_env or dest_dir not in path_env):
        print("Please add your local bin path [%s] to your environment PATH" % dest_dir)


def clingon_script():
    return clize(make_link=('m', 's', 'l'), force=('f', 'o'), target_path='p', target_name='n')(
        set_variables(VERSION=__version__)(make_script))


if __name__ == '__main__':
    clingon_script()
