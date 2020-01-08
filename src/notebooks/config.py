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
    """ Initial setup for the application """
    plotter.ioff() # turn off interactive plotting mode
    warnings.filterwarnings('ignore') # turn off warnings


def clean():
    """ Reset python environment """
    pass


def reset():
    """ Reset python environment """
    pass


def has_file(filename, basepath='.'):
    """Wrapper to check if a file exists"""
    return os.path.isfile(os.path.join(basepath, filename))


def has_dir(dirpath, basepath='.'):
    """Wrapper to check if a directory exists"""
    return os.path.isdir(os.path.join(basepath, dirpath))


def get_dirname(dirname):
    """
    Confirm that the specified directory exits before using it. This is a basic
    wrapper for sanitizing future directory-related operations.

    Notes
    -----
    This function helps to play safe when referring to file system handling as
    the application runs in case the user might mistake the paths for the root
    and distribution directories.

    Parameters
    ----------
    dirname : string
        the name of the directory that should be properly set (should exist)

    Returns
    -------
    dirname : string
        the name of the directory that properly set
    """
    if not os.path.isdir(dirname):
        # make the directory if not exits
        print(f'The directory <{dirname}> does not exist yet.')
        os.mkdir(dirname) # FIXME: not considering user permissions
        print(f'The directory <{dirname}> has been created.')
    return dirname


def mkdir(dirname, basepath='.'):
    """
    Create a directory. If there is already a directory with the given name, it
    will forcefully remove the old one, namely its contents, then will create an
    empty directory with the given name.

    Notes
    -----
    This function is a small internal util with a specific goal. Do not use it
    for other purposes. It is built upon the `os.mkdir` method but does not wrap
    all its functionalities. No execeptions are being handled for directory
    creation violations.

    Parameters
    ----------
    dirname : string
        the name of the directory to be created
    basepath : string, default '.'
        the name of the base path serving as the root directory for directory
        creation. Note that the default value is '.', the representation of the
        current working directory.

    Returns
    -------
    fullpath : string
        a reference of the relative path of the created directory

    Examples
    --------
    >>> a_dir = mkdir('directory-1')
    >>> print(a_dir)
    './a_directory'

    >>> a_dir = mkdir('directory-1', './path/to/a-directory')
    >>> print(a_dir)
    './path/to/a-directory/directory-1'

    """
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
    """
    Load the application configuration from an external YAML file.

    Parameters
    ----------
    filename : string, default 'config.yml'
        the name of the YAML-formated file containing the required setup to
        configure the application at its startup.

    Notes
    -----
    There is no API defining the YAML-based keys yet. That is, the required YAML
    keys are shown in the `config.yml` as an example of references the required
    keys.
    """
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