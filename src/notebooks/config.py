#!/usr/bin/env python
#
# Individual-Based Modeling (IBM)
#
# Created on October 12, 2019
#
# Authors:
#   Ralph Florent <r.florent@jacobs-university.de>
#   Davi Tavares <davi.tavares@leibniz-zmt.de>
#   Agostino Merico <a.merico@jacobs-university.de>
#
# Configuration before initialization

# ==============================================================================
# START: Config
# ==============================================================================

# -*- coding: utf-8 -*-

import os
import sys
import yaml
import shutil
import warnings
import matplotlib.pyplot as plotter # plotter
import matplotlib.pylab as pylab

# TODO: plotter, env, sys

# Default parameters for the graphs
pylab.rcParams['figure.figsize'] = (11, 6.5)
pylab.rcParams['axes.titlesize'] = 18.0
pylab.rcParams['xtick.labelsize'] = 12
pylab.rcParams['ytick.labelsize'] = 12
pylab.rcParams['legend.fontsize'] = 12
pylab.rcParams['axes.labelsize'] = 12
pylab.rcParams['mathtext.fontset'] = 'stix'
pylab.rcParams['font.family'] = 'STIXGeneral'

def init():
    plotter.ioff() # turn off interactive plotting mode
    warnings.filterwarnings('ignore') # turn off warnings


def clean():
    pass


def reset():
    pass


def has_file(filename, basepath='.'):
    return os.path.isfile(os.path.join(basepath, filename))


def has_dir(dirpath, basepath='.'):
    return os.path.isdir(os.path.join(basepath, dirpath))


def get_dirname(dirname):
    if not os.path.isdir(dirname):
        # make the directory if not exits
        print(f'The directory <{dirname}> does not exist yet.')
        os.mkdir(dirname) # FIXME: not considering user permissions
        print(f'The directory <{dirname}> has been created.')
    return dirname


def mkdir(dirname, basepath='.'):
    fullpath = os.path.join(basepath, dirname)
    if not has_dir(dirname, basepath):
        os.mkdir(fullpath)
        print(f'The directory <{fullpath}> has been created.')
    else:
        try:
            # remove old one and its contents, then create a new one
            shutil.rmtree(fullpath)
            os.mkdir(fullpath) # FIXME: not considering user permissions
        except OSError as e:
            print ('Error: %s - %s.' % (e.filename, e.strerror)) # not handled :(
    return fullpath


def load_config(filename='config.yml'):
    # make sure the config file exists
    if not os.path.isfile(filename):
        raise IOError(f'the filename <{filename}> does not exists.')

    with open(filename, 'r') as configfile:
        config = yaml.load(configfile)
    return config


CONFIG = load_config()
rootDir = get_dirname(CONFIG['rootDir'])
outDir = get_dirname(CONFIG['outDir'])
sampleDir = mkdir(CONFIG['paths']['sample'], outDir)
graphDir = mkdir(CONFIG['paths']['graph'], outDir)
# ==============================================================================
# END: Config
# ==============================================================================