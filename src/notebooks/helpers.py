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
import numpy as np # arithmetic computations

__doc__ = """
TODO
"""

def gen_rand_point(habitats=[], option=None):
    """ Generate random point that belongs (or not) to a set of patches

    Parameters
    ----------
    habitats: list of Habitat, default []
        a set of patches (polycurve) to draw simple and compound outlines
        consisting of line segments and splines.

    option: string = {'in', 'out', None}, default = None
        determine whether conditioning the random point being generated
        within or out of the patches. If not specified, return just random
        points without considering the patches.

    Returns
    -------
    (x, y): tuple, of shape (2,)
        a vertex (x_coord, y_coord) of unit rectangle from (0,0) to (1,1).
    """
    # initialize random point(x, y) by generating an array of 2 random values
    # between 0 and 1:: [0.1..., 0.4...]
    x, y = np.random.rand(2)

    # flag up a condition to assess points within, or out of the patches
    if option == 'in':
        condition = lambda f: f
    elif option == 'out':
        condition = lambda f: not f
    elif option is None or len(habitats) is 0:
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

    Parameters
    ----------
    habitat : Habitat
        the current habitat
    human_settlements : list, shape(n,)
        the list of created human settlements

    Returns
    -------
    distances : list, shape(n,)
        the corresponding distance between each human settlement and the given
        habitat
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

    Parameters
    ----------
    point : tuple, shape(2,)
        the x- and y-coordinate of the Cartersian plane
    habitats : list
        a group of habitats where this points possibly lives

    Returns
    -------
    result: Habitat, None
        the habitat that contains that point, geometrically speaking

    Notes
    -----
    The habitats in the current setting are not superposed or overlapped, which
    makes that the search returns a unique result (or None if the point is not
    contained in any the habitats).
    """
    for h in habitats:
        if h.contains_point(point):
            return h
    return None


def eval_fn(meta_fn, *args):
    """
    Evaluate a function within the python environment
    The keys required as meta information are:
    'def' : holds the function definition
    'args' : holds the list of arguments of the function, if any
    'deps' : holds the list of dependencies for the function to execute properly

    Parameters
    ----------
    meta_fn : dict
        the meta information required to evaluate a function (def, args, deps)
    *args
        additional argument values for the existing argument of the function
        definition. If no args, that means that the function needs no args to
        execute.

    Examples
    --------
    Evaluate a function with no argument or dependencies

    >>> meta = {'def': 'lambda: print("cool evaluation")', 'args': None, 'deps': None }
    >>> eval_fn(meta) # print the value
    cool evaluation

    Evaluate a function with arguments but no dependencies

    >>> meta = {'def': 'lambda x: x**2', 'args': ['x'], 'deps': None }
    >>> eval_fn(meta, 3) # compute square of 3
    9

    Evaluate a function with arguments and dependencies

    >>> meta = {'def': 'lambda x, y: math.pow(x, y)', 'args': ['x', 'y'], 'deps': 'import math' }
    >>> eval_fn(meta, 2, 3) # compute 2 to the power of 3
    8
    >>> eval_fn(meta, *[2, 3]) # compute 2 to the power of 3
    8

    Notes
    -----
    The evaluation of a given function is callable if and only if the conditions
    for running it are proper. Any violation will raise a runtime exception.
    """
    fn_def, fn_args, fn_deps = meta_fn['def'], meta_fn['args'], meta_fn['deps']
    if isinstance(fn_deps, list):
        for dep in fn_deps: exec(dep, globals()) # execute deps if any
    fn = eval(fn_def)

    if not isinstance(fn_args, list) or len(fn_args) == 0: # no args required
        return fn()
    elif len(fn_args) == len(args):
        kwargs = dict(zip(fn_args, args)) # zip into keyworded args: {'k': v, ...}
        return fn(**kwargs)
    else:
        raise RuntimeError(f'Cannot evaluate this function <{fn_def}>. Check required arguments')

# ==============================================================================
# END: Helpers
# ==============================================================================