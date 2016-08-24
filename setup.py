#!/usr/bin/env python
import os
from setuptools import setup, find_packages


README = os.path.join(os.path.dirname(__file__), 'README.md')

# when running tests using tox, README.md is not found
try:
    with open(README) as file:
        long_description = file.read()
except Exception:
    long_description = ''


setup(
    name='blinktrade',
    version='0.1.1',
    description='A python client for BlinkTrade Bitcoin Platform',
    long_description=long_description,
    url='https://github.com/vinicius-ronconi/blinktrade',
    author='Vinicius Ronconi',
    author_email='vinicius.ronconi@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='blinktrade blinktrade v3 client bitcoin exchange foxbit chilebit surbitcoin vbtc urbubit',
    packages=find_packages(),
    install_requires=['requests'],
    extras_require={
        'test': ['coverage', 'mock', 'nose'],
    },
)
