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
# Main entry point for the application

# ==============================================================================
# START: Preamble
# ==============================================================================

# -*- coding: utf-8 -*-
import config
import constants as CONST
from core import initialize, observe, update
from helpers import plot_figure, make_gif

# ==============================================================================
# END: Preamble
# ==============================================================================

# ==============================================================================
# START: Application
# ==============================================================================

# main entry point for the application
# TODO: proper docs
def application():

    # pre-conditions
    config.init() # initialize internal config for the app
    time = 0 # define stopwatch for the process

     # process for t times
    print('=> START: Processing random movements based on prob dist')
    habitats, agents = initialize()
    observe(habitats, agents, time)

    for time in range(1, CONST.PROCESSING_TIME):
        agents = update(habitats, agents, time) # override agents when being updated
        observe(habitats, agents, time)

    print('=> END: Processing random movements based on prob dist')

    # post-conditions
    make_gif('snapshots.gif')
    plot_figure()


# run application
application()