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
SHORT_LEGGED_SEABIRD = 'short-legged'
LONG_LEGGED_SEABIRD  = 'long-legged'

# Path variables
MAIN_DIRECTORY = '../../samples/'
FILEPATH = MAIN_DIRECTORY + 'frame/'

# Miscellaneous variables
IMAGE_STORAGE = []  # images to become gif
PROCESSING_TIME = 50 # time limit for the entire process
THRESHOLD = 1e-7 # threshold to allow agents' movements driven by the probability

# Matplotlib Patches variables
HABITAT_1A_VERTICES = [
    (0.70, 0.51), # left, bottom
    (0.70, 0.86), # left, top
    (0.79, 0.86), # right, top
    (0.79, 0.51), # right, bottom
    (0.70, 0.51)  # ignored (end of polyline)
]
HABITAT_1B_VERTICES = [(0.20, 0.50), (0.20, 0.81), (0.42, 0.81), (0.42, 0.50), (0.20, 0.50)]
HABITAT_2_VERTICES  = [(0.10, 0.20), (0.10, 0.40), (0.40, 0.40), (0.40, 0.20), (0.10, 0.40)]
HABITAT_3_VERTICES  = [(0.60, 0.05), (0.60, 0.25), (0.70, 0.25), (0.70, 0.05), (0.60, 0.05)]
HUMAN_STM1_VERTICES = [(0.42, 0.67), (0.42, 0.86), (0.61, 0.86), (0.61, 0.67), (0.42, 0.67)]
HUMAN_STM2_VERTICES = [(0.85, 0.70), (0.85, 0.90), (0.95, 0.90), (0.95, 0.70), (0.85, 0.70)]
HUMAN_STM3_VERTICES = [(0.80, 0.15), (0.80, 0.25), (0.90, 0.25), (0.90, 0.15), (0.80, 0.15)]

# Total of Agents
TOTAL_LONG_LEGGED_SEABIRDS  = 20
TOTAL_SHORT_LEGGED_SEABIRDS = 20

# Seabird can use certain habitats
LONG_LEGGED_SEABIRD_HABITAT_LIMIT  = ['orange-sm', 'orange-lg', 'blue', 'green']
SHORT_LEGGED_SEABIRD_HABITAT_LIMIT = ['orange-sm', 'orange-lg']

# dictionary-based, in-memory Store for sensitivity analysis
STORE = {
    'env': {},
    'agents': [],
    'habitats': []
}

# ==============================================================================
# END: Constants
# ==============================================================================