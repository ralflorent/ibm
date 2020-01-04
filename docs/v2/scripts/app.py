import config
import constants
from core import initialize, observe, update

# main entry point for the application
def application():
    # pre-conditions
    config.init() # initialize internal config for the app
    time = 0 # define stopwatch for the process

    # process for t times
    print('=> START: Running simulation for waterbirds ABM')
    habitats, agents = initialize()
    observe(habitats, agents, time)

    for time in range(1, constants.PROCESSING_TIME):
        agents = update(habitats, agents, time)
        observe(habitats, agents, time)
    print('=> END: Running simulation for waterbirds ABM')
    # omit post-conditions

application() # run application