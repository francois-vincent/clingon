# -*- coding: utf-8 -*-

from clingon import clingon
from clingon.utils import AreYouSure
import os.path


@clingon.clize
def copy(source, force=False, *dest):
    ays = AreYouSure(output='stderr')
    for d in dest:
        if os.path.exists(d) and (force or ays('%s already exists, replace it' % d)):
            print("replacing %s" % d)
