# Individual-Based Modeling (IBM)
#
# Created on October 12, 2019
#
# Authors:
#   Ralph Florent <r.florent@jacobs-university.de>
#   Davi Tavares <davi.tavares@leibniz-zmt.de>
#   Agostino Merico <a.merico@jacobs-university.de>
#
# Shared and default values across the project

# ==============================================================================
# START: Constants
# ==============================================================================

# -*- coding: utf-8 -*-

# Core elements
SHORT_LEGGED = 'short-legged'
LONG_LEGGED = 'long-legged'
TOTAL_LONG_LEGGED  = 20
TOTAL_SHORT_LEGGED = 20
PROCESSING_TIME = 12 # time limit for the entire process
TIME_DIVISOR = 10 # time factor to simulate time steps
LAGOON_ORANGE_SM = 'orange-sm'
LAGOON_ORANGE_LG = 'orange-lg'
LAGOON_BLUE = 'blue'
LAGOON_GREEN = 'green'
HUMAN_SETTLEMENT = 'human'
MOVE_THRESHOLD = 1e-7 # threshold to allow agents' movements driven by the probability

AREA_SHORT_LEGGED = (
    LAGOON_ORANGE_SM,
    LAGOON_ORANGE_LG,
    LAGOON_BLUE,
    LAGOON_GREEN
)

AREA_LONG_LEGGED = (
    LAGOON_ORANGE_SM,
    LAGOON_ORANGE_LG
)

COLORS = dict()
COLORS[SHORT_LEGGED] = '#000000'
COLORS[LONG_LEGGED] = '#AAAAAA'

ROOT_DIR = '../../samples/' # TODO: handle file system
SAMPLE_DIR = ROOT_DIR + 'frame/'

STORE = dict() # in-memory store for sensitivity analysis
STORE['env'] = list()
STORE['agents'] = list()
STORE['habitats'] = list()
STORE['images'] = list()

DEFAULTS = dict()
DEFAULTS['verts'] = dict()
DEFAULTS['verts'][LAGOON_ORANGE_SM] = ((0.70, 0.51),(0.70, 0.86),(0.79, 0.86),(0.79, 0.51),(0.70, 0.51))
DEFAULTS['verts'][LAGOON_ORANGE_LG] = ((0.20, 0.50), (0.20, 0.81), (0.42, 0.81), (0.42, 0.50), (0.20, 0.50))
DEFAULTS['verts'][LAGOON_BLUE] = ((0.10, 0.20), (0.10, 0.40), (0.40, 0.40), (0.40, 0.20), (0.10, 0.40))
DEFAULTS['verts'][LAGOON_GREEN] = ((0.60, 0.05), (0.60, 0.25), (0.70, 0.25), (0.70, 0.05), (0.60, 0.05))
DEFAULTS['verts'][HUMAN_SETTLEMENT+'1'] = ((0.42, 0.67), (0.42, 0.86), (0.61, 0.86), (0.61, 0.67), (0.42, 0.67))
DEFAULTS['verts'][HUMAN_SETTLEMENT+'2'] = ((0.85, 0.70), (0.85, 0.90), (0.95, 0.90), (0.95, 0.70), (0.85, 0.70))
DEFAULTS['verts'][HUMAN_SETTLEMENT+'3'] = ((0.80, 0.15), (0.80, 0.25), (0.90, 0.25), (0.90, 0.15), (0.80, 0.15))

DEFAULTS['props'] = dict()
DEFAULTS['props'][LAGOON_ORANGE_SM] = {'w': 0.05, 's': 80, 'f': 0.3}
DEFAULTS['props'][LAGOON_ORANGE_LG] ={'w': 0.05, 's': 80, 'f': 2.56}
DEFAULTS['props'][LAGOON_BLUE] = {'w': 1.0, 's': 10, 'f': 6.41}
DEFAULTS['props'][LAGOON_GREEN] = {'w': 0.40, 's': 25, 'f': 11.53}

CONFIG = dict() # TODO: should be loaded from yaml
# ==============================================================================
# END: Constants
# ==============================================================================