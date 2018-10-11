#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script"""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'dataclasses',
    'marshmallow',
    'requests',
    'urllib3',
]

test_requirements = [
    'pytest',
    'tox',
    'coverage',
    'pytest-cov',
]

setup_requirements = ['pytest-runner', ]


setup(
    name='bors',
    version='0.3.6',
    description="A highly flexible and extensible service integration framework for scraping the web or consuming APIs",
    long_description=readme + '\n\n' + history,
    author="Bobby",
    author_email='bobby@robot.studio',
    url='https://github.com/RobotStudio/bors',
    packages=find_packages(exclude=['tests', 'docs']),
    package_dir={'bors': 'bors'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='web-scraper api-integrator scraping scraper data-integration '
             'data-ingestion bors',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
