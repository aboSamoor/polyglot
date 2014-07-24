#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='polyglot',
    version='"14.11"',
    description='Polyglot is a natuaral language pipeline that supports massive multilingual applications.',
    long_description=readme + '\n\n' + history,
    author='Rami Al-Rfou',
    author_email='rmyeid@gmail.com',
    url='https://github.com/aboSamoor/polyglot',
    packages = ['polyglot',
                'polyglot.detect',
                'polyglot.tokenize',
                'polyglot.mapping'],
    scripts=['polyglot/polyglot'],
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='polyglot',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
