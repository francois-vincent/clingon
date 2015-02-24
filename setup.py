#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = ['future', 'wheel']
test_requirements = ['mock', 'coverage', 'nose', 'nose-cov', 'codecov']

# Add Python 2.6 specific dependencies
if sys.version_info[:2] < (2, 7):
    test_requirements.append('unittest2')
    requirements.append('ordereddict')


setup(
    name='clingon',
    version='0.1.1',
    description="Command Line INterpreter Generator for pythON",
    long_description=readme + '\n\n' + history,
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
    license="BSD",
    zip_safe=False,
    keywords='clingon',
    classifiers=[
        # 'Development Status ::  3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Desktop Environment',
        'Topic :: System :: Shells',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
