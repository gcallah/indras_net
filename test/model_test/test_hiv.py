#!/usr/bin/env python3

from unittest import TestCase, main
import sys
import random
from collections import deque
import indra.prop_args2 as props
import json
import models.hiv as hiv
from models.hiv_run import INI_INFECTED_PCT
from models.hiv_run import STD_COUP_TEND
from models.hiv_run import STD_TEST_FREQ
from models.hiv_run import STD_COMMITMENT
from models.hiv_run import STD_CONDOM_USE
import os
from datetime import date
import numpy

VALUE = "val"
QUESTION = "question"
DEFAULT_VAL = "default_val"
ATYPE = "atype"
HIVAL = "hival"
LOWVAL = "lowval"
MODEL_NM = "hiv"


def announce(name):
    present = date.today()
    print("Running " + name + " at " + str(present), file=sys.stderr)


# make sure to run test file from root directory!
class BasicTestCase(TestCase):
    def __init__(self, methodName, prop_file="models/hiv_for_test.props"):
        super().__init__(methodName=methodName)

        self.pa = props.read_props(MODEL_NM, prop_file)

        # Now we create a forest environment for our agents to act within:
        self.env = hiv.People("People", self.pa["grid_width"],
                              self.pa["grid_height"], model_nm=MODEL_NM,
                              preact=True, postact=True, props=self.pa)

        self.max_ppl = self.pa["grid_width"] * self.pa["grid_height"]
        if self.pa["ini_ppl"] > self.max_ppl:
            self.ini_ppl = self.max_ppl
        else:
            self.ini_ppl = self.pa["ini_ppl"]
        self.ini_infected_ppl = round(INI_INFECTED_PCT * self.ini_ppl)
        self.ini_healthy_ppl = self.ini_ppl - self.ini_infected_ppl

        self.coup_tend = numpy.random.normal(self.pa["avg_coup_tend"],
                                             STD_COUP_TEND, self.ini_ppl)
        self.test_freq = numpy.random.normal(self.pa["avg_test_freq"],
                                             STD_TEST_FREQ, self.ini_ppl)
        self.commitment = numpy.random.normal(self.pa["avg_commitment"],
                                              STD_COMMITMENT, self.ini_ppl)
        self.condom_use = numpy.random.normal(self.pa["avg_condom_use"],
                                              STD_CONDOM_USE, self.ini_ppl)
        for i in range(self.ini_ppl):
            if self.coup_tend[i] < 0:
                self.coup_tend[i] = 0
            elif self.coup_tend[i] > 10:
                self.coup_tend[i] = 10
            if self.test_freq[i] < 0:
                self.test_freq[i] = 0
            elif self.test_freq[i] > 2:
                self.test_freq[i] = 2
            if self.commitment[i] < 1:
                self.commitment[i] = 1
            elif self.commitment[i] > 200:
                self.commitment[i] = 200
            if self.condom_use[i] < 0:
                self.condom_use[i] = 0
            elif self.condom_use[i] > 10:
                self.condom_use[i] = 10

        for i in range(self.ini_infected_ppl):
            rand_inf_len = random.randint(0, hiv.SYMPTOMS_SHOW-1)
            new_agent = hiv.Person(name="person" + str(i),
                                   infected=True,
                                   infection_length=rand_inf_len,
                                   initiative=i,
                                   coupling_tendency=self.coup_tend[i],
                                   test_frequency=self.test_freq[i],
                                   commitment=self.commitment[i],
                                   condom_use=self.condom_use[i])
            self.env.add_agent(new_agent)
        for i in range(self.ini_healthy_ppl):
            j = self.ini_infected_ppl+i
            new_agent = hiv.Person(name="person"+str(j),
                                   infected=False, infection_length=0,
                                   initiative=j,
                                   coupling_tendency=self.coup_tend[j],
                                   test_frequency=self.test_freq[j],
                                   commitment=self.commitment[j],
                                   condom_use=self.condom_use[j])
            self.env.add_agent(new_agent)

    def test_agent_inspect(self):
        announce('test_agent_inspect')
        agent = self.env.agent_inspect("person0")
        self.assertEqual(agent.name, "person0")

    def test_add_agent(self):
        announce('test_add_agent')
        self.env.add_agent(hiv.Person(name="new added person", infected=False,
                                      infection_length=0, initiative=0,
                                      coupling_tendency=5,
                                      test_frequency=0,
                                      commitment=50,
                                      condom_use=0))
        new_agent = self.env.agent_inspect("new added person")
        self.assertIsNotNone(new_agent)

    def test_props_write(self):
        announce('test_props_write')
        report = True
        self.env.pwrite(self.env.model_nm + '.props')
        with open(self.env.model_nm + '.props', 'r') as f:
            props_written = json.load(f)
        if len(props_written) != len(self.env.props.props):
            report = False
        if report:
            for key in props_written:
                if key not in self.env.props.props:
                    report = False
                    break
                elif (props_written[key]["val"] !=
                      self.env.props.props[key].val):
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
        random_steps = random.randint(3, 30)
        self.env.n_steps(random_steps)
        period_after_run = self.env.period
        if (period_before_run + random_steps) != period_after_run:
            report = False
        self.assertEqual(report, True)

    def test_population_report(self):
        announce('test_population_report')
        self.env.n_steps(random.randint(10, 20))
        report = True
        self.env.pop_report(self.env.model_nm + ".csv")
        f = open(self.env.model_nm + ".csv", "r")
        head = f.readline()
        head = head.strip("\n")
        head_list = head.split(",")
        dic_for_reference = self.env.agents.get_pop_hist()
        for i in head_list:
            if i not in dic_for_reference:
                report = False
                break
        if report:
            dic_for_check = {}
            for i in head_list:
                dic_for_check[i] = []
            for line in f:
                line = line.strip("\n")
                line_list = line.split(",")
                if len(line_list) == len(head_list):
                    for i in range(len(line_list)):
                        dic_for_check[head_list[i]].append(int(line_list[i]))
                else:
                    report = False
                    break

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
        f.readline()

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

        path = (base_dir + "json/" + self.env.model_nm +
                str(rand_sess_id) + ".json")
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

        f.close()
        os.remove(path)

        self.assertEqual(report, True)

    def test_restore_session(self):
        announce('test_restore_session')
        report = True
        rand_sess_id = random.randint(1, 10)
        try:
            base_dir = self.env.props["base_dir"]
        except:
            base_dir = ""
        self.env.save_session(rand_sess_id)
        self.env.n_steps(random.randint(1, 10))
        self.env.restore_session(rand_sess_id)

        path = (base_dir + "json/" + self.env.model_nm +
                str(rand_sess_id) + ".json")
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

        os.remove(path)
        f.close()

        self.assertEqual(report, True)


if __name__ == '__main__':
    announce("main")
    main()
