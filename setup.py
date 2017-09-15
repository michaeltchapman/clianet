#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import clianet 


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

packages = [
    'clianet',
    'clianet.drivers',
]

data_files = []
dirs = os.listdir('playbooks')
for d in dirs:
    files = os.listdir('playbooks/' + d)
    files = [ 'playbooks/'+d+'/'+f for f in files ]
    data_files.append(('usr/share/clianet/playbooks/'+d , files))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

requires = [
]

classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Libraries :: Python Modules',
]
 
setup(
    name='clianet',
    version=clianet.__version__,
    description='Cross vendor CLI for common ansible networking tasks.',
    long_description=readme,
    packages=packages,
    data_files=data_files,
    install_requires=requires,
    entry_points='''
    [console_scripts]
    clianet=clianet.core:main
    ''',
    author=clianet.__author__,
    author_email='michapma@redhat.com',
    url='https://github.com/michaeltchapman/clianet',
    license='MIT',
    classifiers=classifiers,
)
