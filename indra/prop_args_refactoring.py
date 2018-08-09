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
BASE_DIR = 'base_dir'
DATAFILE = 'datafile'

OS = "OS"

UTYPE = "user_type"
# user types
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"
WEB = "Web browser"

VALUE = "val"
QUESTION = "question"
DEFAULT_VAL = "default_val"
ATYPE = "atype"
HIVAL = "hival"
LOWVAL = "lowval"

global user_type
user_type = TERMINAL

INT = 'INT'
FLT = 'DBL'
BOOL = 'BOOL'
STR = 'STR'
TYPE_DICT = {INT: int, FLT: float, BOOL: bool, STR: str}


def get_prop_from_env():
    global user_type
    try:
        user_type = os.environ[UTYPE]
    except KeyError:
# this can't be done before logging is set up!
#        logging.info("Environment variable user type not found")
        user_type = TERMINAL
    return user_type


def read_props(model_nm, file_nm):
    """
    Create a new PropArgs object from a json file
    """
    props = json.load(open(file_nm))
    return PropArgs.create_props(model_nm, props=props)


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

    def __init__(self, val=None, question=None, atype=None, default_val=None,
                        lowval=None, hival=None):
        self.val = val
        self.question = question
        self.atype = atype
        self.default_val = default_val
        self.lowval = lowval
        self.hival = hival


class PropArgs():
    """
    This class holds named properties for program-wide values.
    It enables getting properties from a file, a database,
    or from the user, either via the command line or a prompt.
    """

    @staticmethod
    def create_props(model_nm, prop_dict=None):
        """
        Create a property object with values in 'props'.
        """
        if prop_dict is None:
            prop_dict = {}
        return PropArgs(model_nm, prop_dict=prop_dict)


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

        if self[UTYPE].val in (TERMINAL, IPYTHON, IPYTHON_NB):

            # 4. process command line args and set them as properties:
            self.overwrite_props_from_command_line()

            # 5. Ask the user questions.
            self.overwrite_props_from_user()

        elif self[UTYPE].val == WEB:
            self[PERIODS] = Prop(val=1)
            self[BASE_DIR] = Prop(val=os.environ[BASE_DIR])

        self.logger = Logger(self, model_name=model_nm, logfile=logfile)
        self.graph.add_edge(self, self.logger)

    def set_props_from_db(self):
        params = Model.objects.get(name=self.model_nm).params.all()
        for param in params:
            atype = param.atype
            typed_default_val = self._type_val_if_possible(param.default_val, param.atype)
            self[param.prop_name] = Prop(val=typed_default_val,
                                               question=param.question,
                                               atype=atype,
                                               default_val=typed_default_val,
                                               lowval=param.lowval,
                                               hival=param.hival)

    def overwrite_props_from_env(self):
        global user_type
        user_type = get_prop_from_env()
        self[UTYPE] = Prop(val=user_type)
        self[OS] = Prop(val=platform.system())

    def overwrite_props_from_dict(self, prop_dict):
        """
        General Dict:

            {
                prop_name:
                    {
                        val: <something>,
                        question: <something>,
                        atype: <something>,
                    }
                prop_name:
                    {
                        val: <something>,
                        hival: <something>,
                        lowval: <something>,
                    }
            }

        Simple Dict:

            {
                prop_name: val,
                prop_name: val
            }

        """
        for prop_nm in prop_dict:
            if type(prop_dict[prop_nm]) is dict:
                atype = prop_dict[prop_nm].get(ATYPE, None)
                val = self._type_val_if_possible(prop_dict[prop_nm].get(VALUE, None), atype)
                question = prop_dict[prop_nm].get(QUESTION, None)
                hival = prop_dict[prop_nm].get(HIVAL, None)
                lowval = prop_dict[prop_nm].get(LOWVAL, None)
                self[prop_nm] = Prop(val=val, question=question, atype=atype,
                                           hival=hival, lowval=lowval)
            else:
                val = prop_dict[prop_nm]

#            if not self._answer_within_bounds(prop_nm, val):
#                raise ValueError("{val} for {prop_nm} is not valid."
#                                 "lower_bound: {lowval} upper_bound: {hival}"
#                                 .format(val=val, prop_nm=prop_nm, lowval=lowval, hival=hival))
 
    def overwrite_props_from_command_line(self):
        prop_nm = None
        for arg in sys.argv:
            # the first arg (-prop) names the property
            if arg.startswith(SWITCH):
                prop_nm = arg.lstrip(SWITCH)
            # the second arg is the property value
            if prop_nm is not None:
                self[prop_nm].val = arg
                prop_nm = None

    def overwrite_props_from_user(self):
        for prop_nm in self:
            if hasattr(self[prop_nm], QUESTION) and self[prop_nm].question:
                self[prop_nm].val = self._keep_asking_until_correct(prop_nm)
    
    @staticmethod
    def _type_val_if_possible(val, atype):
        if atype in TYPE_DICT:
            type_cast = TYPE_DICT[atype]
            return type_cast(val)
        else:
            return val

    def _keep_asking_until_correct(self, prop_nm):
        atype = None
        if hasattr(self[prop_nm], ATYPE):
            atype = self[prop_nm].atype

        while True:
            answer = input(self.get_question(prop_nm))
            if not answer:
                return self[prop_nm].val

            try:
                typed_answer = self._type_val_if_possible(answer, atype)
            except ValueError:
                print("Input of invalid type. Should be {atype}"
                      .format(atype=atype))
                continue

            if not self._answer_within_bounds(prop_nm, typed_answer):
                print("Input must be between {lowval} and {hival} inclusive."
                      .format(lowval=self[prop_nm].lowval,
                              hival=self[prop_nm].hival))
                continue

            return typed_answer

    def _answer_within_bounds(self, prop_nm, typed_answer):
        if self[prop_nm].atype is None or self[prop_nm].atype in (STR, BOOL):
            return True

        if self[prop_nm].lowval is not None and self[prop_nm].lowval > typed_answer:
            return False

        if self[prop_nm].hival is not None and self[prop_nm].hival < typed_answer:
            return False

        return True

    def display(self):
        """
        How to represent the properties on screen.
        """
        ret = "Properties for " + self.model_nm + "\n"
        for prop_nm in self:
            ret += "\t" + prop_nm + ": " + str(self[prop_nm].val) + "\n"

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
        self.props[key] = value

    def __getitem__(self, key):
        return self.props[key]

    def __delitem__(self, key):
        del self.props[key]

    def items(self):
        return self.props.items()

    def get_logfile(self):
        """
        Special get function for logfile name
        """
        return self.props["log_fname"].val

    def write(self, file_nm):
        """
        Write properties to json file.
        Useful for storing interesting parameter sets.
        """
        json.dump(self.props, open(file_nm, 'w'), indent=4)

    def to_json(self):
        return self.props

    def get_val(self, key, default=None):
        if key in self.props and self.props[key].val:
            return self.props[key].val
        return default

    def set_val(self, key, value):
        if key in self:
            print("{} in self".format(key))
            self.props[key].val = value
        else:
            self.props[key] = Prop(val=value)

    def get_question(self, prop_nm):
            return "{question} [{lowval}-{hival}] ({default}) "\
                   .format(question=self[prop_nm].question, 
                           lowval=self[prop_nm].lowval,
                           hival=self[prop_nm].hival,
                           default=self[prop_nm].val)


class Logger():
    """
    A class to track how we are logging.
    """

    DEF_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
    DEF_LEVEL = logging.INFO
    DEF_FILEMODE = 'w'
    # DEF_FILENAME = 'log.txt'

    def __init__(self, props, model_name, logfile=None,
                 loglevel=logging.INFO):
        if logfile is None:
            logfile = model_name + ".log"
        fmt = props.get_val("log_format", Logger.DEF_FORMAT)
        lvl = props.get_val("log_level", Logger.DEF_LEVEL)
        fmd = props.get_val("log_fmode", Logger.DEF_FILEMODE)
        props.set_val("log_fname", logfile)
# we put the following back in once the model names are fixed
#  fnm = props.get("log_fname", logfile)
        logging.basicConfig(format=fmt,
                            level=lvl,
                            filemode=fmd,
                            filename=logfile)
        logging.info("Logging initialized.")

