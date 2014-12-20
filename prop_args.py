
class PropArgs:

    prop_sets = {}


    @staticmethod
    def get_props(prog_nm):
        if prog_nm in PropArgs.prop_sets:
            print("Found " + prog_nm + " in prop_sets")
            return PropArgs.prop_sets[prog_nm]
        else:
            print("Did not find " + prog_nm + " in prop_sets")
            return(PropArgs(prog_nm))


    def __init__(self, prog_nm):
        self.prog_nm = prog_nm
# store this instance as the value in the dict for 'prog_nm'
        PropArgs.prop_sets[prog_nm] = self
        self.props = {}


    def set(self, nm, val):
        self.props[nm] = val


    def get(self, nm, default=None):
        if nm not in self.props:
            self.props[nm] = default
        return self.props[nm]


