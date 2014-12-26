import logging
import json


class PropArgs():

    """
    This class holds sets of named properties for program-wide values.
    """

    prop_sets = {}


    @staticmethod
    def get_props(model_nm, props={}):
        if model_nm in PropArgs.prop_sets:
            return PropArgs.prop_sets[model_nm]


    def create_props(model_nm, props={}):
        return(PropArgs(model_nm, props))

    
    @staticmethod
    def read_props(model_nm, file_nm):
        props = json.load(open(file_nm))
        return PropArgs.create_props(model_nm, props)

    
    def __init__(self, model_nm, logfile=None, props={}):
        self.model_nm = model_nm
# store this instance as the value in the dict for 'model_nm'
        PropArgs.prop_sets[model_nm] = self
        self.props = props
        self.logger = Logger(self, logfile=logfile)


    def set(self, nm, val):
        self.props[nm] = val


    def get(self, nm, default=None):
        if nm not in self.props:
            self.props[nm] = default
        return self.props[nm]

    """
    Special get function for logfile name
    """
    def get_logfile(self):
        return self.props.get("log_fname")


    def write(self, file_nm):
        json.dump(self.props, open(file_nm, 'w'))


class Logger():

    DEF_FORMAT   = '%(levelname)s:%(message)s'
    DEF_LEVEL    = logging.INFO
    DEF_FILEMODE = 'w'
    DEF_FILENAME = 'log.txt'

    def __init__(self, props, logfile=None):
        if logfile is None:
            logfile = DEF_FILENAME
        fmt = props.get("log_format", Logger.DEF_FORMAT)
        lvl = props.get("log_level", Logger.DEF_LEVEL)
        fmd = props.get("log_fmode", Logger.DEF_FILEMODE)
        fnm = props.get("log_fname", logfile)

        logging.basicConfig(format=fmt, level=lvl, filemode=fmd, filename=fnm)


