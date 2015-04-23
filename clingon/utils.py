# -*- coding: utf-8 -*-

from builtins import input as user_input
import inspect
import sys


def auto_update_attrs_from_kwargs(method):
    """ this decorator will update the attributes of an
     instance object with all the kwargs of the decorated
     method, updated with the kwargs of the actual call.
     This saves you from boring typing:
     self.xxxx = xxxx
     self.yyyy = yyyy
     ...
     in the decorated method (typically __init__)
    """
    def wrapped(self, **kwargs):
        # method signature introspection
        argspec = inspect.getargspec(method)
        defaults = argspec.defaults or ()
        nb_args, nb_defaults = len(argspec.args), len(defaults)
        # construct a dict of method's keyword arguments
        options = dict(zip(argspec.args[nb_args - nb_defaults:], defaults))
        # update it with actual keyword arguments
        options.update(kwargs)
        # update attributes of instance
        self.__dict__.update(options)
        method(self, **kwargs)
    return wrapped


class AreYouSure(object):
    """This class implements a binary (True or False) oracle
       with the capacity to lock its state to be always True
       or always False.
    """
    @auto_update_attrs_from_kwargs
    def __init__(self, message='Are you sure', output='stdout',
                 yes=('yes', 'y'), yes_ignore_case=True,
                 yes_default='no', default='default',
                 all_yes=('ALL',), all_no=('NONE',), all_ignore_case=False):
        self.reset_all()
        if self.yes_default in self.yes:
            self.expect = ','.join(self.yes) + '(%s)' % self.default
        else:
            self.expect = ','.join(self.yes) + ',%s(%s)' % (self.yes_default, self.default)
        if self.all_yes:
            self.expect += ',' + ','.join(self.all_yes)
        if self.all_no:
            self.expect += ',' + ','.join(self.all_no)

    def reset_all(self):
        self.all_yes_locked = False
        self.all_no_locked = False

    def __call__(self, message=None, input=None):
        if self.all_yes_locked:
            return True
        if self.all_no_locked:
            return
        message = self.message if message is None else message
        output = sys.stdout if self.output == 'stdout' else sys.stderr
        output.write('%s [%s] ? ' % (message, self.expect))
        rep = user_input() if input is None else input
        all_rep = rep.lower() if self.all_ignore_case else rep
        if self.all_yes and all_rep in self.all_yes:
            self.all_yes_locked = True
            return True
        if self.all_no and all_rep in self.all_no:
            self.all_no_locked = True
            return
        rep = rep or self.yes_default
        if (rep.lower() if self.yes_ignore_case else rep) in self.yes:
            return True
