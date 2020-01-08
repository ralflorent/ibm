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
import matplotlib.patches as mpatches
from matplotlib.path import Path

# ------------------------------------------------------------------------------
# Habitat class definition
class Habitat:
    """
    A patch-focused drawing representation of the lagoons, rectangularly shaped
    and based on additional design settings.

    Parameters
    ----------
    _id : string
        a key identifier that adds uniqueness to a patch object
    _type : string
        a category name in order to group lagoons that share similarities
    _color : string
        the color representation of the lagoon within the system (design focus)
    label : string
        the tag description used to label the lagoon (design focus)
    verts : tuple of shape(5, 2)
        the vertices for the patch based on matplotlib's artist
    codes : list
        the lines describing the polycurve of the artist
    desc : string
        a long description
    props : dict
        the environmental characteristics a lagoon (water depth, salinity, food
        or prey availability, minimal distance to human settlements, etc.)
    artist :
        the final artist built upon the given design setting

    Examples
    --------
    Construct a habitat
    >>> habitat = Habitat('habitat-id-1', '1', 'blue')
    >>> habitat.verts = ((0.7, 0.5),(0.7, 0.9),(0.6, 0.9),(0.6, 0.5),(0.7, 0.5))
    >>> habitat.props = {'w': 0.05, 's': 80, 'f': 0.3}
    >>> habitat.desc = 'some long description'
    >>> habitat.label = 'an example of label'
    >>> habitat.build() # build an artist in memory, ready for plotting

    Plot a habitat (built artist)
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure(1)
    >>> ax  = fig.add_subplot(111)
    >>> ax.add_patch(habitat.artist) # omit additional settings for plots
    >>> plt.show()

    """
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
        """ Build an artist in memory based on how it was constructed.

        Parameters
        ----------
        color : string, None
            the color used to override the existing color representation of a
            habitat that will be built up.
        fill : boolean
            If True, the color will be applied to the entire area of the artist.
            Otherwise, only the edge of the figure(artist) will be colored.

        Returns
        -------
        artist : PathPatch <matplotlib.patches>
            the created artist

        Notes
        -----
        See ref: https://matplotlib.org/users/path_tutorial.html for more info.
        """
        c = color if color is not None else self.color
        path = Path(self.verts, self.codes)
        self.artist = mpatches.PathPatch(
            path, label=self.label,
            ec=c, fc=c, fill=fill, alpha=0.5
        )
        return self.artist


    def contains_point(self, point):
        """ Check if a point belongs to this specific patch """
        return self.artist.get_path().contains_point(point)


    def get_center(self):
        """ Compute the center point of the rectangularly-shaped patch

        Notes
        -----
        The center of rectangle is the mid point of the diagonal
        end points of a rectangle ABCD.

        Returns
        -------
        point: tuple
            the x- and y-coordinate representing the center point of a given
            retangular patch
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