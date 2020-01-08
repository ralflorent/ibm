# Virtual Environment for Individual-Based Modeling (IBM)
#
# Created on March 31, 2019
# Last updated on Jan 6, 2020
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
import constants
from core import initialize, observe, update, finalize

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
    print('=> START: Running simulation for waterbirds ABM')
    habitats, agents = initialize()
    observe(habitats, agents, time)

    for time in range(1, constants.PROCESSING_TIME):
        agents = update(habitats, agents, time) # override agents when being updated
        observe(habitats, agents, time)

    print('=> END: Running simulation for waterbirds ABM')

    # post-conditions
    finalize()

# run application
application()

# ==============================================================================
# END: Application
# ==============================================================================