# omit imports and helpers
def update_one(habitats, agent):
    """ Update agent in one unit of time
    d: distance between the current habitat and the closest human settlement
    w: water depth of the current habitat
    s: salinity of the current habitat
    f: food availability in the current habitat
    """
    human_settlements = [h for h in habitats if h.id == C.HUMAN_SETTLEMENT]
    prob = 0.0

    for ag_cnf in C.CNF_AG: # for each category of agent (e.g., 15cm legged)
        restricted_habs = [] # this agent can use certain areas only

        for _type in ag_cnf['habs']:
            for hab in habitats:
                if hab.type == _type:
                    restricted_habs.append(hab) # are these limited areas
                    break

        if agent.type == ag_cnf['type']: # do's and dont's specific to this agent
            _x, _y = gen_rand_point(restricted_habs, 'in')
            _habitat = which_habitat((_x, _y), restricted_habs)
            _d = compute_dist(_habitat, human_settlements)
            min_index = _d.index( min(_d) ) # consider minimal distance

            # specific characteristics (props) of the selected habitat
            d = _d[min_index] # minimal distance to human settlement
            w, s, f = _habitat.props.values() # water depth, salinity, food

            # this agent knows a specific way to compute certain operations
            w_meta_fn = C.get_agentp(agent.type, 'fn')

            # compute the probability of moving to this habitat
            prob_w = eval_fn(w_meta_fn, w) # evaluate, compute the probability
            prob_d = -0.0013 * d**2 + 0.0074 * d - 0.0001 # missing eval_fn
            prob_s = 0.00006 * s**2 + 0.0002 * s + 0.0004 # missing eval_fn
            prob_f = (0.00673 * f**2) - (0.002936 * f) + 0.5 # missing eval_fn
            prob = prob_s * prob_w * prob_d * prob_f

        if prob > C.THRESHOLD:
            agent.set_point((_x, _y)) # allocate new position to the agent
    return agent, _habitat