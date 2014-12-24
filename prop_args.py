import json


class PropArgs():

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

    
    def __init__(self, model_nm, props={}):
        self.model_nm = model_nm
# store this instance as the value in the dict for 'model_nm'
        PropArgs.prop_sets[model_nm] = self
        self.props = props


    def set(self, nm, val):
        self.props[nm] = val


    def get(self, nm, default=None):
        if nm not in self.props:
            self.props[nm] = default
        return self.props[nm]


    def write(self, file_nm):
        json.dump(self.props, open(file_nm, 'w'))

