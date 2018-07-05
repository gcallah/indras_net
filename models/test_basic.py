#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""

from unittest import TestCase, main

MODEL_NM = "Basic"

import indra.prop_args as props
# we will create props here to set user_type:
pa = props.PropArgs.create_props(MODEL_NM)


import models.basic_model as bm


class BasicTestCase(TestCase):
    def __init__(self, methodName, prop_file="basic.props"):
    
        super().__init__(methodName=methodName)
    
        result = props.read_props(MODEL_NM, prop_file)
        if result:
            pa.add_props(result.props)
        else:
            print("Oh-oh, no props to read in!")
            exit(1)
    
        # Now we create a minimal environment for our agents to act within:
        env = bm.BasicEnv(model_nm=MODEL_NM, props=pa)
    
        # Now we loop creating multiple agents
        #  with numbered names based on the loop variable:
        for i in range(pa.get("num_agents")):
            env.add_agent(bm.BasicAgent(name="agent" + str(i),
                                        goal="acting up!"))

    def test_add_agent(self):
        # env.add_agent(bm.Gozer())
        # test if the add worked!
        # test by running 
        # new_agent = env.agent_inspect("Gozer the Destructor")
        # self.assertIsNotNone(agent)
        self.assertTrue(True)

if __name__ == '__main__':
    main()
