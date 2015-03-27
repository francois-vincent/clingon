#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clingon import clingon
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = ['future', 'wheel']
test_requirements = ['mock', 'coverage', 'nose', 'nose-cov', 'codecov']

# Add Python 2.6 specific dependencies
if sys.version_info[:2] < (2, 7):
    test_requirements.append('unittest2')


setup(
    name='clingon',
    version=clingon.__version__,
    description="Command Line INterpreter Generator for pythON",
    long_description=history + '\n\n',
    author="François Vincent",
    author_email='francois.vincent01@gmail.com',
    url='https://github.com/francois-vincent/clingon',
    packages=[
        'clingon',
    ],
    package_dir={'clingon':
                 'clingon'},
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        ':python_version=="2.6"': ['ordereddict'],
    },
    license="BSD",
    zip_safe=False,
    keywords='cli',
    classifiers=[
        # 'Development Status ::  3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Environment :: Console',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={'console_scripts': [
        'clingon = clingon.clingon:clingon_script',
    ]},
)
