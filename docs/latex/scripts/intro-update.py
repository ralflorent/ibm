# omit scripts for library import, patch and agent creation

# START: simplest approach for synchronous updates based on lack of resources
def update():
    global patches, agents # make previously created patches and agents available
    sh_patches, lg_pathes = patches[0:2], patches[2:4] # distribute patches for short and long legs
    ag = agents[np.random.randint(len(agents))] # randomly choose an agent to update its status

    # simulating random movements based on agent's type
    if ag.type == 'short-legged':
        _x, _y = gen_random_point(sh_patches)
        # agent is moving within the same area
        if is_in_patch(sh_patches[1], (ag.x, ag.y)): # resourceless patch
            ag.x, ag.y = _x, _y # this agent belongs to the small patch, therefore he can move anywhere
        else: # agent coming from a long-legged patch
            if is_in_patch(sh_patches[0], (_x, _y)): # moving within the same is fine
                ag.x, ag.y = _x, _y
            else:# moving to small-legged patch requires resource availability checks
                pos = [(ag.x, ag.y) for ag in agents if ag.type == 'short-legged']
                count = count_points(sh_patches[1], pos)
                if count < 5: # maximum capacity for short-legged waterbirds
                    ag.x, ag.y = _x, _y
    else:
        _x, _y = gen_random_point(lg_pathes)
        # agent is moving within the same area
        if is_in_patch(lg_pathes[0], (ag.x, ag.y)): # resourceless patch
            ag.x, ag.y = _x, _y # this agent belongs to the small patch, therefore he can move anywhere
        else: # agent coming from long patch
            if is_in_patch(lg_pathes[1], (_x, _y)): # moving within the same is fine
                ag.x, ag.y = _x, _y
            else: # moving to small patch requires resource availability checks
                pos = [(ag.x, ag.y) for ag in agents if ag.type == 'long-legged']
                count = count_points(lg_pathes[0], pos)
                if count < 7: # maximum capacity for long-legged waterbirds
                    ag.x, ag.y = _x, _y
    # END: update