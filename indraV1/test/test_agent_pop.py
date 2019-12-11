import random
import indra.agent_pop as ap
from unittest import TestCase, main
from collections import OrderedDict
import indra.node as node
import indra.entity as ent
import json
import os

AGENTS = "agents"
POP_DATA = "pop_data"
POP_HIST = "pop_hist"
MY_PERIODS = "my_periods"
DISP_COLOR = "disp_color"


class AgentPopTestCase(TestCase):
    def __init__(self, methodName):
        super().__init__(methodName=methodName)
        # A dictionary for different types of dummy agents in order to test agent pop class
        # First we will fill this dict with various dummy agents,
        # then we will fill the Agent Pop class, using dict_for_reference as source
        # The OrderedDict in Agent Pop should be the same as dic_for_reference. That will test if append works
        # If append works and we have the OrderedDict in Agent Pop,
        # we will test rest of the functions if they return correct result, with reference of dict_for_reference
        # format: {var:{"agents": [], "pop_data": 0,"pop_hist": [],"my_periods": 0,"disp_color": None}}
        self.dic_for_reference = OrderedDict()
        self.agentpop = ap.AgentPop("test")
        # add 3 varieties
        for i in range(3):
            self.dic_for_reference[str(i)] = {AGENTS: [], POP_DATA: 0,POP_HIST: [],MY_PERIODS: 0,DISP_COLOR: None}
        for i in range(3):
            # add color to each variety
            self.dic_for_reference[str(i)][DISP_COLOR] = "#" + str(i)
            # add agents; agent type is Node
            for r in range(random.randint(1,7)):
                self.dic_for_reference[str(i)][AGENTS].append(node.Node("agent"+str(r)))
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                a.ntype = var
                #assign ntype for each agent; each dic_for_reference's variety should be the same as its agents' ntype!
    #     finish building dic_for_reference,
    #     dic_for_reference should look like: {
    #       '0':{"agents": [1-7 agents of ntype('0')], "pop_data": 0,"pop_hist": [],"my_periods": 0,"disp_color": '#0'}
    #       '1':{"agents": [1-7 agents of ntype('1')], "pop_data": 0,"pop_hist": [],"my_periods": 0,"disp_color": '#1'}
    #       '2':{"agents": [1-7 agents of ntype('2')], "pop_data": 0,"pop_hist": [],"my_periods": 0,"disp_color": '#2'}
    # }
    # Note: each individual test function has its own unique self.dic_for_reference and self.agent_pop. Change of self.dic_for_reference
    # in one function won't affect the use of it in other functions. (Two functions will have different self.dic_for_reference)

    def test_add_variety(self):
        report = True
        self.agentpop.add_variety("1")
        if "1" not in self.agentpop.vars:
            report = False
        if report is True:
            if len(self.agentpop.vars['1'][AGENTS])!= 0:
                report = False
            if self.agentpop.vars['1'][POP_DATA] != 0:
                report = False
            if len(self.agentpop.vars['1'][POP_HIST]) != 0:
                report = False
            if self.agentpop.vars['1'][MY_PERIODS] != 0:
                report = False
            if self.agentpop.vars['1'][DISP_COLOR] is not None:
                report = False
            # make sure when a variety already exist, adding the same variety won't overwrite the existing one
            self.agentpop.vars["1"][DISP_COLOR] = "dummy color"
            self.agentpop.add_variety("1")
            if self.agentpop.vars["1"][DISP_COLOR] is None:
                report = False

            self.agentpop.vars["1"][DISP_COLOR] = None
        self.assertEqual(report, True)

    def test_append(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)

        for var in self.agentpop.vars:
            if self.agentpop.vars[var][AGENTS] != self.dic_for_reference[var][AGENTS]:
                report = False

        self.assertEqual(report, True)

    def test_iter(self):
        report = True
        lst_for_reference = []
        for var in self.dic_for_reference:
            lst_for_reference += self.dic_for_reference[var][AGENTS]
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)

        counter = 0
        for i in self.agentpop:
            if i != lst_for_reference[counter]:
                report = False
                break
            counter += 1

        self.assertEqual(report, True)

    def test_len(self):
        report = True
        counter = 0
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                counter += 1
                self.agentpop.append(a)

        if len(self.agentpop) != counter:
            report = False
        self.assertEqual(report, True)

    def test_all_agents_list(self):
        report = True
        lst_for_reference = []
        for var in self.dic_for_reference:
            lst_for_reference += self.dic_for_reference[var][AGENTS]
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        result_lst = self.agentpop.all_agents_list()

        if result_lst != lst_for_reference:
            report = False
        self.assertEqual(report, True)

    def test_reversed(self):
        report = True
        lst_for_reference = []
        for var in self.dic_for_reference:
            lst_for_reference += self.dic_for_reference[var][AGENTS]
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)

        result_lst = self.agentpop.__reversed__()
        lst_for_reference.reverse()
        counter = 0
        for i in result_lst:
            if i != lst_for_reference[counter]:
                report = False
            counter += 1

        self.assertEqual(report, True)

    def test_element_at(self):
        report = True
        lst_for_reference = []
        for var in self.dic_for_reference:
            lst_for_reference += self.dic_for_reference[var][AGENTS]
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        index = random.randint(0,len(self.agentpop)-1)
        if self.agentpop.element_at(index) != lst_for_reference[index]:
            report = False

        self.assertEqual(report, True)

    def test_get_var_color(self):
        report = True
        self.agentpop.add_variety("1")
        self.agentpop.vars['1'][DISP_COLOR] = "#1"
        result_color = self.agentpop.get_var_color('1')
        if result_color != "#1":
            report = False
        self.assertEqual(report, True)

    def test_set_var_color(self):
        report = True
        self.agentpop.add_variety("1")
        self.agentpop.set_var_color('1', "#1")
        if self.agentpop.vars['1'][DISP_COLOR] != "#1":
            report = False
        self.assertEqual(report, True)

    def test_remove(self):
        report = True
        self.agentpop.add_variety("dummy var")
        dummy_node = node.Node("dummy node")
        dummy_node.ntype = "dummy var"
        self.agentpop.append(dummy_node)
        self.agentpop.remove(dummy_node)
        if dummy_node in self.agentpop.vars['dummy var'][AGENTS]:
            report = False

        self.assertEqual(report, True)

    def test_get_agents_of_var(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        var = str(random.randint(0,2))
        result_lst = self.agentpop.get_agents_of_var(var)
        if self.dic_for_reference[var][AGENTS] != result_lst:
            report = False

        self.assertEqual(report, True)

    def test_get_pop(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        var = str(random.randint(0, 2))
        result = self.agentpop.get_pop(var)
        if result != len(self.dic_for_reference[var][AGENTS]):
            report = False

        self.assertEqual(report, True)

    def test_get_total_pop(self):
        report = True
        correct_pop = 0
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
                correct_pop += 1
        result = self.agentpop.get_total_pop()
        if correct_pop != result:
            report = False

        self.assertEqual(report, True)

    def test_get_my_pop(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        var = str(random.randint(0, 2))
        dummy_node = node.Node("dummy node")
        dummy_node.ntype = var
        self.agentpop.append(dummy_node)
        self.dic_for_reference[var][AGENTS].append(dummy_node)
        result = self.agentpop.get_my_pop(dummy_node)
        correct_pop = len(self.dic_for_reference[var][AGENTS])
        if result != correct_pop:
            report = False

        self.assertEqual(report, True)

    def test_census(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        census_report = self.agentpop.census()
        census_report = census_report.split('\n')
        census_report.pop()
        #print(census_report)
        index = 0
        for var in self.agentpop.vars:
            # also need to check if census functino append the right number to ["pop_hist"]
            if self.agentpop.vars[var][POP_HIST][-1] != len(self.agentpop.vars[var][AGENTS]):
                report = False
                break
            item_to_check = census_report[index]
            item_to_check = item_to_check.split(": ")
            if var != item_to_check[0]:
                report = False
                break
            if len(self.agentpop.vars[var][AGENTS]) != int(item_to_check[1]):
                report = False
                break
            # print(item_to_check)
            index += 1

        self.assertEqual(report, True)

    def test_get_pop_hist(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
                self.agentpop.census()
            self.agentpop.set_var_color(var, self.dic_for_reference[var][DISP_COLOR])

        result_dic = self.agentpop.get_pop_hist()
        if not result_dic:
            report = False
        for var in result_dic:
            if result_dic[var]["data"] != self.agentpop.vars[var][POP_HIST]:
                report = False
                break
            if result_dic[var]["color"] != self.agentpop.vars[var][DISP_COLOR]:
                report = False
                break

        self.assertEqual(report, True)

    def test_get_pop_data(self):
        report = True
        check_list = []
        for var in self.dic_for_reference:
            random_pop_data = random.randint(1,10)
            check_list.append(random_pop_data)
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
            self.agentpop.vars[var][POP_DATA] = random_pop_data
        index = 0
        for var in self.agentpop.vars:
            result = self.agentpop.get_pop_data(var)
            if result != check_list[index]:
                report = False
                break
            index += 1

        self.assertEqual(report, True)

    def test_change_pop_data(self):
        report = True
        check_list = []
        for var in self.dic_for_reference:
            random_pop_data = random.randint(1, 10)
            check_list.append(random_pop_data)
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
            self.agentpop.vars[var][POP_DATA] = random_pop_data
        change = 5
        self.agentpop.change_pop_data('1', change)
        answer = check_list[1] + change
        if self.agentpop.vars['1'][POP_DATA] != answer:
            report = False
        self.assertEqual(report, True)

    def test_change_agent_type(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        agent_for_track = node.Node("agent for track")
        agent_for_track.ntype = "0"
        self.agentpop.append(agent_for_track)
        # print("check1 !!!", agent_for_track.ntype)
        new_type = "dummy type"
        old_type = '0'
        self.agentpop.change_agent_type(agent_for_track, old_type, new_type)
        # print("check2 !!!", agent_for_track.ntype)
        if agent_for_track.ntype != new_type:
            report = False
        if new_type not in self.agentpop.vars:
            report = False
        if agent_for_track not in self.agentpop.vars[new_type][AGENTS]:
            report = False
        if agent_for_track in self.agentpop.vars[old_type][AGENTS]:
            report = False

        self.assertEqual(report, True)

    def test_restore_hist_from(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
            self.agentpop.set_var_color(var, self.dic_for_reference[var][DISP_COLOR])
        dict_to_pass_in = self.agentpop.get_pop_hist()
        dummy_ap = ap.AgentPop("dummy")
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                dummy_ap.append(a)
        dummy_ap.restore_hist_from(dict_to_pass_in)
        dict_to_check = dummy_ap.get_pop_hist()
        if dict_to_pass_in != dict_to_check:
            report = False

        self.assertEqual(report, True)

    def test_jsondump(self):
        report = True
        returned_0 = self.agentpop.jsondump(self.agentpop.graph)
        if returned_0 != "Graph":
            report = False
        dummy_entity = ent.Entity("dummy_ent")
        dummy_to_json = dummy_entity.to_json()
        returned_1 = self.agentpop.jsondump(dummy_entity)
        if returned_1 != dummy_to_json:
            report = False
        vars_to_json = self.agentpop.vars.__dict__
        returned_2 = self.agentpop.jsondump(self.agentpop.vars)
        if returned_2 != vars_to_json:
            report = False

        self.assertEqual(report, True)

    def test_record_results(self):
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                self.agentpop.append(a)
        self.agentpop.record_results("dummy.json")
        json_input = ''
        with open("dummy.json", "r") as f:
            for line in f:
                json_input+=line.strip()
        json_input_dic = json.loads(json_input)
        f.close()
        if json_input_dic['name'] != 'test':
            report = False
        if json_input_dic['graph'] != 'Graph':
            report = False
        if json_input_dic['ntype'] != 'AgentPop':
            report = False
        if len(json_input_dic['vars']) != len(self.agentpop.vars):
            report = False
        for var in json_input_dic['vars']:
            if (var in self.agentpop.vars) and (report == True):
                if json_input_dic['vars'][var]["pop_data"] != self.agentpop.vars[var]["pop_data"]:
                    report = False
                if json_input_dic['vars'][var]["pop_hist"] != self.agentpop.vars[var]["pop_hist"]:
                    report = False
                if json_input_dic['vars'][var]["my_periods"] != self.agentpop.vars[var]["my_periods"]:
                    report = False
                if json_input_dic['vars'][var]["disp_color"] != self.agentpop.vars[var]["disp_color"]:
                    report = False
                # need to figure out how to see if two set of agents are same
                for agent in self.agentpop.vars[var][AGENTS]:
                    report = False
                    for agent2 in json_input_dic['vars'][var]["agents"]:
                        if agent2['name'] == agent.name and agent2['graph']==agent.graph and agent2['ntype']==agent.ntype:
                            report = True
                    if not report:
                        break

            else:
                report = False

        os.remove("dummy.json")
        self.assertEqual(report, True)


if __name__ == '__main__':
    main()
