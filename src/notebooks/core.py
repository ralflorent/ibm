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
import uuid # hasher
import pandas as pd # dataframe handling
import copy as cp # copier
import imageio as gm # gif maker
import numpy as np # arithmetic computer
import matplotlib.pyplot as plt # plotter
import matplotlib.patches as Patches # artist
from datetime import datetime # datetime handler
from matplotlib.path import Path # designing field
from functools import reduce # utils

import constants as C
from helpers import *
from habitat import Habitat
from agent import Agent

def initialize():
    """
    TODO: docs
    """
    habitats = create_patches()
    print('==> {} habitats have been created successfully!'.format(len(habitats)))
    agents = create_agents(habitats)
    print('==> {} agents have been created successfully!'.format(len(agents)))

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

    C.STORE['env'].append(snapshots)
    print('--- snapshot for time {}'.format(1))
    print('--- updating agents will start processing...')
    return habitats, agents


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

        for i in range(ag_cnf['quantity']):
            x, y = gen_rand_point(restricted_habs, 'in')
            ag = Agent(ag_cnf['type'], x, y)
            ag.name = '{}-{}'.format(i + 1, ag_cnf['type']) # name: 1-30cm
            ag.color = ag_cnf['color']
            agents.append(ag)
    return agents


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
    # END: observe


def update_one(habitats, agent, time):
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
    prob = 0.0

    for ag_cnf in C.CNF_AG: # for each category of agent (e.g., 15cm legged)
        # this agent can use certain areas only
        restricted_habs = []
        for _type in ag_cnf['habs']:
            for hab in habitats:
                if hab.type == _type:
                    restricted_habs.append(hab) # are these limited areas
                    break

        # do's and dont's specific to this agent
        if agent.type == ag_cnf['type']:
            point = gen_rand_point(restricted_habs, 'in')
            habitat = which_habitat(point, restricted_habs)
            _d = compute_dist(habitat, human_settlements)
            min_index = _d.index( min(_d) ) # consider minimal distance

            # specific characteristics of the selected habitat
            d = _d[min_index] # distance to human settlement
            w, s, f = habitat.props.values() # water depth, salinity, food availability

            # this agent knows a specific way to compute certain operations
            meta_fns = C.get_agentp(agent.type, 'fns')
            probs = { 'w': 0, 's': 0, 'f': 0, 'd': 0 } # track probabilities
            for meta_fn in meta_fns:
                penv = meta_fn['penv'] # which spec: w, s, f, d
                if penv == 'w': probs['w'] = eval_fn(meta_fn, w)
                elif penv == 's': probs['s'] = eval_fn(meta_fn, s)
                elif penv == 'f': probs['f'] = eval_fn(meta_fn, f)
                else: probs['d'] = eval_fn(meta_fn, d)

            # compute the overall probability of moving to this habitat
            prob = reduce(lambda acc, val: acc * val, probs.values())

        if prob > C.THRESHOLD:
            agent.set_point(point)

    stats = {
        'processing_unit': time,
        'agent_name': agent.name,
        'agent_x': agent.get_point()[0],
        'agent_y': agent.get_point()[1],
        'hab_name': habitat.id,
        'hab_type': habitat.type,
        'hab_water_depth': w,
        'hab_salinity': s,
        'hab_food': f,
        'hab_distance': d,
        'prob_overall': prob,
        'prob_water': probs['w'],
        'prob_salinity': probs['s'],
        'prob_food': probs['s'],
        'prob_distance': probs['d'],
        'has_moved': prob > C.THRESHOLD
    }
    return agent, habitat, stats
    # END: update


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
        agent = agents[ np.random.randint( len(agents) ) ]
        updated_agent, habitat, stats = update_one(habitats, cp.copy(agent), time)
        updated_agents.append( updated_agent )
        agents.remove(agent)
        for k, v in stats.items(): C.STORE['stats'][k].append(v) # data tracking

    for agent in updated_agents:
        habitat = which_habitat(agent.get_point(), habitats)
        snapshots[habitat.id][agent.type] += 1

    C.STORE['env'].append(snapshots)
    print('--- snapshot for time {}'.format(time + 1))
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



def make_gif(gifname='image.gif', dirname=C.SAMPLE_DIR, storage=[]):
    """
    Store or dump all generated png images on disk

    TODO: proper docs
    """
    IMG_EXT = '.png'
    filename = os.path.join(dirname, gifname)
    if len(storage) == 0:
        imgnames = [f for f in os.listdir(dirname) if f.lower().endswith(IMG_EXT)]
        sorted_imgnames = sort_imgnames(imgnames, IMG_EXT)
        for imgname in sorted_imgnames:
            image = gm.imread(os.path.join(dirname, imgname))
            storage.append(image)
    gm.mimsave(filename, storage)
    print(f'=> Combined snapshots are saved as GIF at <{filename}>')


def sort_imgnames(imgnames, ext='.png', reverse=False):
    names = list(map(int, [p.split(ext)[0] for p in imgnames]))# convert to integers
    names.sort(reverse=reverse) # proper sorting for integers
    return list(map(lambda n: str(n) + ext, names)) # restore names


def plot_figure():
    """Plot a summary of the distribution of the agents within the habitats."""
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.5
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['font.size'] = 12
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.markersize'] = 3

    grouped_agents = dict()
    for ag_cnf in C.CNF_AG:
        grouped_agents[ag_cnf['type']] = dict()

    for regions in C.STORE['env']: # snapshot
        for region_key in regions.keys(): # area key: 'orange-sm'
            for grouped_key in grouped_agents: # by agent key: '15cm'
                if region_key not in grouped_agents[grouped_key]:
                    grouped_agents[grouped_key][region_key] = [] # make sure key exist
                # final thread: { '15cm': { 'orange-sm': [4, ...] } } ::
                # of this agent in region for each time t processing
                grouped_agents[grouped_key][region_key].append(regions[region_key][grouped_key])

    plt.cla()
    plt.clf()
    fig = plt.figure(2, figsize=(11, 6.5))
    t = np.arange(C.PROCESSING_TIME)
    xlim = [0, C.PROCESSING_TIME]
    ylim = [0, C.MAX_AGENT_QTY]
    handlers = []

    panel_A = fig.add_subplot(2,2,1)
    panel_A.set_xlim(xlim)
    panel_A.set_ylim(ylim)
    panel_A.tick_params(axis='y', colors='orange')
    panel_A.set_xlabel('Times')
    panel_A.set_ylabel('Waterbirds', color='orange')
    panel_A.set_title('Distribution in Habitat 1 (Large Lagoon)', fontsize=13)

    panel_B = fig.add_subplot(2,2,2)
    panel_B.set_xlim(xlim)
    panel_B.set_ylim(ylim)
    panel_B.tick_params(axis='y', colors='orange')
    panel_B.set_xlabel('Times')
    panel_B.set_ylabel('Waterbirds', color='orange')
    panel_B.set_title('Distribution in Habitat 1 (Small Lagoon)', fontsize=13)

    panel_C = fig.add_subplot(2,2,3)
    panel_C.set_xlim(xlim)
    panel_C.set_ylim(ylim)
    panel_C.tick_params(axis='y', colors='blue')
    panel_C.set_xlabel('Times')
    panel_C.set_ylabel('Waterbirds', color='blue')
    panel_C.set_title('Distribution in Habitat 2 (Blue Lagoon)', fontsize=13)

    panel_D = fig.add_subplot(2,2,4)
    panel_D.set_xlim(xlim)
    panel_D.set_ylim(ylim)
    panel_D.tick_params(axis='y', colors='green')
    panel_D.set_xlabel('Times')
    panel_D.set_ylabel('Waterbirds', color='green')
    panel_D.set_title('Distribution in Habitat 3 (Green Lagoon)', fontsize=13)

    for gk in grouped_agents.keys():
        color = C.get_agentp(gk, 'color')
        label = C.get_agentp(gk, 'label')
        panel_A.plot(t, grouped_agents[gk][C.LAGOON_ORANGE_LG], '-o', color=color)
        panel_B.plot(t, grouped_agents[gk][C.LAGOON_ORANGE_SM], '-o', color=color)
        panel_C.plot(t, grouped_agents[gk][C.LAGOON_BLUE], '-o', color=color)
        leg_handler, = panel_D.plot(t, grouped_agents[gk][C.LAGOON_GREEN], '-o', color=color, label=label)
        handlers.append(leg_handler)

    fig.legend(
        handles=handlers,
        loc='lower left',
        bbox_to_anchor=(0.05, 0.98, 0.92, .102),
        ncol=C.TOTAL_AGENT_TYPE, mode='expand',
        borderaxespad=0., fancybox=True, shadow=True
    )

    fig.set_tight_layout(True) # Avoid panel overlaps
    fig.suptitle('Simulation of Waterbirds in the Tropics', y=1.1, fontsize=14, fontweight='bold')
    filename = os.path.join(C.GRAPH_DIR, uuid.uuid4().hex +'.pdf') # save in pdf format
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
    # plt.show()


def finalize():
    # summarize all snapshots in a GIF image
    make_gif('snapshots.gif')
    # display all snapshots' summary in a graph
    plot_figure()
    # track data for analysis
    df = pd.DataFrame(C.STORE['stats'])
    datenow = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(C.GRAPH_DIR, datenow + '.csv')
    df.to_csv(filename, index=None, header=True)
    print(f'=> Statistics successfully saved at <{filename}>')
    # reset store
    C.STORE['stats'] = []
    C.STORE['env'] = []


# ==============================================================================
# END: Core functionality
# ==============================================================================