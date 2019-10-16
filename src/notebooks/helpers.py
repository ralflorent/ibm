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


# ==============================================================================
# END: Helpers
# ==============================================================================