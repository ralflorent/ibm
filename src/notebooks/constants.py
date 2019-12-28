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
# Shared and default values across the project

# ==============================================================================
# START: Constants
# ==============================================================================

# -*- coding: utf-8 -*-
import config

# Loaded configurations
CONFIG = config.CONFIG

# Core elements: unique (used as key identifier)
SHORT_LEGGED = config.name_short_legged
LONG_LEGGED = config.name_long_legged
TOTAL_SHORT_LEGGED = config.total_short_legged
TOTAL_LONG_LEGGED = config.total_long_legged
PROCESSING_TIME = config.processing_time # time limit for the entire process
TIME_DIVISOR = config.time_divisor # time factor to simulate time steps
LAGOON_ORANGE_SM = 'lagoon-orange-sm'
LAGOON_ORANGE_LG = 'lagoon-orange-lg'
LAGOON_BLUE = 'lagoon-blue'
LAGOON_GREEN = 'lagoon-green'
HUMAN_SETTLEMENT = 'human-settlement'
LAGOON_TYPE_ORANGE = '1'
LAGOON_TYPE_BLUE = '2'
LAGOON_TYPE_GREEN = '3'

MOVE_THRESHOLD = 1e-7 # threshold to allow agents' movements driven by the probability

# Restricted areas
AREA_SHORT_LEGGED = (
    LAGOON_ORANGE_SM,
    LAGOON_ORANGE_LG
)

AREA_LONG_LEGGED = (
    LAGOON_ORANGE_SM,
    LAGOON_ORANGE_LG,
    LAGOON_BLUE,
    LAGOON_GREEN
)

# Color palette definition
COLORS = dict()
COLORS[SHORT_LEGGED] = config.color_short_legged
COLORS[LONG_LEGGED] = config.color_long_legged
COLORS[LAGOON_ORANGE_LG] = 'orange'
COLORS[LAGOON_ORANGE_SM] = 'orange'
COLORS[LAGOON_BLUE] = 'blue'
COLORS[LAGOON_GREEN] = 'green'
COLORS[HUMAN_SETTLEMENT] = 'red'

# Labels for patches
LABELS = dict()
LABELS[SHORT_LEGGED] = '{} short legged'.format(TOTAL_SHORT_LEGGED)
LABELS[LONG_LEGGED] = '{} long legged'.format(TOTAL_LONG_LEGGED)
LABELS[LAGOON_ORANGE_SM] = 'Habitat {} (5cm)'.format(LAGOON_TYPE_ORANGE)
LABELS[LAGOON_ORANGE_LG] = 'Habitat {} (5cm)'.format(LAGOON_TYPE_ORANGE)
LABELS[LAGOON_BLUE] = 'Habitat {} (1m)'.format(LAGOON_TYPE_BLUE)
LABELS[LAGOON_GREEN] = 'Habitat {} (40cm)'.format(LAGOON_TYPE_GREEN)
LABELS[HUMAN_SETTLEMENT] = 'Humans'

# Directories (paths)
ROOT_DIR = config.rootDir
OUT_DIR = config.outDir
SAMPLE_DIR = config.sampleDir
GRAPH_DIR = config.graphDir

# In-memory storage
STORE = dict()
STORE['env'] = list()
STORE['agents'] = list()
STORE['habitats'] = list()
STORE['images'] = list()

# Default values for habitats
DEFAULTS = dict()
DEFAULTS['verts'] = dict()
DEFAULTS['verts'][LAGOON_ORANGE_SM] = ((0.70, 0.51),(0.70, 0.86),(0.79, 0.86),(0.79, 0.51),(0.70, 0.51))
DEFAULTS['verts'][LAGOON_ORANGE_LG] = ((0.20, 0.50), (0.20, 0.81), (0.42, 0.81), (0.42, 0.50), (0.20, 0.50))
DEFAULTS['verts'][LAGOON_BLUE] = ((0.22, 0.20), (0.22, 0.40), (0.42, 0.40), (0.42, 0.20), (0.22, 0.40))
DEFAULTS['verts'][LAGOON_GREEN] = ((0.60, 0.05), (0.60, 0.25), (0.70, 0.25), (0.70, 0.05), (0.60, 0.05))
DEFAULTS['verts'][HUMAN_SETTLEMENT+'1'] = ((0.42, 0.67), (0.42, 0.86), (0.61, 0.86), (0.61, 0.67), (0.42, 0.67))
DEFAULTS['verts'][HUMAN_SETTLEMENT+'2'] = ((0.85, 0.70), (0.85, 0.90), (0.95, 0.90), (0.95, 0.70), (0.85, 0.70))
DEFAULTS['verts'][HUMAN_SETTLEMENT+'3'] = ((0.80, 0.15), (0.80, 0.25), (0.90, 0.25), (0.90, 0.15), (0.80, 0.15))

DEFAULTS['props'] = dict()
DEFAULTS['props'][LAGOON_ORANGE_SM] = {'w': 0.05, 's': 80, 'f': 0.3}
DEFAULTS['props'][LAGOON_ORANGE_LG] ={'w': 0.05, 's': 80, 'f': 2.56}
DEFAULTS['props'][LAGOON_BLUE] = {'w': 1.0, 's': 10, 'f': 6.41}
DEFAULTS['props'][LAGOON_GREEN] = {'w': 0.40, 's': 25, 'f': 11.53}

DEFAULTS['rain'] = dict()
DEFAULTS['rain'][0] = 20
DEFAULTS['rain'][10] = 200
DEFAULTS['rain'][20] = 600
DEFAULTS['rain'][30] = 30
DEFAULTS['rain'][40] = 0
DEFAULTS['rain'][50] = 0
# ==============================================================================
# END: Constants
# ==============================================================================