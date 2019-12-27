import matplotlib.patches as Patches
from matplotlib.path import Path

# vertices of the rectangle
verts = [
    (0.2, 0.2), # left, bottom
    (0.2, 0.4), # left, top
    (0.4, 0.4), # right, top
    (0.4, 0.2), # right, bottom
    (0.2, 0.4), # ignored
]

# how to draw the lines
codes = [
    Path.MOVETO, # start designing here
    Path.LINETO, # draw line to
    Path.LINETO, # draw line to
    Path.LINETO, # draw line to
    Path.CLOSEPOLY,# finish polycurve here
]

# create the final plottable rectangle
path = Path(verts, codes)
patch = Patches.PathPatch(path, facecolor='b', alpha=0.5, lw=2)

# omit scripts for plotting