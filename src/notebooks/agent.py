# Individual-Based Modeling (IBM)
#
# Created on October 12, 2019
#
# Authors:
#   Ralph Florent <r.florent@jacobs-university.de>
#   Davi Tavares <davi.tavares@leibniz-zmt.de>
#   Agostino Merico <a.merico@jacobs-university.de>
#
# Class definition for the Agents of the system

# ==============================================================================
# START: Agent class definition
# ==============================================================================

# -*- coding: utf-8 -*-
from collections.abc import Iterable

# ------------------------------------------------------------------------------
# Agent class definition
class Agent:
    """
    Categorized by the length of their legs, a drawing representation of the
    waterbirds inhabiting the lagoons.

    Parameters
    ----------
    _type : string
        the category name treated as unique to identify waterbirds that share
        the same leg's length.
    x : float, default 0.0
        the x-coordinate in a Cartesian plane as part of a waterbird's position
    y : float, default 0.0
        the y-coordinate in a Cartesian plane as part of a waterbird's position
    name : string
        the name associated to a waterbird. It is also used a unique key
        identifier.
    color : string
        the color representation of the agent within the system (design focus)

    Notes
    -----
    Though set separately in the constructor, the x and y coordinates are then
    handled as a point(x, y). Internally, x and y are private properties and
    cannot be used afterwards. For that, it exists a getter and setter for the
    point that gives more control over how these values are passed in the future
    after instantiating an agent.

    Examples
    --------
    Construct an agent
    >>> agent = Agent('15cm', 0.12, 0.53)
    >>> agent.name = 'agent-1-1cm'
    >>> agent.color = '#afaf3a'

    Obtain agent's current position
    >>> agent.get_point()
    (0.12, 0.53)

    Update an agent's position
    >>> point = (0.67454, 0.89237)
    >>> agent.set_point(point)
    """
    def __init__(self, _type, x=0.0, y=0.0):
        self.type = _type
        self.color = ''
        self.name = ''

        self.__x = x
        self.__y = y
        self.__point = (x, y)

    def set_point(self, point):
        """
        Setter for the point property

        Parameters
        ----------
        point : tuple of shape (2,)
            the x and y coordinates. Must be float values.
        """
        if not isinstance(point, Iterable): # point: (x, y)
            raise TypeError(f'the argument {point} is not iterable.')
        if len(point) != 2:
            raise TypeError(f'the argument {point} must contain 2 elements.')
        self.__x, self.__y = point
        self.__point = tuple(point)

    def get_point(self):
        """Getter for the point property"""
        return self.__point

# ==============================================================================
# END: Agent class definition
# ==============================================================================