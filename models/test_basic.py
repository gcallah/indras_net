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

import json
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
        self.env = bm.BasicEnv(model_nm=MODEL_NM, props=pa)
    
        # Now we loop creating multiple agents
        #  with numbered names based on the loop variable:
        for i in range(pa.get("num_agents")):
            self.env.add_agent(bm.BasicAgent(name="agent" + str(i),
                                        goal="acting up!"))
        self.env.add_agent(bm.BasicAgent(name="agent for tracking",
                                         goal="acting up!"))

    def test_agent_inspect(self):
        agent = self.env.agent_inspect("agent for tracking")
        self.assertEqual(agent.name, "agent for tracking")

    def test_add_agent(self):
        self.env.add_agent(bm.Gozer())
        # test if the add worked!
        # test by running 
        new_agent = self.env.agent_inspect("Gozer the Destructor")
        self.assertIsNotNone(new_agent)

    def test_props_write(self):
        report = True
        self.env.pwrite(self.env.model_nm + ".props")
        props_written = json.load(open(self.env.model_nm + ".props"))
        if len(props_written) != len(self.env.props.props):
            report = False
        if report == True:
            for key in props_written:
                if key not in self.env.props.props:
                    report = False
                    break
                else:
                    if props_written[key] != self.env.props.props[key]:
                        report = False
                        break
        self.assertEquals(report, True)


if __name__ == '__main__':
    main()
