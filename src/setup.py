# Individual-Based Modeling (IBM)
#
# Created on October 12, 2019
#
# Authors:
#   Ralph Florent <r.florent@jacobs-university.de>
#   Davi Tavares <davi.tavares@leibniz-zmt.de>
#   Agostino Merico <a.merico@jacobs-university.de>
#
# Setup to bootstrap your next Python project

# ==============================================================================
# START: Setup
# ==============================================================================

# -*- coding: utf-8 -*-
# Learn more: https://github.com/navdeep-G/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ve-ibm',
    version='0.1.0',
    description='Virtual Environment for Individual-Based Modeling',
    long_description=readme,
    author='Ralph Florent',
    author_email='r.florent@jacobs-university.de',
    url='https://github.com/systemsecologygroup/BirdsABM',
    license=license,
    packages=find_packages(exclude=('assets', 'tests'))
)

# ==============================================================================
# END: Setup
# ==============================================================================