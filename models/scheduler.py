"""
    This is the fashion model re-written in indra.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

import random
import json
import copy

MODEL_NAME = "scheduler"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 0
DEF_NUM_RED = 0

red_group = None
blue_group = None
env = None

'''
classes CSP and minConflicts below define & 
solve a constraint satisfaction problem
'''

class CSP(object):
    def __init__(self):
        self.nodes = []
        # describes the domain of values assignable to the node
        self.nodeDomains = {}
        # constraints depending only on
        # asingular node 0,1 depending on node value
        self.unary_constraints = {}
        # binary constraints depending on node pair, 0,1 or 2 
        # depending on node values
        self.binary_constraints = {}

    def add_node(self, node_name, domain):
        # check that node doesn't already exist
        if node_name in self.nodes:
            return False
        self.nodes.append(node_name) 
        self.nodeDomains[node_name] = domain

    def add_unary_constraint(self, node, constraintFunc):
        # make sure node has previously been added
        if node not in self.nodes:
            raise KeyError
            return
        domain  = self.nodeDomains[node]
        factor = {val : constraintFunc(val) for val in domain}
        # case where no constraints existed  
        if node not in self.unary_constraints.keys():
            self.unary_constraints[node] = factor
            return
        # case where constraints did exist
        self.unary_constraints[node] = ({val : 
            self.unary_constraints[node][val] * 
            factor[val] for val in domain})

    def add_binary_constraint(self, node1, node2, constaintFunc):
        # make sure both nodes have been added
        if node1 not in self.nodes or node2 not in self.nodes:
            raise KeyError
            return False
        domain1 = self.nodeDomains[node1]
        domain2 = self.nodeDomains[node2]
        tableFactor1 = ({val1 : {val2 : constaintFunc(val1,val2) 
            for val2 in domain2} for val1 in domain1})
        tableFactor2 = ({val2 : {val1 : constaintFunc(val1,val2) 
            for val1 in domain1} for val2 in domain2})
        self.update_binary_constraint_table(node1, node2, tableFactor1)
        self.update_binary_constraint_table(node2, node1, tableFactor2) 

    def update_binary_constraint_table(self, nodeA, nodeB, tableFactor):
        if nodeA not in self.binary_constraints.keys():
            self.binary_constraints[nodeA] = {}
            self.binary_constraints[nodeA][nodeB] = tableFactor
            return
        if nodeB not in self.binary_constraints[nodeA].keys():
               self.binary_constraints[nodeA][nodeB] = tableFactor
               return
        currentTable = self.binary_constraints[nodeA][nodeB]
        for i in tableFactor:
            for j in tableFactor[i]:
                assert i in currentTable and j in currentTable[i]
                currentTable[i][j] *= tableFactor[i][j]

class minConflicts(object):
    def __init__(self, csp):
        self.csp = csp

    #assigns each variable a random domain value
    def initial_var_assignment(self):
        assignments = {}
        nodes = self.csp.nodes
        domains = self.csp.nodeDomains
        for n in nodes:
            val_rand = random.choice(domains[n])
            assignments[n] = val_rand
        return assignments

    #returns list of conflicted node assignments i.e. which evaulate to zero
    def conflicted(self, assignments):
        conflicted = []
        csp = self.csp
        for n in assignments:
            if n in conflicted: continue 
            val = assignments[n]
            #make sure no KeyError on unary and binary constraints
            try:
                if csp.unary_constraints[n][val]==0:
                    conflicted.append(n)
            except KeyError:
                pass
            try:
                neighbors = set(csp.binary_constraints[n].keys())
            except KeyError:
                continue
            for m in neighbors:
                val_neigh = assignments[m]
                if csp.binary_constraints[n][m][val][val_neigh]==0:
                    conflicted+=[n,m]
        return set(conflicted)

    #returns list of node neighbors that conflict with it
    def conflicted_neighbors(self, assignments, n):
        conflicted = []
        val = assignments[n]
        csp = self.csp  
        soft_weight = 1
        """
        proportional to number of 
        soft-constraints satisfied
        checks for missing keys on unary constraints
        """
        try:
            if csp.unary_constraints[n][val] == 0: 
                conflicted.append(n)
        except:
            pass
        #checks on binary constraints
        try:
            neighbors = set(csp.binary_constraints[n].keys())
        except:
            return (set(conflicted), soft_weight)
        for m in neighbors:
            val_neigh = assignments[m]
            w = csp.binary_constraints[n][m][val][val_neigh]
            if w==0:
                conflicted += [n,m]
            else:
                soft_weight *= w
        return (set(conflicted), soft_weight)

    def solve(self, max_iters = 100):
        assignments = self.initial_var_assignment()
        csp = self.csp
        for _ in range(max_iters):
            conflicted = self.conflicted(assignments)
            if len(conflicted)==0: return assignments
            #choose a random conflicted variable
            node = random.choice(list(conflicted))
            val = assignments[node]
            c0, w0 = self.conflicted_neighbors(assignments, node)
            min_conflicted = len(c0)
            D = csp.nodeDomains[node]
            random.shuffle(D)
            for u in D:
                if u == val: continue
                assignments_cpy = copy.deepcopy(assignments)
                assignments_cpy[node] = u
                c,w = self.conflicted_neighbors(assignments_cpy, node)
                if len(c) < min_conflicted:
                    assignments = assignments_cpy 
                    min_conflicted = len(c)
                    w0 = w
                elif len(c) == min_conflicted:
                    #chooose equally conflicted node by random weighted on soft-constraint
                    r = random.random()
                    if r < w / (w + w0):
                        w0 = w
                        assignments = assignments_cpy

        return False    #process failed


'''
Function for defining and solving the 
teacher-class-course scheduler problem
'''                     
def CourseRoomProfAssigner():       
    def add_nodes():
        #nodes have format (c,p)
        for c in courses:
            #enforce room consistency
            if rooms_chosen.get(c) == None:
                rooms_for_course = rooms
            else:
                rooms_for_course = rooms_chosen[c]            
            p = full_prof_assignment[c]
            if p == None: continue
            domain = [(r, h) for r in rooms_for_course for h in hours_for_prof(p)]
            node_name = (c, p)
            csp.add_node(node_name,domain)

    def profs_for_courses(courses):
        profs_chosen = {c:None for c in courses}
        for c in courses:
            hits = []
            for p in professors:
                their_courses = prof_info[p]['courses']
                if c in their_courses: hits.append(p)
            profs_chosen[c] = random.choice(hits)
        return profs_chosen

    #Soft constraint. Assigns courses randomly weighted to preferred days
    def courses_per_day():
        course_days_choice = dict([(c, days_for_course(c)) for c in courses])
        weekdays = ['mon', 'tues', 'wed', 'thur', 'fri']
        courses_on_days = dict([(d, []) for d in weekdays])
        for c, days in course_days_choice.items():
            for d in days:
                courses_on_days[d].append(c)
        return courses_on_days

    def days_for_course(c):
        n = min(course_days_weekly[c], 5)
        days_chosen = []
        #Pairs Mon-Wed & Thurs-Fri preferred if course runs 2-4 days
        if 2 <= n and n <= 4:
            workdays = ['mon', 'wed', 'thur', 'fri'] * 2 + ['tues']
        elif n == 1:
            workdays = ['mon', 'tues', 'wed', 'thur', 'fri']
        else:
            return ['mon', 'tues', 'wed', 'thur', 'fri']
        for i in range(n):
            d = random.choice(workdays)
            if i==0:
                if d in ['mon', 'wed']:
                    pref = ['mon', 'wed']
                    pref.remove(d)
                    days = ['mon', 'tues', 'wed', 'thur', 'fri']
                    days.remove(d)
                    workdays = days + pref
                elif d in ['thur', 'fri']:
                    pref = ['thur', 'fri']
                    pref.remove(d)
                    days = ['mon', 'tues', 'wed', 'thur', 'fri']
                    days.remove(d)
                    workdays = days + pref
                else:
                    workdays = ['mon', 'wed', 'thur', 'fri']
            else:
                workdays = list(set(workdays))
                workdays.remove(d)
            days_chosen.append(d)
        return days_chosen

    def hours_for_prof(p):
        #in format (hours,minutes) in 30min intervals
        start_time = prof_info[p]['start_time']
        end_time = prof_info[p]['end_time']
        return {(i ,j * 30) for i in range(start_time, end_time) for j in range(2)}

    def add_unary():                
        for n in csp.nodes:   
            c, p = n
            def room_has_capacity(val, course=c, prof=p):
                room,hour_and_min = val
                no_students = course_no_students[course]
                return bool(room_capacities[room] >= no_students)
            csp.add_unary_constraint((c, p), room_has_capacity)
    def add_binary():
        nodes = csp.nodes
        for i, n in enumerate(nodes):
            course_n, prof_n = n
            for m in nodes[i:]:
                course_m, prof_m = m
                if prof_n == prof_m:
                    if course_n == course_m: continue
                    '''first binary constraint'''
                    def no_class_overlap(val1, val2, course1 = course_n, course2 = course_m):
                        """makes the math easy: calculate course 
                        times in 10min intervals e.g. 120min is 12 intervals"""
                        hours1, mins1 = val1[1]
                        hours2, mins2 = val2[1]
                        course_start1 = hours1 * 6 + mins1 // 10
                        course_end1 = course_start1 + course_mins[course1] // 10
                        course_start2 = hours2 * 6 + mins2 // 10
                        course_end2 = course_start2 + course_mins[course2]//10
                        #conditions to check if one class starts during other
                        if course_start1 <= course_start2 and course_start2 < course_end1:
                            return bool(False)
                        if course_start2 <= course_start1 and course_start1 < course_end2:
                            return bool(False)
                        #soft constraint: non-sequental classes get higher weight
                        if course_start1 == course_end2 or course_start2 == course_end1:
                            return 2
                        return bool(True)
                    csp.add_binary_constraint(n, m, no_class_overlap)
                '''second binary constraint'''
                def no_time_clash(val1, val2, course1 = course_n):
                    room1, time1 = val1
                    room2, time2 = val2
                    if room1 != room2: return bool(True)
                    hours1, mins1 = time1
                    hours2, mins2 = time2
                    start_time1 = hours1 * 6 + mins1 // 10
                    end_time1 = start_time1 + course_mins[course1] // 10
                    start_time2 = hours2 * 6 + mins2 // 10
                    if start_time1 <= start_time2 and start_time2 < end_time1:
                        return bool(False)
                    return bool(True)             
                csp.add_binary_constraint(n, m, no_time_clash)

    #JSON loading for room, professor and course data
    with open('sample_json_data.txt', 'r') as outfile:
        data = json.load(outfile)
    professors = data['professors']
    prof_info = data['prof_info']
    rooms = data['rooms']
    room_capacities = data['room_capacities']
    courses = data['courses']
    course_no_students = data['course_no_students']
    global course_mins#need this for time ranges outside this function 
    course_mins = data['course_mins']
    course_days_weekly = data['course_days_weekly']

    full_prof_assignment = profs_for_courses(courses)       #enforce professor-course consistency among different days
    rooms_chosen = {}       #rooms are consistent
    weekdays = ['mon', 'tues', 'wed', 'thur', 'fri']
    solution = {d: None for d in weekdays}
    retries = 0     #will retry max 3 times to get a solution
    while retries < 3:
        daily_courses = courses_per_day()
        max_iters = 100 * (retries + 1)     #upon retry increase maximum iterations
        for d in weekdays:
            csp = CSP()
            courses = daily_courses[d]
            add_nodes()
            add_unary()
            add_binary()
            minconf = minConflicts(csp)
            solved = minconf.solve(max_iters)
            if solved is None:
                retries += 1
                if retries < 3:
                    break
            solution[d] = solved
        break
    #output solution in agent friendly format
    form = {'professor': None, 'room': None}
    agent_solution = {}
    for day in solution:
        solved = solution[day]
        for k, a in solved.items():
            course, prof = k
            room, start_time = a
            #get end_time
            h, m = start_time
            end = h * 6 + m // 10 + course_mins[k[0]] // 10
            end_time = (end // 6,(end - (end // 6) * 6) * 10)
            if agent_solution.get(course) is None:
                agent_solution[course] = copy.deepcopy(form)
                agent_solution[course]['professor'] = prof
                agent_solution[course]['room'] = room
            agent_solution[course]['start_time' + '_' + str(day)] = start_time
            agent_solution[course]['end_time' + '_' + str(day)] = end_time
    return agent_solution

def sched_agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # return False means to move
    return False

def create_agent(color, i):
    """
    Create an agent.
    """
    return Agent(color + str(i), action=sched_agent_action)

def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = props
    ds_file = get_prop_path(MODEL_NAME)
    if pa is None:
        pa = PropArgs.create_props(MODEL_NAME, ds_file=ds_file)
    blue_group = Composite("Blues", {"color": BLUE},
                           member_creator=create_agent,
                           num_members=pa.get('num_blue', DEF_NUM_BLUE))

    red_group = Composite("Reds", {"color": RED},
                          member_creator=create_agent,
                          num_members=pa.get('num_red', DEF_NUM_RED))

    # add our agents to the groups
    course_assignments = CourseRoomProfAssigner()
    for c, a in course_assignments.items():
        course_agent = create_agent('Reds_', c)
        course_agent.attrs = a
        red_group += course_agent
        cprop = copy.deepcopy(a)
        prof = cprop['professor']
        room = cprop['room']
        blues_prof = 'Blues_' + str(prof)
        blues_room = 'Blues_' + str(room)
        if blues_prof not in blue_group.members:
            blue_group += create_agent('Blues_', prof)
        if blues_room not in blue_group.members:
            blue_group += create_agent('Blues_', room)
    print(red_group.members)
    print('```````')
    print(blue_group.members)
    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[blue_group, red_group],
              props=pa)
    return (env, blue_group, red_group)

def main():
    global red_group
    global blue_group
    global env

    (env, blue_group, red_group) = set_up()

    if DEBUG2:
        print(env.__repr__())
    # env()
    return 0

if __name__ == "__main__":
    main()
