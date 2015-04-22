# -*- coding: utf-8 -*-


from clingon import clingon
from clingon.utils import AreYouSure
import os.path

@clingon.clize
def copy(source, dest, force=False):
    if (os.path.exists(dest) and
        (force or AreYouSure(all_yes=None, all_no=None)('%s already exists, replace it' % dest))):
        print("replacing %s" % dest)
