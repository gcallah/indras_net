#!/usr/bin/env python3

import models.hiv as hiv

def run():
    
    env = hiv.People("People", 25, 25, model_nm="hiv", preact=True, postact=True)

    for i in range(45):
        env.add_agent(hiv.neg("neg" + str[i], "N/A", ))



if __name__ == "__main__":
    run()
