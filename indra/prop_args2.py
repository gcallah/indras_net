"""
prop_args2.py
Set, read, and write program-wide properties in one location. Includes logging.
"""
import logging
import sys
import platform
import networkx as nx
import json
import os
from django.core.exceptions import ObjectDoesNotExist

from IndrasNet.models import ABMModel

SWITCH = '-'
PERIODS = 'periods'
BASE_DIR = 'base_dir'
DATAFILE = 'datafile'

OS = "OS"

UTYPE = "user_type"
# user types (DUMMY type is only for automated test)
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"
WEB = "Web browser"
DUMMY = "dummy"

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
type_dict = {INT: int, FLT: float, BOOL: bool, STR: str}


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
    return PropArgs.create_props(model_nm, props)


class Prop():
    """
    Container for prop attributes.

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

    def to_json(self):
        return {"val": self.val,
                "question": self.question,
                "atype": self.atype,
                "default_val": self.default_val,
                "lowval": self.lowval,
                "hival": self.hival}

    def __str__(self):
        return str(self.val)


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
        self.props = {}

        # 1. The Database
        self.set_props_from_db()

        # 2. The Environment
        self.overwrite_props_from_env()

        # 3. Property File
        self.overwrite_props_from_dict(prop_dict)

        if self.props[UTYPE].val in (TERMINAL, IPYTHON, IPYTHON_NB):
            # 4. process command line args and set them as properties:
            self.overwrite_props_from_cl()

            # 5. Ask the user questions.
            self.overwrite_props_from_user()

        elif self.props[UTYPE].val == WEB:
            self.props[PERIODS] = Prop(val=1)
            self.props[BASE_DIR] = Prop(val=os.environ[BASE_DIR])

        self.logger = Logger(self, model_name=model_nm, logfile=logfile)
        self.graph.add_edge(self, self.logger)

    def set_props_from_db(self):
        try:
            params = ABMModel.objects.get(name=self.model_nm).params.all()
            for param in params:
                atype = param.atype
                typed_default_val = self._type_val_if_possible(param.default_val,
                                                               param.atype)
                self.props[param.prop_name] = Prop(val=typed_default_val,
                                                   question=param.question,
                                                   atype=atype,
                                                   default_val=typed_default_val,
                                                   lowval=param.lowval,
                                                   hival=param.hival)
        except ObjectDoesNotExist:
            print("ABMModel not found in db: " + self.model_nm)

    def overwrite_props_from_env(self):
        global user_type
        user_type = get_prop_from_env()
        self.props[UTYPE] = Prop(val=user_type)
        self.props[OS] = Prop(val=platform.system())

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
                val = self._type_val_if_possible(prop_dict[prop_nm].get(VALUE,
                                                                        None),
                                                 atype)
                question = prop_dict[prop_nm].get(QUESTION, None)
                default_val = prop_dict[prop_nm].get(DEFAULT_VAL, None)
                hival = prop_dict[prop_nm].get(HIVAL, None)
                lowval = prop_dict[prop_nm].get(LOWVAL, None)
                self.props[prop_nm] = Prop(val=val, question=question, atype=atype, default_val=default_val,
                                           hival=hival, lowval=lowval)
            else:
                self[prop_nm] = prop_dict[prop_nm]

    def overwrite_props_from_cl(self):
        prop_nm = None
        for arg in sys.argv:
            # the first arg (-prop) names the property
            if arg.startswith(SWITCH):
                prop_nm = arg.lstrip(SWITCH)
            # the second arg is the property value
            if prop_nm is not None:
                self.props[prop_nm].val = arg
                prop_nm = None

    def overwrite_props_from_user(self):
        for prop_nm in self:
            if (hasattr(self.props[prop_nm], QUESTION)
                and self.props[prop_nm].question):
                self.props[prop_nm].val = self._keep_asking_until_correct(prop_nm)
    
    @staticmethod
    def _type_val_if_possible(val, atype):
        if atype in type_dict:
            type_cast = type_dict[atype]
            return type_cast(val)
        else:
            return val

    def _keep_asking_until_correct(self, prop_nm):
        atype = None
        if hasattr(self.props[prop_nm], ATYPE):
            atype = self.props[prop_nm].atype

        while True:
            answer = input(self.get_question(prop_nm))
            if not answer:
                return self.props[prop_nm].val

            try:
                typed_answer = self._type_val_if_possible(answer, atype)
            except ValueError:
                print("Input of invalid type. Should be {atype}"
                      .format(atype=atype))
                continue

            if not self._answer_within_bounds(prop_nm, typed_answer):
                print("Input must be between {lowval} and {hival} inclusive."
                      .format(lowval=self.props[prop_nm].lowval,
                              hival=self.props[prop_nm].hival))
                continue

            return typed_answer

    def _answer_within_bounds(self, prop_nm, typed_answer):
        if (self.props[prop_nm].atype is None 
            or self.props[prop_nm].atype in (STR, BOOL)):
            return True

        if (self.props[prop_nm].lowval is not None 
            and self.props[prop_nm].lowval > typed_answer):
            return False

        if (self.props[prop_nm].hival is not None 
            and self.props[prop_nm].hival < typed_answer):
            return False

        return True

    def display(self):
        """
        How to represent the properties on screen.
        """
        ret = "Properties for " + self.model_nm + "\n"
        for prop_nm in self:
            ret += "\t" + prop_nm + ": " + str(self.props[prop_nm].val) + "\n"

        return ret

    def __iter__(self):
        return iter(self.props)

    def __str__(self):
        return self.display()

    def __len__(self):
        return len(self.props)

    def __contains__(self, key):
        return key in self.props

    def __setitem__(self, key, v):
        """
        Set a property value.
        """
        if key in self:
            self.props[key].val = v
        else:
            self.props[key] = Prop(val=v)

    def __getitem__(self, key):
        return self.props[key].val

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
        dict_for_json = {}
        for prop_name in self.props:
            dict_for_json[prop_name] = self.props[prop_name].to_json()
        f = open(file_nm, 'w')
        json.dump(dict_for_json, f, indent=4)
        f.close()

    def to_json(self):
        return { prop_nm: self.props[prop_nm].to_json() for prop_nm in self.props }

    def get(self, key, default=None):
        if key in self.props and self.props[key].val:
            return self.props[key].val
        return default

    def get_question(self, prop_nm):
            return "{question} [{lowval}-{hival}] ({default}) "\
                   .format(question=self.props[prop_nm].question, 
                           lowval=self.props[prop_nm].lowval,
                           hival=self.props[prop_nm].hival,
                           default=self.props[prop_nm].val)


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
        fmt = props["log_format"] if "log_format" in props else Logger.DEF_FORMAT
        lvl = props["log_level"] if "log_level" in props else Logger.DEF_LEVEL
        fmd = props["log_fmode"] if "log_fmode" in props else Logger.DEF_FILEMODE
        props["log_fname"] = logfile
# we put the following back in once the model names are fixed
#  fnm = props.get("log_fname", logfile)
        logging.basicConfig(format=fmt,
                            level=lvl,
                            filemode=fmd,
                            filename=logfile)
        logging.info("Logging initialized.")

