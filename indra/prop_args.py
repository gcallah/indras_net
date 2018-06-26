"""
prop_args.py
Set, read, and write program-wide properties in one location. Includes logging.
"""
import logging
import sys
import platform
import networkx as nx
import json

from IndrasNet.models import Model

SWITCH = '-'
PERIODS = 'periods'
DATAFILE = 'datafile'

type_dict = {'INT': int, 'DBL': float, 'BOOL': bool, 'STR': str}


def in_range(low, val, high):
    if all([low, high]):
        return low <= val <= high
    elif low:
        return low <= val
    elif high:
        return val <= high
    else:
        return True


class PropArgs():
    """
    This class holds sets of named properties for program-wide values.
    It enables getting properties from a file, in-program,
    or from the user, either via the command line or a prompt.
    """
    prop_sets = {}

    @staticmethod
    def get_props(model_nm):
        """
        Get properties for model 'model_nm'.
        """
        if model_nm in PropArgs.prop_sets:
            return PropArgs.prop_sets[model_nm]

    @staticmethod
    def create_props(model_nm, props={}):
        """
        Create a property object with values in 'props'.
        """
        return PropArgs(model_nm, props=props)

    @staticmethod
    def read_props(model_nm, file_nm):
        """
        Create a new PropArgs object from a json file
        """
        props = json.load(open(file_nm))
        return PropArgs.create_props(model_nm, props=props)

    def __init__(self, model_nm, logfile=None, props=None,
                 loglevel=logging.INFO):
        super().__init__("Properties")
        self.model_nm = model_nm
        # store this instance as the value in the dict for 'model_nm'
        PropArgs.prop_sets[model_nm] = self
        self.graph = nx.Graph()
        if props is None:
            self.set_props_from_db()
        else:
            self.props = props
            logfile = self.get("log_fname")
        self.logger = Logger(self, logfile=logfile)
        self.graph.add_edge(self, self.logger)
        self.set("OS", platform.system())
        self.set("model", model_nm)
        # process command line args and set them as properties:
        prop_nm = None
        for arg in sys.argv:
            # the first arg (-prop) names the property
            if arg.startswith(SWITCH):
                prop_nm = arg.lstrip(SWITCH)
            # the second arg is the property value
            elif prop_nm is not None:
                self.set(prop_nm, arg)
                prop_nm = None

    def set_props_from_db(self):
        """
        Asks user to set parameters associated with the model.
        If an input isn't given, we use a default.

        :return:
        """
        self.props = {}

        db_model_name = self.model_nm
        basic_model = Model.objects.get(name=db_model_name)

        params_to_set = basic_model.params.all()
        for param in params_to_set:
            self.check_val(nm=param.prop_name,
                     msg=param.question,
                     val_type=type_dict[param.atype],
                     default=param.default_val,
                     limits=(param.lowval, param.hival))

    def display(self):
        """
        How to represent the properties on screen.
        """
        ret = "Properties for " + self.model_nm + "\n"
        for prop in self.props:
            ret += "\t" + prop + ": " + str(self.props[prop]) + "\n"

        return ret

    def set(self, nm, val):
        """
        Set a property value.
        """
        self.props[nm] = val

    def get(self, nm, default=None):
        """
        Get a property value, with a default
        that gets stored if the property is not there
        at the time of the call.
        """
        if nm not in self.props:
            self.props[nm] = default
        return self.props[nm]

    def check_val(self, nm, msg, val_type, default=None, limits=None):
        """
        """
        rng_msg = ""
        if limits is not None:
            (low, high) = limits
        if default is not None:
            msg += " (" + str(default) + ")"
        msg += rng_msg + " "
        good_val = False
        if nm not in self.props:
            val = None
        else:  # was set from command line, but we still need to type it
            val = self.get(nm)
        typed_val = val_type(val)
        if limits is not None:
            good_val = in_range(low, typed_val, high)
        else:
            good_val = True
        if not good_val:
            pass  // raise exception here: can use msg
        self.set(nm, typed_val)

    def get_logfile(self):
        """
        Special get function for logfile name
        """
        return self.props.get("log_fname")

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
