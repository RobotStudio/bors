from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


version = '0.0.1'


setup(
    name='bors',
    packages=['bors', 'bors.envs', 'bors.envs.stocks'],
    version=version,
    description="A highly flexible and extensible service integration framework for scraping the web or consuming APIs.",
    long_description=README,
    classifiers=[],
    keywords='web-scraper api-integrator scraping scraper data-integration data-ingestion',
    author='Bobby',
    author_email='karma0@gmail.com',
    url='https://github.com/RobotStudio/bors',
    license='GPL',
    install_requires=['marshmallow', 'requests'],
)
