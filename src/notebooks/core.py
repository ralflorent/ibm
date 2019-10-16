# Individual-Based Modeling (IBM)
#
# Created on October 12, 2019
#
# Authors:
#   Ralph Florent <r.florent@jacobs-university.de>
#   Davi Tavares <davi.tavares@leibniz-zmt.de>
#   Agostino Merico <a.merico@jacobs-university.de>
#
# Core functionalities and interactions of the components within the system

# ==============================================================================
# START: Core functionality
# ==============================================================================

# -*- coding: utf-8 -*-
import numpy as np # arithmetic computer
import matplotlib.pyplot as plt # plotter
import matplotlib.patches as Patches # artist
import imageio as gm # gif maker
import constants as CONST

from matplotlib.path import Path # designing field
from helpers import gen_rand_point, which_habitat, compute_dist
from habitat import Habitat
from agent import Agent


def create_patches():
    habitats = []

    # Food availability per habitat: 0.3, 2.56, 6.41, and 11.53
    # prepare static (patch-based) habitats and human settlements
    habitats.append( Habitat('one', CONST.HABITAT_1A_VERTICES, 'orange', {'w': 0.05, 's': 80, 'f': 0.3}) )
    habitats.append( Habitat('one', CONST.HABITAT_1B_VERTICES, 'orange', {'w': 0.05, 's': 80, 'f': 2.56}) )
    habitats.append( Habitat('two', CONST.HABITAT_2_VERTICES, 'blue', {'w': 1.0, 's': 10, 'f': 6.41}) )
    habitats.append( Habitat('three', CONST.HABITAT_3_VERTICES, 'green', {'w': 0.40, 's': 25, 'f': 11.53}) )
    habitats.append( Habitat('human', CONST.HUMAN_STM1_VERTICES, 'red') )
    habitats.append( Habitat('human', CONST.HUMAN_STM2_VERTICES, 'red') )
    habitats.append( Habitat('human', CONST.HUMAN_STM3_VERTICES, 'red') )

    # then build patch for each habitat
    for h in habitats:
        filled = False
        if h.type == 'human':
            filled = True
        h.build(fill=filled)

    return habitats


# create agents
def create_agents(habitats):
    """
    TODO: docs
    """
    agents = []

    # build patches for short- and long-legged seabirds
    short_legged_habitat = [h for h in habitats if h.type in CONST.SHORT_LEGGED_SEABIRD_HABITAT_LIMIT]
    long_legged_habitat  = [h for h in habitats if h.type in CONST.LONG_LEGGED_SEABIRD_HABITAT_LIMIT]

    for i in range(CONST.TOTAL_SHORT_LEGGED_SEABIRDS + CONST.TOTAL_LONG_LEGGED_SEABIRDS):
        ag = Agent()

        # classify agents as short- and long-legged seabirds
        if i < CONST.TOTAL_SHORT_LEGGED_SEABIRDS:
            ag.type = 'short-legged'
            ag.x, ag.y = gen_rand_point(short_legged_habitat, 'in')
        else:
            ag.type = 'long-legged'
            ag.x, ag.y = gen_rand_point(long_legged_habitat, 'in')

        agents.append(ag) # store in-memory agents

    return agents


def initialize():
    """
    TODO: docs
    """
    habitats = create_patches()
    agents = create_agents(habitats)
    return habitats, agents


def observe(habitats, agents, counter=0):
    """
    Create and plot figure
    TODO: docs
    """
    plt.cla()

    fig = plt.figure(figsize=(11, 6.5)) # define figure size 11x6.5 inches
    ax  = fig.add_subplot(111)

    for h in habitats:
        ax.add_patch(h.artist) # add artists (patches) to display rectangles

    # distribute agents according their types
    short = [ag for ag in agents if ag.type == 'short-legged']
    long = [ag for ag in agents if ag.type == 'long-legged']

    # plot agents' positions
    ax.plot([ag.x for ag in short], [ag.y for ag in short], 'o', mfc ='k', mec ='k', label='short-legged')
    ax.plot([ag.x for ag in long], [ag.y for ag in long], 'o', mfc ='w', mec ='k', label='long-legged')

    # additional settings for the graph
    plt.axis('image')
    plt.axis([0, 1, 0, 1])
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(loc="best")
    plt.xlabel('Time ' + str(int(counter)), fontsize=15) # Identify which image is plotted
    plt.title('Virtual Environment', fontsize=15) # Title the graph

    image_path = CONST.FILEPATH + str(int(counter)) + '.png'
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # storing image for final gif
    image = gm.imread(image_path)
    CONST.IMAGE_STORAGE.append(image)
    # END: observe


def update(agents):
    """
    TODO: docs
    """

    # Cannot put single artist in more than one figure
    habitats = create_patches()

    # build patches for short- and long-legged seabirds, human settlements
    short_legged_habitat = [h for h in habitats if h.type in CONST.SHORT_LEGGED_SEABIRD_HABITAT_LIMIT]
    long_legged_habitat  = [h for h in habitats if h.type in CONST.LONG_LEGGED_SEABIRD_HABITAT_LIMIT]
    human_settlements = [h for h in habitats if h.type == 'human']

    # randomly choose an agent to update its status,
    # approach for asynchronous updates: see Davi's ref.
    agent = agents[ np.random.randint( len(agents) ) ]

    # simulating random movements
    """ Algorithm to move agents
    0: given a selected agent
    1: randomly choose a new destination (point)
    2: compute probability of habitat use for the destination
    3: move agent if doable (available, resourceful, unthreatening)

    Formulas to compute respective probabilities:

    P(large_wading_birds) = -0.0003 * w + 0.0087
    P(large_wading_birds) = -0.0004 * d + 0.0064
    P(large_wading_birds) = -0.000004 * (s^2) + 0.0004 * s - 0.0002
    P(large_wading_birds) = (3.40 * food_availability) + 0.9239

    P(small_wading_birds) = 0.00002 * (w^2) - 0.0009 * w + 0.0114
    P(small_wading_birds) = -0.0013 * (d^2) + 0.0074 * d - 0.0001
    P(small_wading_birds) = 0.00006 * (s^2) + 0.0002 * s + 0.0004
    P(small_wading_birds) = (6.73 * food_availability^2) – (29.36 * food_availability) + 14.35

    d: distance between current habitat and closest human settlement
    w: water depth of the current habitat
    s: salinity of the current habitat
    f: food availability in the current habitat
    """

    if agent.type == 'short-legged':
        # [_variable_name] means variables within this scope
        _x, _y = gen_rand_point(short_legged_habitat, 'in')
        _habitat = which_habitat((_x, _y), short_legged_habitat)
        _d = compute_dist(_habitat, human_settlements)
        min_index = _d.index( min(_d) ) # consider minimal distance

        d = _d[min_index] # distance to human settlement
        w, s, f = _habitat.props.values() # water depth, salinity, food availability

        _prob_w = 0.00002 * w**2 - 0.0009 * w + 0.0114
        _prob_d = -0.0013 * d**2 + 0.0074 * d - 0.0001
        _prob_s = 0.00006 * s**2 + 0.0002 * s + 0.0004
        _prob_f = (0.00673 * f**2) - (0.002936 * f) + 0.5
        prob = _prob_s * _prob_w * _prob_d * _prob_f
        print('-- habitat: {}'.format(_habitat.type))
        print('---- short: s:{:1.5f}, w:{:1.5f}, d:{:1.5f}, f:{:1.5f}'.format(_prob_s, _prob_w, _prob_d, _prob_f))
    else:
        _x, _y = gen_rand_point(long_legged_habitat, 'in')
        _habitat = which_habitat((_x, _y), long_legged_habitat)
        _d = compute_dist(_habitat, human_settlements)
        min_index = _d.index( min(_d) ) # consider minimal distance

        d = _d[min_index] # distance to human settlement
        w, s, f = _habitat.props.values() # water depth, salinity

        _prob_w = -0.0003 * w + 0.0087
        _prob_d = -0.0004 * d + 0.0064
        _prob_s = -0.000004 * s**2 + 0.0004 * s - 0.0002
        _prob_f = (0.00340 * f) + 0.5
        prob = _prob_s * _prob_w * _prob_d * _prob_f
        print('-- habitat: {}'.format(_habitat.type))
        print('---- long: s:{:1.5f}, w:{:1.5f}, d:{:1.5f}, f:{:1.5f}'.format(_prob_s, _prob_w, _prob_d, _prob_f))

    print('---- overall prob: {:1.10f}'.format(prob))
    if prob > CONST.THRESHOLD:
        agent.x, agent.y = _x, _y

    return habitats, agents
    # END: update

# ==============================================================================
# END: Core functionality
# ==============================================================================