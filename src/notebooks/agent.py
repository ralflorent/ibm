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

# This class will represent the seabirds of the system
class Agent:
    def __init__(self, _type, x=0.0, y=0.0):
        self.type = _type
        self.color = ''
        self.name = ''

        self.__x = x
        self.__y = y
        self.__point = (x, y)

    def set_point(self, point):
        if not isinstance(point, Iterable): # point: (x, y)
            raise TypeError(f'the argument {point} is not iterable.')
        if len(point) != 2:
            raise TypeError(f'the argument {point} must contain 2 elements.')
        self.__x, self.__y = point
        self.__point = tuple(point)

    def get_point(self):
        return self.__point

# ==============================================================================
# END: Agent class definition
# ==============================================================================