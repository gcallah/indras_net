import random
import indra.agent_pop as ap
from unittest import TestCase, main
from collections import OrderedDict
import indra.node as node

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
        # we will test rest of the functions with reference of dict_for_reference if they return correct result
        # format: {var:{"agents": [], "pop_data": 0,"pop_hist": [],"my_periods": 0,"disp_color": None}}
        self.dic_for_reference = OrderedDict()
        self.agentpop = ap.AgentPop("test")
        # add 3 varieties
        for i in range(3):
            self.dic_for_reference[str(i)] = {AGENTS: [], POP_DATA: 0,POP_HIST: [],MY_PERIODS: 0,DISP_COLOR: None}
        for i in range(3):
            # add color to each variety
            self.dic_for_reference[str(i)][DISP_COLOR] = "#" + str(i)
            # add agents
            for r in range(random.randint(1,7)):
                self.dic_for_reference[str(i)][AGENTS].append(node.Node("agent"+str(r)))
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var][AGENTS]:
                a.ntype = var
        # for var in self.dic_for_reference:
        #     for a in self.dic_for_reference[var]["agents"]:
        #         print(a.ntype)
    #     finish building dic_for_reference

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
        print(self.agentpop.vars)
        self.assertEqual(report, True)

    def test_append(self):
        print(self.agentpop.vars)
        print(self.dic_for_reference)
        report = True
        for var in self.dic_for_reference:
            for a in self.dic_for_reference[var]["agents"]:
                self.agentpop.append(a)

        for var in self.agentpop.vars:
            if self.agentpop.vars[var]["agents"] != self.dic_for_reference[var]["agents"]:
                print(self.agentpop.vars[var]["agents"])
                print(self.dic_for_reference[var]["agents"])
                report = False
        self.assertEqual(report, True)


if __name__ == '__main__':
    main()
