#!/usr/bin/env python

from clingon import clingon
import glob
import os
import time
import zipfile


@clingon.clize(clear='C', list_members=('l', 'm'), time_show=('t', 's'))
def toto(arch_name, comment='', clear=False, read_comment=False, list_members=False, time_show=False):
    """ Small utility for testing zip file comment modification
        without changing file modification time.
    """
    if comment and clear:
        clingon.RunnerError("You cannot specify --comment and --clear together")
    z = None
    # if archive does not exist, create it with up to 3 files from current directory
    if not os.path.isfile(arch_name):
        print "Creating archive", arch_name
        z = zipfile.ZipFile(arch_name, 'w')
        for f in [x for x in glob.iglob('*.*') if not x.endswith('.zip')][:3]:
            print "  Add file %s to %s" % (f, arch_name)
            z.write(f)
    if comment:
        mtime = os.path.getmtime(arch_name)
        if not z:
            z = zipfile.ZipFile(arch_name, 'a')
        z.comment = comment
    if z:
        z.close()
        if comment:
            os.utime(arch_name, (time.time(), mtime))
    if read_comment:
        z = zipfile.ZipFile(arch_name, 'r')
        print "Comment:", z.comment, len(z.comment)
    if list_members:
        z = zipfile.ZipFile(arch_name, 'r')
        print "Members:", z.namelist()
    if time_show:
        print "Access time:", time.ctime(os.path.getatime(arch_name))
        print "Modif time:", time.ctime(os.path.getmtime(arch_name))
