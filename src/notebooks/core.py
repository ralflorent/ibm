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
import math
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
    agents = []

    for ag_cnf in C.CNF_AG:
        restricted_habs = []

        for _type in ag_cnf['habs']:
            for hab in habitats:
                if _type == hab.type:
                    restricted_habs.append(hab)
                    break

        for i in range(ag_cnf['quantity']):
            x, y = gen_rand_point(restricted_habs, 'in')
            ag = Agent(ag_cnf['type'], x, y)
            ag.name = '{}-{}'.format(i + 1, ag_cnf['type']) # name: 1-30cm
            ag.color = ag_cnf['color']
            agents.append(ag)
            # create a dict-based structure to store and run analytics
            # C.STORE['agents'].append({ ag.name: { 'hab': [], 'pos': [], 'pdf': [] }})
    return agents


def initialize():
    """
    TODO: docs
    """
    habitats = create_patches()
    print('==> :) All habitats have been created successfully!')
    agents = create_agents(habitats)
    print('==> :) All agents have been created successfully!')

    # initialize stats for first run
    snapshots = {
        C.LAGOON_ORANGE_SM: {},
        C.LAGOON_ORANGE_LG: {},
        C.LAGOON_BLUE: {},
        C.LAGOON_GREEN: {}
    }
    for ag_cnf in C.CNF_AG:
        for k in snapshots.keys():
            snapshots[k][ag_cnf['type']] = 0

    for agent in agents:
        point = agent.get_point()
        habitat = which_habitat(point, habitats)
        snapshots[habitat.id][agent.type] += 1

    C.STORE['habitats'].append(snapshots)
    print('--- initial snapshot created')
    print('--- updating agents will start processing')
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
    leg_handlers = []

    # artists to display (with indicator)
    for h in habitats:
        ax.add_patch( cp.copy(h.artist) )

    # group by agent's type: { '5cm': [...agents] }
    grouped_agents = dict()
    for ag in agents:
        if ag.type in grouped_agents:
            grouped_agents[ag.type].append(ag)
        else:
            grouped_agents[ag.type] = [ag]

    for _type, g_ags in grouped_agents.items():
        points = [ag.get_point() for ag in g_ags] # get all points: [(x1, y1), (x2, y2), ...]
        x, y = list(zip(*points)) # unzip them: [(x1, x2, ...), (y1, y2, ...)]
        c = C.get_agentp(_type, 'color')
        l = C.get_agentp(_type, 'label')
        leg_handle, = ax.plot(x, y, 'o', mec=c,mfc=c, label=l)
        leg_handlers.append(leg_handle)

    # legends for the plot through handlers
    handler_artists = [h.artist for h in habitats[1:5]] # hard-coded order
    handler_artists.extend(leg_handlers)

    # additional settings for the plot
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.legend(handles=handler_artists, loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    plt.xlabel('Time ' + str(counter + 1))
    plt.title('Snapshot in time ' + str(counter + 1), fontsize=12) # Identify which image is plotted

    image_path = os.path.join(C.SAMPLE_DIR, str(counter + 1) + '.png')
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

    # store image for final gif
    image = gm.imread(image_path)
    C.STORE['images'].append(image) # FIXME: read it when necessary
    # END: observe


def update_one(habitats, agent):
    """ Update agent in one unit of time
    Algorithm for simulating random movements
    - given a randomly-selected agent
    - randomly choose a new destination (point: x, y)
    - compute probability of habitat use for the new destination
    - move agent if doable (available, resourceful, unthreatening)

    d: distance between the current habitat and the closest human settlement
    w: water depth of the current habitat
    s: salinity of the current habitat
    f: food availability in the current habitat
    """
    human_settlements = [h for h in habitats if h.id == C.HUMAN_SETTLEMENT]

    for ag_cnf in C.CNF_AG: # for each category of agent (e.g., 15cm legged)
        restricted_habs = [] # this agent can use certain areas only

        for _type in ag_cnf['habs']:
            for hab in habitats:
                if hab.type == _type:
                    restricted_habs.append(hab) # are these limited areas
                    break

        if agent.type == ag_cnf['type']: # do's and dont's specific to this agent
            _x, _y = gen_rand_point(restricted_habs, 'in')
            _habitat = which_habitat((_x, _y), restricted_habs)
            _d = compute_dist(_habitat, human_settlements)
            min_index = _d.index( min(_d) ) # consider minimal distance

            # specific characteristics (props) of the selected habitat
            d = _d[min_index] # distance to human settlement
            w, s, f = _habitat.props.values() # water depth, salinity, food availability

            # this agent knows a specific way to compute certain operations
            w_meta_fn = C.get_agentp(agent.type, 'fn')

            # compute the probability of moving to this habitat
            _prob_w = eval_fn(w_meta_fn, w)
            _prob_d = -0.0013 * d**2 + 0.0074 * d - 0.0001
            _prob_s = 0.00006 * s**2 + 0.0002 * s + 0.0004
            _prob_f = (0.00673 * f**2) - (0.002936 * f) + 0.5
            prob = _prob_s * _prob_w * _prob_d * _prob_f
        # so, can the agent finally move?
        if prob > C.THRESHOLD:
            agent.set_point((_x, _y))

    # store agent's position and probs
    update_store(C.STORE['agents'], agent, prob, _habitat.id)
    return agent, _habitat
    # END: update


def eval_fn(meta_fn, *args):
    fn_def, fn_args = meta_fn['def'], meta_fn['args']
    fn = eval(fn_def)

    if not isinstance(fn_args, list) or len(fn_args) == 0: # no args required
        return fn()
    elif len(fn_args) == len(args):
        kwargs = dict(zip(fn_args, args)) # zip into keyworded args: {'k': v, ...}
        return fn(**kwargs)
    else:
        raise RuntimeError(f'Cannot evaluate this function <{fn_def}>. Check required arguments')


def update(habitats, agents, time):
    """
    This update signifies that, at a time t, some changes should apply to every
    and each single agent of the system.

    TODO: proper docs
    """
    updated_agents = [] # temporary for the new agents' positions

    snapshots = {
        C.LAGOON_ORANGE_SM: {},
        C.LAGOON_ORANGE_LG: {},
        C.LAGOON_BLUE: {},
        C.LAGOON_GREEN: {}
    }
    for ag_cnf in C.CNF_AG:
        for k in snapshots.keys():
            snapshots[k][ag_cnf['type']] = 0

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

    C.STORE['habitats'].append(snapshots)
    print('--- snapshot for time {}'.format(time))
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