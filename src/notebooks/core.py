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
# Core functionalities and interactions of the components within the system

# ==============================================================================
# START: Core functionality
# ==============================================================================

# -*- coding: utf-8 -*-
import os
import numpy as np # arithmetic computer
import matplotlib.pyplot as plt # plotter
import matplotlib.patches as Patches # artist
import imageio as gm # gif maker
import constants as C
import copy as cp

from matplotlib.path import Path # designing field
from helpers import gen_rand_point, which_habitat, compute_dist, update_store
from habitat import Habitat
from agent import Agent


def create_patches():
    habitats = []
    verts = C.DEFAULTS['verts']
    props = C.DEFAULTS['props']

    # prepare static (patch-based) habitats and human settlements
    habitats.append( Habitat(C.LAGOON_ORANGE_SM, verts[C.LAGOON_ORANGE_SM], 'orange',
            props[C.LAGOON_ORANGE_SM]) )
    habitats.append( Habitat(C.LAGOON_ORANGE_LG, verts[C.LAGOON_ORANGE_LG], 'orange',
            props[C.LAGOON_ORANGE_LG]) )
    habitats.append( Habitat(C.LAGOON_BLUE, verts[C.LAGOON_BLUE], 'blue', props[C.LAGOON_BLUE]) )
    habitats.append( Habitat(C.LAGOON_GREEN, verts[C.LAGOON_GREEN], 'green', props[C.LAGOON_GREEN]))
    habitats.append( Habitat(C.HUMAN_SETTLEMENT, verts[C.HUMAN_SETTLEMENT+'1'], 'red') )
    habitats.append( Habitat(C.HUMAN_SETTLEMENT, verts[C.HUMAN_SETTLEMENT+'2'], 'red') )
    habitats.append( Habitat(C.HUMAN_SETTLEMENT, verts[C.HUMAN_SETTLEMENT+'3'], 'red') )

    # then build patch for each habitat
    for h in habitats:
        filled = False
        if h.type == C.HUMAN_SETTLEMENT:
            filled = True
        h.build(fill=filled)

    return habitats


# create agents once
def create_agents(habitats):
    """
    TODO: docs
    """
    agents = []

    # build patches for short- and long-legged seabirds
    short_legged_habitat = [h for h in habitats if h.type in C.AREA_SHORT_LEGGED]
    long_legged_habitat  = [h for h in habitats if h.type in C.AREA_LONG_LEGGED]

    for i in range(C.TOTAL_SHORT_LEGGED + C.TOTAL_LONG_LEGGED):
        ag = Agent()
        ag.name = str(i + 1) # labelling for analysis

        # classify agents as short- and long-legged seabirds
        if i < C.TOTAL_SHORT_LEGGED:
            ag.type = C.SHORT_LEGGED
            ag.x, ag.y = gen_rand_point(short_legged_habitat, 'in')
        else:
            ag.type = C.LONG_LEGGED
            ag.x, ag.y = gen_rand_point(long_legged_habitat, 'in')

        agents.append(ag) # store in-memory agents

        # create a dict-based structure to store and run analytics
        C.STORE['agents'].append({ ag.name: { 'hab': [], 'pos': [], 'pdf': [] }})

    return agents


def initialize():
    """
    TODO: docs
    """
    habitats = create_patches()
    agents = create_agents(habitats)

    # initialize stats for first run
    snapshots = {
        C.LAGOON_ORANGE_SM: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 },
        C.LAGOON_ORANGE_LG: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 },
        C.LAGOON_BLUE: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 },
        C.LAGOON_GREEN: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 }
    }

    for agent in agents:
        habitat = which_habitat((agent.x, agent.y), habitats)
        snapshots[habitat.type][agent.type] += 1

    print('--- snapshot stats: {}'.format(snapshots))
    C.STORE['habitats'].append(snapshots)
    print('--- process update: {}'.format(len(C.STORE['habitats'])))
    return habitats, agents


def observe(habitats, agents, counter=0):
    """
    Create and plot figure
    TODO: docs
    """
    plt.cla()

    fig = plt.figure(1)
    ax  = fig.add_subplot(111)

    for h in habitats:
        ax.add_patch( cp.copy(h.artist) ) # add artists (patches) to display rectangles

    # distribute agents according their types
    shorts = [ag for ag in agents if ag.type == C.SHORT_LEGGED]
    longs = [ag for ag in agents if ag.type == C.LONG_LEGGED]

    # plot agents' positions
    ax.plot([ag.x for ag in shorts], [ag.y for ag in shorts], 'o',
            mfc=C.COLORS[C.SHORT_LEGGED], mec='k', label=C.SHORT_LEGGED)
    ax.plot([ag.x for ag in longs], [ag.y for ag in longs], 'o',
            mfc=C.COLORS[C.LONG_LEGGED], mec='k', label=C.LONG_LEGGED)

    # additional settings for the graph
    plt.axis('off')
    plt.legend(loc='lower left')
    plt.xlabel('Time ' + str(counter + 1)) # Identify which image is plotted
    plt.title('Virtual Environment') # Title the graph

    image_path = os.path.join(C.SAMPLE_DIR, str(counter + 1) + '.png')
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # storing image for final gif
    image = gm.imread(image_path)
    C.STORE['images'].append(image)
    # END: observe


def update_one(habitats, agent):
    """
    TODO: docs
    """

    # FIXME: Cannot put single artist in more than one figure
    # habitats = create_patches()

    # build patches for short- and long-legged seabirds, human settlements
    short_legged_habitat = [h for h in habitats if h.type in C.AREA_SHORT_LEGGED]
    long_legged_habitat = [h for h in habitats if h.type in C.AREA_LONG_LEGGED]
    human_settlements = [h for h in habitats if h.type == C.HUMAN_SETTLEMENT]

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
    P(large_wading_birds) = (3.40 * f) + 0.9239

    P(small_wading_birds) = 0.00002 * (w^2) - 0.0009 * w + 0.0114
    P(small_wading_birds) = -0.0013 * (d^2) + 0.0074 * d - 0.0001
    P(small_wading_birds) = 0.00006 * (s^2) + 0.0002 * s + 0.0004
    P(small_wading_birds) = (6.73 * f^2) – (29.36 * f) + 14.35

    d: distance between the current habitat and the closest human settlement
    w: water depth of the current habitat
    s: salinity of the current habitat
    f: food availability in the current habitat
    """

    if agent.type == C.SHORT_LEGGED:
        # [_variable_name] means variables within this scope
        _x, _y = gen_rand_point(short_legged_habitat, 'in')
        _habitat = which_habitat((_x, _y), short_legged_habitat)
        _d = compute_dist(_habitat, human_settlements)
        min_index = _d.index( min(_d) ) # consider minimal distance

        d = _d[min_index] # distance to human settlement
        w, s, f = _habitat.props.values() # water depth, salinity, food availability

        # TODO: avoid magic numbers and string values
        _prob_w = 0.00002 * w**2 - 0.0009 * w + 0.0114
        _prob_d = -0.0013 * d**2 + 0.0074 * d - 0.0001
        _prob_s = 0.00006 * s**2 + 0.0002 * s + 0.0004
        _prob_f = (0.00673 * f**2) - (0.002936 * f) + 0.5
        prob = _prob_s * _prob_w * _prob_d * _prob_f
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

    # print('---- overall prob: {:1.10f}'.format(prob))
    if prob > C.MOVE_THRESHOLD:
        agent.x, agent.y = _x, _y

    # store agent's position and probs
    update_store(C.STORE['agents'], agent, prob, _habitat.type)
    return agent, _habitat
    # END: update


def update(habitats, agents, time):
    """
    This update signifies that, at a time t, some changes should apply to every
    and each single agent of the system.

    TODO: proper docs
    """
    updated_agents = [] # temporary for the new agents' positions

    snapshots = {
        C.LAGOON_ORANGE_SM: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 },
        C.LAGOON_ORANGE_LG: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 },
        C.LAGOON_BLUE: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 },
        C.LAGOON_GREEN: { C.SHORT_LEGGED: 0, C.LONG_LEGGED: 0 }
    }

    if time % C.TIME_DIVISOR == 0: # every t time steps, change the environment
        rainfall = C.DEFAULTS['rain'].get(time, 0)
        for h in habitats:
            update_habitat_water_depth(h, rainfall)

    while len(agents) > 0:
        # randomly choose an agent to update its status,
        # approach for asynchronous updates: see Davi's ref.
        agent = agents[ np.random.randint( len(agents) ) ]
        # old_habitat = which_habitat((agent.x, agent.y), habitats) # diogo
        updated_agent, habitat = update_one(habitats, cp.copy(agent))
        updated_agents.append( updated_agent )
        agents.remove(agent)

    # TODO: (can be improved) save stats for each agent: regions -> blue -> short-legged: 0+
    for agent in updated_agents:
        habitat = which_habitat((agent.x, agent.y), habitats)
        snapshots[habitat.type][agent.type] += 1

    print('--- snapshot stats: {}'.format(snapshots))
    C.STORE['habitats'].append(snapshots)
    print('--- process update: {}'.format(len(C.STORE['habitats'])))

    return updated_agents


def update_habitat_water_depth(h: Habitat, x=0):
    """
    Simulate change in habitat's characteristics (water depth) over time
    TODO: docs
    """
    if h.type == C.LAGOON_ORANGE_SM:
        h.props['w'] = -0.00002*x**2 + 0.064*x + 10.034
    elif h.type == C.LAGOON_ORANGE_LG:
        h.props['w'] = -0.0001*x**2 + 0.0987*x + 6.1176
    elif h.type == C.LAGOON_BLUE:
        h.props['w'] = -0.00003*x**2 + 0.0636*x + 34.114
    elif h.type == C.LAGOON_GREEN:
        h.props['w'] = -0.00005*x**2 + 0.061*x + 97.442


# ==============================================================================
# END: Core functionality
# ==============================================================================