import numpy as np
from matplotlib.path import Path
import matplotlib.patches as Patches

# omit scripts for patch creation...

def gen_random_point(patches):
    x, y = np.random.rand(2) # initialize random point(x, y): [0-1, 0-1]
    while True:
        found = False # flag to determine when to stop iterating
        for p in patches:
            if p.get_path().contains_point((x, y)):
                found = True
        if not found: break # ice breaker
        x, y = np.random.rand(2) # update point(x, y)
    return (x, y)

# on-the-fly agent class definition
class Agent:
    pass

# create agents
def create_agents(n_agents):
    global patches # make previously created patches available
    agents = []
    for i in range(n_agents):
        agent = Agent()
        agent.type = "short-legged"
        x, y = gen_random_point(patches) # that is not in patch
        agent.x, agent.y = x, y # new position being assinged to this agent
        agents.append(agent) # append (i.e. add) the ith agent into the array 'agents'
    return agents

# omit scripts for plotting...