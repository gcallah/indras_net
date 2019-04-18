"""
forestfire_model.py
Adapted from the George Mason mesa project.
This model shows the spread of a forest fire through a forest.
"""

# import indra.display_methods as disp
# import indra.markov as markov
# import indra.markov_agent as ma
# import indra.markov_env as menv


X = 0
Y = 1

# tree condition strings
HEALTHY = "Healthy"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

# states
HE = 0
OF = 1
BO = 2
NG = 3

STATE_MAP = {HE: HEALTHY, OF: ON_FIRE, BO: BURNED_OUT, NG: NEW_GROWTH}

NSTATES = 4

NORMAL_TRANS = ".9995 .0005 0 0; 0 0 1 0; 0 0 .90 .10; 1 0 0 0"
FIRE_TRANS = "0 1 0 0; 0 0 1 0; 0 0 .90 .10; .30 .70 0 0"


class Tree():
    '''
    A tree cell.

    Attributes:
        condition: Can be "New Growth", "Healthy", "On Fire", or "Burned Out"

    '''
    def __init__(self, name):
        '''
        Create a new tree.
        '''
        super().__init__(name, "health", NSTATES, HE)
        self.state = HE
        self.ntype = STATE_MAP[HE]
        self.next_state = None

    def is_healthy(self):
        return self.state == HE or self.state == NG

    def set_state(self, new_state):
        """
        Set tree's new type.
        """
        old_type = self.ntype
        self.state = new_state
        self.ntype = STATE_MAP[new_state]
        self.env.change_agent_type(self, old_type, self.ntype)

    def postact(self):
        """
        Set our type to next_state.
        """
        if self.next_state is not None and self.next_state != self.state:
            # print("Setting state to " + str(self.next_state))
            self.set_state(self.next_state)
            self.next_state = None

        return self.pos

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["state"] = self.state
        safe_fields["ntype"] = self.ntype
        safe_fields["next_state"] = self.next_state

        return safe_fields

    def from_json_preadd(self, json_input):
        super().from_json_preadd(json_input)
        self.state = json_input["state"]
        self.ntype = json_input["ntype"]
        self.next_state = json_input["next_state"]


class ForestEnv():
    '''
    Simple Forest Fire model.
    '''
    def __init__(self, width, height, density, strike_freq, regen_period,
                 torus=False, model_nm="ForestFire", postact=True,
                 props=None):
        '''
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        # Initialize model parameters
        super().__init__("Forest Fire", width, height, NORMAL_TRANS,
                         torus=False, model_nm=model_nm, postact=postact,
                         props=props)
        self.density = density
        self.plot_title = "A Forest Fire"
        # set up our two possible transition matrices:
        # self.normal = markov.MarkovPre(NORMAL_TRANS)
        # self.fire = markov.MarkovPre(FIRE_TRANS)

    def get_pre(self, agent, n_census):
        if (ON_FIRE in n_census) and (n_census[ON_FIRE] > 0):
            return self.fire
        else:
            return self.normal

    # def set_agent_color(self):
        # setting our colors adds varieties as well!
        # self.set_var_color(BURNED_OUT, disp.BLACK)
        # self.set_var_color(ON_FIRE, disp.RED)
        # self.set_var_color(HEALTHY, disp.GREEN)
        # self.set_var_color(NEW_GROWTH, disp.CYAN)
    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["density"] = self.density
        safe_fields["plot_title"] = self.plot_title
        safe_fields["normal"] = self.normal.to_json()
        safe_fields["fire"] = self.fire.to_json()
        return safe_fields
    # def from_json(self, json_input):
        # super().from_json(json_input)
        # self.density = json_input["density"]
        # self.plot_title = json_input["plot_title"]
        # self.normal.from_json(json_input["normal"])
        # self.fire.from_json(json_input["fire"])
    # def restore_agent(self, agent_json):
    # #     new_agent = Tree(name=agent_json["name"])
    #     self.add_agent_to_grid(new_agent, agent_json)
