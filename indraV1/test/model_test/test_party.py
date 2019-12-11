#!/usr/bin/env python3
VALUE = "val"
QUESTION = "question"
DEFAULT_VAL = "default_val"
ATYPE = "atype"
HIVAL = "hival"
LOWVAL = "lowval"

from unittest import TestCase, main
import sys
import indra.user as user
import random
from collections import deque

MODEL_NM = "party"

import indra.prop_args2 as props

import json
import models.party as pm
import os
from datetime import date


def announce(name):
    present = date.today()
    print("Running " + name + " at " + str(present), file=sys.stderr)


# make sure to run test file from root directory!
class BasicTestCase(TestCase):
    def __init__(self, methodName, prop_file="models/party_for_test.props"):
        super().__init__(methodName=methodName)

        self.pa = props.read_props(MODEL_NM, prop_file)

        # Now we create a forest environment for our agents to act within:
        if self.pa["user_type"] == props.WEB:
            self.pa["base_dir"] = os.environ['base_dir']

        # Now we create an environment for our agents to act within:
        self.env = pm.PartyEnv("A cocktail party",
                          self.pa["grid_width"],
                          self.pa["grid_height"],
                          model_nm=self.pa.model_nm,
                          props=self.pa)

        for i in range(self.pa["num_men"]):
            self.env.add_agent(pm.Man(name="Man" + str(i),
                                 goal="A good party.",
                                 tol=0.5,
                                 max_detect=self.pa['max_detect']))

        for i in range(self.pa["num_women"]):
            self.env.add_agent(pm.Woman(name="Woman" + str(i),
                                   goal="A good party.",
                                   tol=0.5,
                                   max_detect=self.pa['max_detect']))

        self.env.add_agent(pm.Woman(name="Woman for tracking",
                                         goal="A good party.",
                                         tol=0.5,
                                         max_detect=self.pa['max_detect']))

    def test_agent_inspect(self):
        announce('test_agent_inspect')
        agent = self.env.agent_inspect("Woman for tracking")
        self.assertEqual(agent.name, "Woman for tracking")

    def test_add_agent(self):
        announce('test_add_agent')
        self.env.add_agent(pm.Woman(name="new added Woman",
                                         goal="A good party.",
                                         tol=0.5,
                                         max_detect=self.pa['max_detect']))
        # test if the add worked!
        # test by running
        new_agent = self.env.agent_inspect("new added Woman")
        self.assertIsNotNone(new_agent)

    def test_props_write(self):
        announce('test_props_write')
        report = True
        self.env.pwrite(self.env.model_nm + ".props")
        with open(self.env.model_nm + ".props", "r") as f:
            props_written = json.load(f)
        if len(props_written) != len(self.env.props.props):
            report = False
        if report:
            for key in props_written:
                if key not in self.env.props.props:
                    report = False
                    break
                else:
                    if props_written[key]["val"] != self.env.props.props[key].val:
                        report = False
                        break
        f.close()
        os.remove(self.env.model_nm + ".props")
        self.assertEqual(report, True)

    def test_step(self):
        announce('test_step')
        report = True
        period_before_run = self.env.period
        self.env.step()
        period_after_run = self.env.period
        if period_before_run + 1 != period_after_run:
            report = False
        self.assertEqual(report, True)

    def test_n_step(self):
        announce('test_n_step')
        report = True
        period_before_run = self.env.period
        random_steps = random.randint(3,30)
        self.env.n_steps(random_steps)
        period_after_run = self.env.period
        if (period_before_run + random_steps) != period_after_run:
            report = False
        self.assertEqual(report, True)

    def test_population_report(self):
        announce('test_population_report')
        # need to test step method first!!!!!!!!!!!!
        self.env.n_steps(random.randint(10,20))
        report = True
        self.env.pop_report(self.env.model_nm+".csv")
        f = open(self.env.model_nm+".csv", "r")
        head = f.readline()
        head = head.strip("\n")
        head_list = head.split(",")
        # print("check1!!!!!!!", head_list)
        dic_for_reference = self.env.agents.get_pop_hist()
        # print("check2!!!!!!!", dic_for_reference)
        for i in head_list:
            if i not in dic_for_reference:
                report = False
                break
        if report:
            dic_for_check = {}
            for i in head_list:
                dic_for_check[i] = []
            # print("check3!!!!!!!", dic_for_check)
            for line in f:
                line = line.strip("\n")
                line_list = line.split(",")
                if len(line_list)==len(head_list):
                    for i in range(len(line_list)):
                        dic_for_check[head_list[i]].append(int(line_list[i]))
                else:
                    report = False
                    break
            # print("check4!!!!!!!", dic_for_check)

        if report:
            if len(dic_for_check) != len(dic_for_reference):
                report = False
            if report is True:
                for key in dic_for_check:
                    if dic_for_check[key] != dic_for_reference[key]["data"]:
                        report = False
                        break
        f.close()
        os.remove(self.env.model_nm + ".csv")
        self.assertEqual(report, True)

    def test_list_agents(self):
        announce('test_list_agents')
        report = True
        orig_out = sys.stdout
        sys.stdout = open("checkfile.txt", "w")
        self.env.list_agents()
        sys.stdout.close()
        sys.stdout = orig_out
        f = open("checkfile.txt", "r")
        line1 = f.readline()

        for agent in self.env.agents:
            line = f.readline()
            line_list = line.split(" with a goal of ")

            line_list[1] = line_list[1].strip()
            if agent.name != line_list[0] or agent.goal != line_list[1]:
                report = False
                break
        f.close()
        os.remove("checkfile.txt")
        self.assertEqual(report, True)

    def test_display_props(self):
        announce('test_display_props')
        report = True
        orig_out = sys.stdout
        sys.stdout = open("checkprops.txt", "w")
        self.env.disp_props()
        sys.stdout.close()
        sys.stdout = orig_out
        f = open("checkprops.txt", "r")
        title = f.readline()
        title_list = title.split(" for ")
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

            for key in self.env.props.props:
                if str(self.env.props.props[key]) != dic_for_check[key]:
                    report = False
        f.close()
        os.remove("checkprops.txt")
        self.assertEqual(report, True)

    def test_examine_log(self):
        announce('test_examine_log')
        report = True
        logfile_name = self.env.props.props["log_fname"].val
        list_for_reference = deque(maxlen=16)

        with open(logfile_name, 'rt') as log:
            for line in log:
                list_for_reference.append(line)
        orig_out = sys.stdout
        sys.stdout = open("checklog.txt", "w")
        self.env.disp_log()
        sys.stdout.close()
        sys.stdout = orig_out
        f = open("checklog.txt", "r")
        first_line = f.readline().strip()
        first_line = first_line.split(" ")
        if logfile_name != first_line[-1]:
            report = False
        if report:
            for i, line in enumerate(f):
                if list_for_reference[i] != line:
                    report = False
                    break
        f.close()

        os.remove("checklog.txt")

        self.assertEqual(report, True)

    def test_save_session(self):
        announce('test_save_session')
        report = True
        rand_sess_id = random.randint(1, 10)
        try:
            base_dir = self.env.props["base_dir"]
        except:
            base_dir = ""
        self.env.save_session(rand_sess_id)

        path = base_dir + "json/" + self.env.model_nm + str(rand_sess_id) + ".json"
        with open(path, "r") as f:
            json_input = f.readline()
            json_input_dic = json.loads(json_input)
        if json_input_dic["period"] != self.env.period:
            report = False
        if json_input_dic["model_nm"] != self.env.model_nm:
            report = False
        if json_input_dic["preact"] != self.env.preact:
            report = False
        if json_input_dic["postact"] != self.env.postact:
            report = False
        if json_input_dic["props"] != self.env.props.to_json():
            report = False
        #Here is why test_save_session fail before.
        #The env will generate a new prop_arg 2 type proparg when restoring
        #session(check env.from_json function), but
        # we were using old prop_arg in this test file.
        if json_input_dic["user"] != self.env.user.to_json():
            report = False
        agents = []
        for agent in self.env.agents:
            agents.append(agent.to_json())
        # print(json_input_dic["agents"][0])
        # print(type(agents[0]))
        # if json_input_dic["agents"] != agents:
        #     report = False
        # Problem: the 'state_pre' attribute returned from json has a list in it.
        # The origin al one should be a tuple

        f.close()
        os.remove(path)

        self.assertEqual(report, True)

    def test_restore_session(self):
        announce('test_restore_session')
        report = True
        # print("check0!!!", self.env.props.props)
        rand_sess_id = random.randint(1, 10)
        try:
            base_dir = self.env.props["base_dir"]
        except:
            base_dir = ""
        self.env.save_session(rand_sess_id)
        # make sure the session we want to restore is different
        #  from our current env status
        self.env.n_steps(random.randint(1,10))
        self.env.restore_session(rand_sess_id)

        path = base_dir + "json/" + self.env.model_nm + str(rand_sess_id) + ".json"
        with open(path, "r") as f:
            json_input = f.readline()
        json_input_dic = json.loads(json_input)
        if json_input_dic["period"] != self.env.period:
            report = False
        if json_input_dic["model_nm"] != self.env.model_nm:
            report = False
        if json_input_dic["preact"] != self.env.preact:
            report = False
        if json_input_dic["postact"] != self.env.postact:
            report = False
        if json_input_dic["props"] != self.env.props.to_json():
            report = False
        if json_input_dic["user"] != self.env.user.to_json():
            report = False
        agents = []
        for agent in self.env.agents:
            agents.append(agent.to_json())
        # if json_input_dic["agents"] != agents:
        #     report = False
        #Problem: same as last test function

        # print("check1!!!", self.env.props.props)
        # print("check2!!!!", json_input_dic["props"])

        os.remove(path)
        f.close()
        os.remove("party.log")

        self.assertEqual(report, True)

if __name__ == '__main__':
    announce("main")
    main()