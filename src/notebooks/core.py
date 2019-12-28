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
    verts, props = C.DEFAULTS['verts'], C.DEFAULTS['props']

    # prepare static patches (habitats and human settlements)
    orange_sm = Habitat(C.LAGOON_ORANGE_SM, C.LAGOON_TYPE_ORANGE, C.COLORS[C.LAGOON_ORANGE_SM])
    orange_sm.verts = verts[C.LAGOON_ORANGE_SM]
    orange_sm.props = props[C.LAGOON_ORANGE_SM]
    orange_sm.label = C.LABELS[C.LAGOON_ORANGE_SM]
    orange_sm.build()
    habitats.append(orange_sm)

    orange_lg = Habitat(C.LAGOON_ORANGE_LG, C.LAGOON_TYPE_ORANGE, C.COLORS[C.LAGOON_ORANGE_LG])
    orange_lg.verts = verts[C.LAGOON_ORANGE_LG]
    orange_lg.props = props[C.LAGOON_ORANGE_LG]
    orange_lg.label = C.LABELS[C.LAGOON_ORANGE_LG]
    orange_lg.build()
    habitats.append(orange_lg)

    blue = Habitat(C.LAGOON_BLUE, C.LAGOON_TYPE_BLUE, C.COLORS[C.LAGOON_BLUE])
    blue.verts = verts[C.LAGOON_BLUE]
    blue.props = props[C.LAGOON_BLUE]
    blue.label = C.LABELS[C.LAGOON_BLUE]
    blue.build()
    habitats.append(blue)

    green = Habitat(C.LAGOON_GREEN, C.LAGOON_TYPE_GREEN, C.COLORS[C.LAGOON_GREEN])
    green.verts = verts[C.LAGOON_GREEN]
    green.props = props[C.LAGOON_GREEN]
    green.label = C.LABELS[C.LAGOON_GREEN]
    green.build()
    habitats.append(green)

    human1 = Habitat(C.HUMAN_SETTLEMENT, C.HUMAN_SETTLEMENT, C.COLORS[C.HUMAN_SETTLEMENT])
    human1.verts = verts[C.HUMAN_SETTLEMENT+'1']
    human1.label = C.LABELS[C.HUMAN_SETTLEMENT]
    human1.build(fill=True)
    habitats.append(human1)

    human2 = Habitat(C.HUMAN_SETTLEMENT, C.HUMAN_SETTLEMENT, C.COLORS[C.HUMAN_SETTLEMENT])
    human2.verts = verts[C.HUMAN_SETTLEMENT+'2']
    human2.label = C.LABELS[C.HUMAN_SETTLEMENT]
    human2.build(fill=True)
    habitats.append(human2)

    human3 = Habitat(C.HUMAN_SETTLEMENT, C.HUMAN_SETTLEMENT, C.COLORS[C.HUMAN_SETTLEMENT])
    human3.verts = verts[C.HUMAN_SETTLEMENT+'3']
    human3.label = C.LABELS[C.HUMAN_SETTLEMENT]
    human3.build(fill=True)
    habitats.append(human3)

    return habitats


def create_agents(habitats):
    """Create agents once
    TODO: docs
    """
    agents = []

    # build patches for short- and long-legged seabirds
    short_legged_habitat = [h for h in habitats if h.id in C.AREA_SHORT_LEGGED]
    long_legged_habitat  = [h for h in habitats if h.id in C.AREA_LONG_LEGGED]

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
        snapshots[habitat.id][agent.type] += 1

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
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.markersize'] = 3
    plt.rcParams['legend.fontsize'] = 10
    fig = plt.figure(1)
    ax  = fig.add_subplot(111)

    # artists to display (with indicator)
    for h in habitats:
        ax.add_patch( cp.copy(h.artist) )

    # distribute agents according their types
    shorts = [ag for ag in agents if ag.type == C.SHORT_LEGGED]
    longs = [ag for ag in agents if ag.type == C.LONG_LEGGED]

    # plot agents' positions
    handler_shorts, = ax.plot(
        [ag.x for ag in shorts],
        [ag.y for ag in shorts],
        'o', mec=C.COLORS[C.SHORT_LEGGED],
        mfc=C.COLORS[C.SHORT_LEGGED],
        label=C.LABELS[C.SHORT_LEGGED]
    )
    handler_longs, = ax.plot(
        [ag.x for ag in longs],
        [ag.y for ag in longs],
        'o', mec=C.COLORS[C.LONG_LEGGED],
        mfc=C.COLORS[C.LONG_LEGGED],
        label=C.LABELS[C.LONG_LEGGED]
    )

    # legends for the plot through handlers
    handler_artists = [h.artist for h in habitats[1:5]] # hard-coded order
    handler_artists.extend([handler_shorts, handler_longs])

    # additional settings for the plot
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.legend(handles=handler_artists, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    plt.xlabel('Time ' + str(counter + 1))
    plt.title('Snapshot in time ' + str(counter + 1), fontsize=12) # Identify which image is plotted

    image_path = os.path.join(C.SAMPLE_DIR, str(counter + 1) + '.png')
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

    # storing image for final gif
    image = gm.imread(image_path)
    C.STORE['images'].append(image) # FIXME: read it when necessary
    # END: observe


def update_one(habitats, agent):
    """ Update agent in one unit of time
    TODO: docs
    """

    # build patches for short- and long-legged seabirds, human settlements
    short_legged_habitat = [h for h in habitats if h.id in C.AREA_SHORT_LEGGED]
    long_legged_habitat = [h for h in habitats if h.id in C.AREA_LONG_LEGGED]
    human_settlements = [h for h in habitats if h.id == C.HUMAN_SETTLEMENT]

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
    update_store(C.STORE['agents'], agent, prob, _habitat.id)
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
        snapshots[habitat.id][agent.type] += 1

    print('--- snapshot stats: {}'.format(snapshots))
    C.STORE['habitats'].append(snapshots)
    print('--- process update: {}'.format(len(C.STORE['habitats'])))

    return updated_agents


def update_habitat_water_depth(h: Habitat, x=0):
    """
    Simulate change in habitat's characteristics (water depth) over time
    TODO: docs
    """
    if h.id == C.LAGOON_ORANGE_SM:
        h.props['w'] = -0.00002*x**2 + 0.064*x + 10.034
    elif h.id == C.LAGOON_ORANGE_LG:
        h.props['w'] = -0.0001*x**2 + 0.0987*x + 6.1176
    elif h.id == C.LAGOON_BLUE:
        h.props['w'] = -0.00003*x**2 + 0.0636*x + 34.114
    elif h.id == C.LAGOON_GREEN:
        h.props['w'] = -0.00005*x**2 + 0.061*x + 97.442


# ==============================================================================
# END: Core functionality
# ==============================================================================