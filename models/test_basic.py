#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""

from unittest import TestCase, main
import sys

import random

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
        # self.env.n_steps(random.randint(10, 20))

    def test_agent_inspect(self):
        agent = self.env.agent_inspect("agent for tracking")
        print("running test 1")
        self.assertEqual(agent.name, "agent for tracking")

    def test_add_agent(self):
        self.env.add_agent(bm.Gozer())
        # test if the add worked!
        # test by running 
        new_agent = self.env.agent_inspect("Gozer the Destructor")
        print("running test 2")
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
        print("running test 3")
        self.assertEquals(report, True)

    def test_population_report(self):
        self.env.n_steps(random.randint(10,20))
        report = True
        self.env.pop_report(self.env.model_nm+".csv")
        f = open(self.env.model_nm+".csv", "r")
        head = f.readline()
        head = head.strip("\n")
        head_list = head.split(",")
        print("check1!!!!!!!", head_list)
        dic_for_reference = self.env.agents.get_pop_hist()
        print("check2!!!!!!!", dic_for_reference)
        for i in head_list:
            if i not in dic_for_reference:
                report = False
                break
        if report == True:
            dic_for_check = {}
            for i in head_list:
                dic_for_check[i] = []
            print("check3!!!!!!!", dic_for_check)
            for line in f:
                line = line.strip("\n")
                line_list = line.split(",")
                if len(line_list)==len(head_list):
                    for i in range(len(line_list)):
                        dic_for_check[head_list[i]].append(int(line_list[i]))
                else:
                    report = False
                    break
            print("check4!!!!!!!", dic_for_check)

        if report == True:
            if len(dic_for_check) != len(dic_for_reference):
                report = False
            if report is True:
                for key in dic_for_check:
                    if dic_for_check[key] != dic_for_reference[key]["data"]:
                        report = False
                        break
        self.assertEquals(report, True)

    def test_list_agents(self):
        report = True
        orig_out = sys.stdout
        sys.stdout = open("checkfile.txt", "w")
        self.env.list_agents()
        sys.stdout.close()
        sys.stdout = orig_out
        f = open("checkfile.txt", "r")
        f.readline()
        for agent in self.env.agents:
            line = f.readline()
            line_list = line.split(" with a goal of ")
            line_list[1] = line_list[1].strip()
            if agent.name != line_list[0] or agent.goal != line_list[1]:
                report = False
                break
        self.assertEquals(report, True)

    def test_display_props(self):
        report = True
        orig_out = sys.stdout
        sys.stdout = open("checkprops.txt", "w")
        self.env.disp_props()
        sys.stdout.close()
        sys.stdout = orig_out
        f = open("checkprops.txt", "r")
        title = f.readline()
        title_list = title.split("for")
        if self.env.model_nm != title_list[1].strip():
            report = False
        dic_for_check = {}
        if report is True:
            for line in f:
                if line != "\n":
                    line_list = line.split(": ")
                    line_list[0] = line_list[0].strip()
                    line_list[1] = line_list[1].strip()
                    dic_for_check[line_list[0]] = line_list[1]
        if dic_for_check != self.env.props.props:
            report = False

if __name__ == '__main__':
    main()
