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

import numpy as np # arithmetic computations
import imageio as gm # gif maker
import matplotlib.pyplot as plt
import constants as CONST


def make_gif(dirname='./', gifname='image.gif', storage=[]):
    """
    Store or dump all generated png images on disk

    TODO: proper docs
    """
    filename = dirname + gifname
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
    # Make single element iterable
    habitats = habitats if isinstance(habitats, list) else [habitats]

    # initialize random point(x, y) by generating an array
    # of 2 random values between 0 and 1: [0.1..., 0.4...]
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
    t = np.arange(CONST.PROCESSING_TIME)

    shorts, longs = dict(), dict()

    for regions in CONST.STORE['habitats']:
        for k in regions.keys():
            if k not in shorts:
                shorts[k] = []
            if k not in longs:
                longs[k] = []
            shorts[k].append(regions[k]['short-legged'])
            longs[k].append(regions[k]['long-legged'])

    plt.cla()
    fig = plt.figure(1, figsize=(11, 6.5))

    panel_A = fig.add_subplot(2,2,1)
    panel_A.plot(t, shorts['orange-lg'], 'k', label='short legs')
    panel_A.plot(t, longs['orange-lg'], color='#AAAAAA', label='long legs')
    panel_A.legend(loc='best')
    panel_A.set_xlim([0, 20])
    panel_A.tick_params(axis='y', colors='orange')
    panel_A.set_xlabel('Times', fontsize=12)
    panel_A.set_ylabel('Total of Seabirds (Large)', color='orange')

    panel_B = fig.add_subplot(2,2,2)
    panel_B.plot(t, shorts['orange-lg'], 'k', label='short legs')
    panel_B.plot(t, longs['orange-lg'], color='#AAAAAA', label='long legs')
    panel_B.legend(loc='best')
    panel_B.set_xlim([0, 20])
    panel_B.tick_params(axis='y', colors='orange')
    panel_B.set_xlabel('Times', fontsize=12)
    panel_B.set_ylabel('Total of Seabirds (Small)', color='orange')

    panel_C = fig.add_subplot(2,2,3)
    panel_C.plot(t, shorts['blue'], 'k', label='short legs')
    panel_C.plot(t, longs['blue'], color='#AAAAAA', label='long legs')
    panel_C.legend(loc='best')
    panel_C.set_xlim([0, 20])
    panel_C.tick_params(axis='y', colors='blue')
    panel_C.set_xlabel('Times', fontsize=12)
    panel_C.set_ylabel('Total of Seabirds', color='blue')

    panel_D = fig.add_subplot(2,2,4)
    panel_D.plot(t, shorts['green'], 'k', label='short legs')
    panel_D.plot(t, longs['green'], color='#AAAAAA', label='long legs')
    panel_D.legend(loc='best')
    panel_D.set_xlim([0, 20])
    panel_D.tick_params(axis='y', colors='green')
    panel_D.set_xlabel('Times', fontsize=12)
    panel_D.set_ylabel('Total of Seabirds', color='green')

    fig.suptitle('Distribution of Seabirds in the Tropics', y=1)
    fig.set_tight_layout(True) # Avoid panel overlaps
    # fig.set_size_inches(11, 6.5) # Proper size for the figure
    fig.savefig(CONST.MAIN_DIRECTORY + 'birds-dist.pdf') # save in pdf format

    # reset store
    CONST.STORE['agents'] = []
    CONST.STORE['habitats'] = []


# ==============================================================================
# END: Helpers
# ==============================================================================