"""
prop_args.py
Set, read, and write program-wide properties in one location. Includes logging.
"""
import logging
import sys
import platform
import networkx as nx
import json
import os

from IndrasNet.models import Model

SWITCH = '-'
PERIODS = 'periods'
DATAFILE = 'datafile'

OS = "OS"
# user types
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"
WEB = "Web browser"

global user_type
user_type = TERMINAL

type_dict = {'INT': int, 'DBL': float, 'BOOL': bool, 'STR': str}


def get_prop_from_env(prop_nm):
    global user_type
    try:
        user_type = os.environ['user_type']
        print(user_type)
    except KeyError:
        print("Environment variable user type not found")
        user_type = TERMINAL
    return user_type

class Prop():
    """
    Placeholder for prop attributes.

    Attributes include:
        val - the value to be used in the model run
        question - a question prompt for the user's input for the prop value
        atype - the user's answer type (INT, DBL, BOOL, STR, etc.)
        default_val - the property's default value
        lowval - the lowest value val can take on
        hival - the highest value val can take on
    """

    def __init__(self):
        pass


class PropArgs():
    """
    This class holds named properties for program-wide values.
    It enables getting properties from a file, a database,
    or from the user, either via the command line or a prompt.
    """

    @staticmethod
    def create_props(model_nm, props=None):
        """
        Create a property object with values in 'props'.
        """
        global user_type

        if props is None:
            props = {}
            user_type = get_prop_from_env("user_type")
            props["user_type"] = user_type
        return PropArgs(model_nm, props=props)

    def read_props(model_nm, file_nm):
        """
        Create a new PropArgs object from a json file
        """
        props = json.load(open(file_nm))
        return PropArgs.create_props(model_nm, props=props)

    def __init__(self, model_nm, logfile=None, prop_dict=None,
                 loglevel=logging.INFO):
        """
        Loads and sets properties in the following order:
        1. The Database
        2. The User's Environment (operating system, dev/prod settings, etc.)
        3. Property File
        4. Command Line
        5. Questions Prompts During Run-Time
        """
        self.logfile = logfile
        self.model_nm = model_nm
        self.graph = nx.Graph()
        self.model_nm = model_nm
        self.props = {}

        # 1. The Database
        self.set_props_from_db()

        # 2. The Environment
        self.overwrite_props_from_env()

        # 3. Property File
        self.overwrite_props_from_dict(prop_dict)

        # 4. process command line args and set them as properties:
        self.overwrite_props_from_command_line()

        # 5. Ask the user questions.
        self.overwrite_props_from_user()

        self.logger = Logger(self, logfile=logfile)
        self.graph.add_edge(self, self.logger)

    def set_props_from_db(self):
        params = Model.objects.get(name=self.model_nm).params.all()
        for param in params:
            self[param.prop_name] = param.default_val
            self.props[param.prop_name].question = param.question
            self.props[param.prop_name].atype = param.atype
            self.props[param.prop_name].default_val = param.default_val
            self.props[param.prop_name].lowval = param.lowval
            self.props[param.prop_name].hival = param.hival

    def overwrite_props_from_env(self):
        self[OS] = platform.system()

    def overwrite_props_from_dict(self, prop_dict):
        """
        General Form of Dict:

            {
                prop_name: value,
                prop_name: value
            }

        Sample Dict:

            {
                "num_agents": 100,
                "agent_speed": 3
            }

        """
        for prop_nm in prop_dict:
            self[prop_nm] = prop_dict[prop_nm]

    def overwrite_props_from_command_line(self):
        prop_nm = None
        for arg in sys.argv:
            # the first arg (-prop) names the property
            if arg.startswith(SWITCH):
                prop_nm = arg.lstrip(SWITCH)
            # the second arg is the property value
            elif prop_nm is not None:
                self[prop_nm] = arg
                prop_nm = None

    def overwrite_props_from_user(self):
        for prop_nm in self:
            if hasattr(self.props[prop_nm], 'question'):
                self[prop_nm] = self._keep_asking_until_correct(prop_nm)
                
    def _keep_asking_until_correct(self, prop_nm):
        while True:
            answer = input(self._get_question(prop_nm))
            if not answer:
                return None
            typed_answer = self._type_answer(prop_nm, answer)
            if not self._answer_valid(prop_nm, typed_answer):
                print("Input must be between {lowval} and {hival} inclusive."\
                      .format(lowval=self.props[prop_nm].lowval,
                              hival=self.props[prop_nm].hival))
                continue
            return typed_answer

    def _get_question(self, prop_nm):
            return "{question} {lowval}-{hival} [{default}] "\
                   .format(question=self.props[prop_nm].question, 
                           lowval=self.props[prop_nm].lowval,
                           hival=self.props[prop_nm].hival,
                           default=self[prop_nm])

    def _type_answer(self, prop_nm, answer):
        type_cast = type_dict[self.props[prop_nm].atype]
        return type_cast(answer)

    def _answer_valid(self, prop_nm, typed_answer):
        if hasattr(self.props[prop_nm], "lowval") and self.props[prop_nm].lowval > typed_answer:
            return False
        if hasattr(self.props[prop_nm], "hival") and self.props[prop_nm].hival < typed_answer:
            return False
        return True

    def add_props(self, props):
        self.props.update(props)

    def display(self):
        """
        How to represent the properties on screen.
        """
        ret = "Properties for " + self.model_nm + "\n"
        for prop_nm in self:
            ret += "\t" + prop_nm + ": " + str(self[prop_nm]) + "\n"

        return ret

    def __iter__(self):
        return iter(self.props)

    def __str__(self):
        return self.display()

    def __len__(self):
        return len(self.props)

    def __contains__(self, key):
        return key in self.props

    def __setitem__(self, key, value):
        """
        Set a property value.
        """
        if key not in self:
            self.props[key] = Prop()
        self.props[key].val = value

    def __getitem__(self, key):
        return self.props[key].val

    def get(self, nm, default=None):
        """
        Get a property value, with a default
        that gets stored if the property is not there
        at the time of the call.
        """
        if nm not in self:
            self.props[nm].val = default
        return self.props[nm].val

    def __delitem__(self, key):
        del self.props[key]

    def items(self):
        return self.props.items()

    def get_logfile(self):
        """
        Special get function for logfile name
        """
        return self.props["log_fname"]

    def write(self, file_nm):
        """
        Write properties to json file.
        Useful for storing interesting parameter sets.
        """
        json.dump(self.props, open(file_nm, 'w'), indent=4)


class Logger():
    """
    A class to track how we are logging.
    """

    DEF_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
    DEF_LEVEL = logging.INFO
    DEF_FILEMODE = 'w'
    DEF_FILENAME = 'log.txt'

    def __init__(self, props, logfile=None,
                 loglevel=logging.INFO):
        if logfile is None:
            logfile = Logger.DEF_FILENAME
        fmt = props.get("log_format", Logger.DEF_FORMAT)
        lvl = props.get("log_level", Logger.DEF_LEVEL)
        fmd = props.get("log_fmode", Logger.DEF_FILEMODE)
        fnm = props.get("log_fname", logfile)
        logging.basicConfig(format=fmt,
                            level=lvl,
                            filemode=fmd,
                            filename=fnm)
        logging.info("Logging initialized.")
