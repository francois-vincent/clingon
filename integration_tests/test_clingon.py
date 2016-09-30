# encoding: utf-8

from . import ROOTDIR

import os.path

import pytest
from simply.platform import platform_setup


clingon_path = os.path.dirname(ROOTDIR)

conf = dict(
    backend='docker',
    frontend='debian',
    parameters='-v {0}:/root/python/clingon'.format(clingon_path)
)


@pytest.mark.parametrize("image", ('debian8',))
def test_install_clingon(image):
    conf['image'] = image
    with platform_setup(conf) as platform:
        platform.execute('cd /root/python/clingon && python setup.py install', shell=True)
        assert platform.execute('which clingon').strip() == '/usr/local/bin/clingon'
        assert 'version' in platform.execute('clingon -V', stdout_only=False).stderr


@pytest.mark.parametrize("image", ('debian8',))
def test_install_script(image):
    conf['image'] = image
    with platform_setup(conf) as platform:
        platform.execute('cd /root/python/clingon && python setup.py install', shell=True)
        platform.execute('cd /root/python/clingon/examples && clingon zipcomment.py', shell=True)
        # zipcomment has been installed in the same directory than python
        assert platform.execute('which zipcomment') == platform.execute('which python').replace('python', 'zipcomment')
        assert platform.execute('which zipcomment | xargs ls -al', shell=True).startswith('-rwxr-xr-x')


@pytest.mark.parametrize("image", ('debian8',))
def test_install_symlink(image):
    conf['image'] = image
    with platform_setup(conf) as platform:
        platform.execute('cd /root/python/clingon && python setup.py install', shell=True)
        platform.execute('cd /root/python/clingon/examples && clingon zipcomment.py -s', shell=True)
        # zipcomment has been installed in the same directory than python
        assert platform.execute('which zipcomment') == platform.execute('which python').replace('python', 'zipcomment')
        print(platform.execute('which zipcomment | xargs ls -al', shell=True))
        assert platform.execute('which zipcomment | xargs ls -al', shell=True).startswith('lrwxrwxrwx')


@pytest.mark.parametrize("image", ('debian8',))
def test_install_symlink_then_script(image):
    conf['image'] = image
    with platform_setup(conf) as platform:
        platform.execute('cd /root/python/clingon && python setup.py install', shell=True)
        platform.execute('cd /root/python/clingon/examples && clingon zipcomment.py -s', shell=True)
        # clingon do not allow to overwrite an existing file (the symlink)
        assert not platform.execute('cd /root/python/clingon/examples && clingon zipcomment.py',
                                shell=True, status_only=True)
        # unless it is explicitly forced to
        assert platform.execute('cd /root/python/clingon/examples && clingon zipcomment.py -f',
                                shell=True, status_only=True)
        assert platform.execute('which zipcomment | xargs ls -al', shell=True).startswith('-rwxr-xr-x')
