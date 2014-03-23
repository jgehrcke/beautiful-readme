#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Jan-Philip Gehrcke (http://gehrcke.de).
# See LICENSE file for details.


import re
from setuptools import setup


long_description = \
"""Beautiful-readme converts a single README file into a simple, modern, and
mobile-friendly `Bootstrap`_-powered static website.

Resources:

- Documentation_
- GitHub_

.. _Bootstrap: http://getbootstrap.com/
.. _GitHub: http://github.com/jgehrcke/beautiful-readme
.. _Documentation: http://gehrcke.de/beautiful-readme
"""


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('beautifulreadme/beautifulreadme.py').read(),
    re.M
    ).group(1)


setup(
    name = "beautiful-readme",
    packages = ["beautifulreadme"],
    entry_points = {
        "console_scripts": ['beautiful-readme = beautifulreadme.main:main']
        },
    version = version,
    description = "Creates a simple mobile-friendly static website from your README.",
    author = "Jan-Philip Gehrcke",
    author_email = "jgehrcke@googlemail.com",
    url = "http://gehrcke.de/beautiful-readme",
    long_description=long_description,
    keywords = ["readme", "website", "static", "Bootstrap"],
    platforms = ["POSIX", "Windows"],
    install_requires = ["markdown", "docutils"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        ],
    )
