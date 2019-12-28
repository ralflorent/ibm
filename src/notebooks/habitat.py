# Individual-Based Modeling (IBM)
#
# Created on October 12, 2019
#
# Authors:
#   Ralph Florent <r.florent@jacobs-university.de>
#   Davi Tavares <davi.tavares@leibniz-zmt.de>
#   Agostino Merico <a.merico@jacobs-university.de>
#
# Class definition for the Habitats of the system

# ==============================================================================
# START: Habitat class definition
# ==============================================================================

# -*- coding: utf-8 -*-
import matplotlib.patches as Patches
from matplotlib.path import Path

# This class will represent the habitats or patches of the system
class Habitat:
    def __init__(self, _id, _type, _color):
        self.id = _id
        self.type = _type
        self.color = _color

        self.label = ''
        self.verts = ()
        self.desc = ''
        self.props = {}
        self.codes = [
            Path.MOVETO,    # start polycurve here (top-left)
            Path.LINETO,    # draw line to (top-right)
            Path.LINETO,    # draw line to (bottom-right)
            Path.LINETO,    # draw line to (bottom-left)
            Path.CLOSEPOLY, # finish polycurve here (top-left)
        ]
        self.artist = None


    def build(self, color=None, fill=False):
        """ Create a set of patches within a specific area

        TODO: proper docs
        ref: https://matplotlib.org/users/path_tutorial.html
        """
        c = color if color is not None else self.color
        path = Path(self.verts, self.codes)
        self.artist = Patches.PathPatch(
            path, label=self.label,
            ec=c, fc=c, fill=fill, alpha=0.5
        )
        return self.artist


    def contains_point(self, point):
        """ Check if a point belongs to this specific patch
        TODO: proper docs
        """
        path = self.artist.get_path()
        return path.contains_point(point)


    def get_center(self):
        """ Compute the center point of the rectangle

        The center of rectangle is the mid point of the diagonal
        end points of a rectangle ABCD.

        TODO: proper docs
        """
        _x, _y = 0, 0
        if len(self.verts) < 4:
            return (_x, _y)

        A, B, D = self.verts[0], self.verts[1], self.verts[3]
        _x = (A[0] + D[0]) / 2 # width
        _y = (A[1] + B[1]) / 2 # height
        return (_x, _y)

# ==============================================================================
# END: Habitat class definition
# ==============================================================================