#Model of the spread of a Standing Ovation for a performance

#Variables set by the user
    #Global Vars
        #auditorium_height
            #int
            #[1, 60]
        #auditorium_width
            #int
            #[1, 80]
        #cone_length
            #int
            #[1, auditorium_length]
        #threshold
            #float
            #[0, 1]
    #Agent Vars
        #noise
            #float
            #[0, 1]

#Agent_Array
    #array with all agents in a width x height array

#Agent( )
    #state
        #string
        #"SITTING", "STANDING"
    #neighbors
        #neighbors will have to be built through a build_neighbors() func
        #list
        #agent left [x-1], agent right [x+1], agent front [y+1], agent front left [x-1][y+1], etc.
            #   * A *
            #   * * *
            # * * * * *
    #if >50% neighbors' state = standing
        #agent state = standing
    #else if >50% neighbors' state = sitting
        #agent state = sitting
    #perceived quality of performance q_val = random floating point [0, 1]
        #If q_val > threshold (default 0.5)
            #agent state = standing