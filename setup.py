#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Bobby",
    author_email='karma0@gmail.com',

    name='bors',
    version='0.3.6',
    url='https://github.com/karma0/bors',
    license="GNU General Public License v3",

    long_description=readme + '\n\n' + history,
    keywords='bors web-scraper api-integrator scraping scraper '
             'data-integration data-ingestion',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],

    description="A highly flexible and extensible service integration framework for scraping the web or consuming APIs",

    entry_points={
        'console_scripts': [
            'bors=bors.cli:main',
        ],
    },
    install_requires=requirements,

    packages=find_packages(exclude=['tests', 'docs']),
    setup_requires=setup_requirements,
    include_package_data=True,
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
)
