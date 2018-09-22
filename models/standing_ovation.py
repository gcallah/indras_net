#Model of the spread of a Standing Ovation for a performance

#Agent( )
    #agent state = sitting, standing
    #neighbors = left, right, three agents in front, five agents in front of that, etc.
            #   * A *
            #   * * *
            # * * * * *
        #if >50% neighbors' state = standing
            #agent state = standing
        #else if >50% neighbors' state = sitting
            #agent state = sitting
    #perceived quality of performance q_val = random floating point [0, 1]
        #If q_val > threshold (default 0.5)
            # agent state = standing

#Variables( )
    #cone-length = int [1, 20]
        #how far neighborhood will extend (1 = 5, 2 = 10)
    #noise = float [0, 1]
        #probability that each agent will change state after revising
        