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

# Agents' configurations
CNF_AG = CONFIG['app']['agents']
TOTAL_AGENTS = sum([ag_cnf['quantity'] for ag_cnf in CNF_AG])

# Core elements: unique (used as key identifier)
PROCESSING_TIME = CONFIG['app']['counter'] # time limit for the entire process
TIME_DIVISOR = CONFIG['app']['rain']['divisor']

LAGOON_ORANGE_SM = 'lagoon-orange-sm'
LAGOON_ORANGE_LG = 'lagoon-orange-lg'
LAGOON_BLUE = 'lagoon-blue'
LAGOON_GREEN = 'lagoon-green'
HUMAN_SETTLEMENT = 'human-settlement'
LAGOON_TYPE_ORANGE = '1'
LAGOON_TYPE_BLUE = '2'
LAGOON_TYPE_GREEN = '3'

THRESHOLD = CONFIG['app']['threshold'] # threshold to allow agents' movements driven by the probability

# Color palette definition
COLORS = dict()
COLORS[LAGOON_ORANGE_LG] = 'orange'
COLORS[LAGOON_ORANGE_SM] = 'orange'
COLORS[LAGOON_BLUE] = 'blue'
COLORS[LAGOON_GREEN] = 'green'
COLORS[HUMAN_SETTLEMENT] = 'red'

# Labels for patches
LABELS = dict()
LABELS[LAGOON_ORANGE_SM] = 'Habitat {} (5cm)'.format(LAGOON_TYPE_ORANGE)
LABELS[LAGOON_ORANGE_LG] = 'Habitat {} (5cm)'.format(LAGOON_TYPE_ORANGE)
LABELS[LAGOON_BLUE] = 'Habitat {} (1m)'.format(LAGOON_TYPE_BLUE)
LABELS[LAGOON_GREEN] = 'Habitat {} (40cm)'.format(LAGOON_TYPE_GREEN)
LABELS[HUMAN_SETTLEMENT] = 'Humans'
for ag_cnf in CNF_AG:
    LABELS[ag_cnf['type']] = ag_cnf['label']

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

# helpers
def get_agentp(_type, prop):
    for ag_cnf in CNF_AG:
        if ag_cnf['type'] == _type:
            return ag_cnf[prop]
# ==============================================================================
# END: Constants
# ==============================================================================