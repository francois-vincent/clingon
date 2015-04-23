# -*- coding: utf-8 -*-

from contextlib import contextmanager
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@contextmanager
def captured_output():
    try:
        sys.stdout, sys.stderr = StringIO(), StringIO()
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__

