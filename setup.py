#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import pkg_resources
import setuptools
import setuptools.command.build_py
import setuptools.command.sdist


__version__ = os.environ.get('PACKAGE_VERSION')
if __version__ is None:
    try:
        __version__ = pkg_resources.get_distribution('wg_srle').version
    except pkg_resources.DistributionNotFound:
        __version__ = 'master'


setuptools.setup(
    name='wg-srle',
    version=__version__,
    description=(
        'SRLE implementation'
    ),
    license='AS-IS',
    author='Alon Bar-Lev',
    author_email='alon.barlev@gmail.com',
    url='https://github.com/alonbl/wg-srle',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            (
                'wg-srle='
                'wg_srle.__main__:main'
            ),
        ],
    },
)
