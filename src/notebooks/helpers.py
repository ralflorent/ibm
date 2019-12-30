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
# Set of wrappers and utilities for the overall scripts

# ==============================================================================
# START: Helpers
# ==============================================================================

# -*- coding: utf-8 -*-
import os
import uuid
import numpy as np # arithmetic computations
import imageio as gm # gif maker
import matplotlib.pyplot as plt
import constants as C


def make_gif(dirname='./', gifname='image.gif', storage=[]):
    """
    Store or dump all generated png images on disk

    TODO: proper docs
    """
    filename = os.path.join(dirname, gifname)
    gm.mimsave(filename, storage)


def gen_rand_point(habitats, option=None):
    """ Generate random point that belongs (or not) to a set of patches

    Parameters
    ----------
    patches: array of objects <matplotlib.patch>
        a set of patches (polycurve) to draw simple and compound outlines
        consisting of line segments and splines.

    option: str = {'in', 'out', None}, default = None
            determine whether conditioning the random point being generated
            within or out of the patches. If not specified, return just
            random points without considering the patches.

    Returns
    -------
    (x, y): tuple, of shape (x_coord, y_coord)
        a vertex of unit rectangle from (0,0) to (1,1).
    """
    # make single element iterable
    habitats = habitats if isinstance(habitats, list) else [habitats]

    # initialize random point(x, y) by generating an array
    # of 2 random values between 0 and 1:: [0.1..., 0.4...]
    x, y = np.random.rand(2)

    # flag up a condition to assess points within, or out of the patches
    if option == 'in':
        condition = lambda f: f
    elif option == 'out':
        condition = lambda f: not f
    else:
        return (x, y)

    # iterate until the point based on the given condition is found
    while True:
        found = False
        for habitat in habitats:
            if habitat.contains_point((x, y)):
                found = True

        # base condition to fulfill requirements
        if condition(found):
            break

        x, y = np.random.rand(2) # update point(x, y)

    return (x, y)


def compute_dist(habitat, human_settlements):
    """
    Compute relative distances to the existing human settlements

    TODO: proper docs
    """
    distances = []
    h_center = np.array( habitat.get_center() ) # center point of the habitat

    for settlement in human_settlements:
        s_center = np.array( settlement.get_center() )
        # compute distance between habitat and settlement
        dist = np.linalg.norm(h_center - s_center)
        distances.append(dist)

    return distances # order of distances depends on settlements' settings


def which_habitat(point, habitats):
    """
    Determine in which habitat dwells the current agent

    TODO: proper docs
    """
    for h in habitats:
        if h.contains_point(point):
            return h
    return None


def update_store(objects, agent, prob, hab):
    """"""
    objects = objects if isinstance(objects, list) else [objects]

    for o in objects:
        for k in o.keys():
            if k == agent.name:
                o[k]['hab'].append(hab)
                o[k]['pos'].append( (agent.x, agent.y) )
                o[k]['pdf'].append(prob)
                break


def plot_figure():
    """
    TODO: proper docs
    """
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.5
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['font.size'] = 12
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['lines.markersize'] = 3

    t = np.arange(C.PROCESSING_TIME)

    xlim = [0, C.PROCESSING_TIME]
    ylim = [0, C.TOTAL_AGENTS]

    grouped_agents = dict()
    for ag_cnf in C.CNF_AG:
        grouped_agents[ag_cnf['type']] = dict()

    for regions in C.STORE['habitats']: # snapshot
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
        ncol=2, mode='expand',
        borderaxespad=0., fancybox=True, shadow=True
    )

    fig.set_tight_layout(True) # Avoid panel overlaps
    fig.suptitle('Simulation of Waterbirds in the Tropics', y=1.1, fontsize=14, fontweight='bold')
    filename = os.path.join(C.GRAPH_DIR, uuid.uuid4().hex +'.pdf') # save in pdf format
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # reset store
    C.STORE['agents'] = []
    C.STORE['habitats'] = []


# ==============================================================================
# END: Helpers
# ==============================================================================