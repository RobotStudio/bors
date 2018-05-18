"""Setup script to package project"""

import os
from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()

VERSION = '0.0.1'


setup(
    name='bors',
    packages=[
        'bors',
        'bors.api',
        'bors.api.adapter',
        'bors.app',
        'bors.common',
        'bors.generics',
        'bors.strategies',
        'bors.algorithms',
    ],
    version=VERSION,
    description="A highly flexible and extensible service integration "
    "framework for scraping the web or consuming APIs.",
    long_description=README,
    classifiers=[],
    keywords="web-scraper api-integrator scraping scraper data-integration"
    "data-ingestion",
    author='Bobby',
    author_email='karma0@gmail.com',
    url='https://github.com/RobotStudio/bors',
    license='GPL',
    install_requires=['marshmallow', 'requests', 'socketclusterclient'],
)
