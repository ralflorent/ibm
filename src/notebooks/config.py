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

import matplotlib.pyplot as plotter # plotter
import matplotlib.pylab as pylab

# TODO: plotter, env, sys, file, common config

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


# ==============================================================================
# END: Config
# ==============================================================================