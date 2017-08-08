"""
utils.py
Various helpful bits that don't fit elsewhere!
"""

import sys
import logging
import indra.prop_args as props
import indra.data_methods as data

# some values useful for checking valid ranges:
BIG_INT = sys.maxsize
BTWN_ZERO_ONE = (.01, .99)
NTRL_NUMS = (0, BIG_INT)
POS_INTS = (1, BIG_INT)
MAX_GRID = 100000
GRID_LIMITS = (1, MAX_GRID)  # this gives us a max grid of 1 billion elements!
MAX_AGENTS = MAX_GRID * MAX_GRID  # enough to fill a maximum sized grid
AGENT_LIMITS = (1, MAX_AGENTS)


def gen_file_names(model_nm):
    """
    Generate our standard list of I/O spots.
    """
    prog_file = model_nm + ".py"
    log_file = model_nm + ".log"
    prop_file = model_nm + ".props"
    rsul_file = model_nm + ".out"
    return (prog_file, log_file, prop_file, rsul_file)


def run_model(env, prog_file, results_file):
    # Logging is automatically set up for the modeler:
    logging.info("Starting program " + prog_file)

    periods = env.props.get(props.PERIODS)
    if periods is None:
        periods = 0
    else:
        periods = int(periods)
    # And now we set things running!
    env.run(periods=periods)
    env.record_results(results_file)


def read_props(model_nm):
    """
    A prop file to read must be our first arg, if it exists.
    """
    if len(sys.argv) > 1:
        poss_props = sys.argv[1]
        if not poss_props.startswith('-'):  # not a property but a prop file
            return props.PropArgs.read_props(model_nm, poss_props)

    return None


def get_grid_dims(pa, def_dims):
    pa.ask("grid_width", "What is the grid width?", int, default=def_dims,
           limits=GRID_LIMITS)
    pa.ask("grid_height", "What is the grid height?", int, default=def_dims,
           limits=GRID_LIMITS)


def get_agent_num(pa, prop_nm, agent_type, def_num):
    pa.ask(prop_nm, "What is the number of %s?" % (agent_type),
           int, default=def_num, limits=AGENT_LIMITS)


def get_max_move(pa, prop_nm, agent_type, def_move):
    pa.ask(prop_nm, "What is %s's maximum move?" % (agent_type),
           int, default=def_move, limits=AGENT_LIMITS)


def get_pct(pa, prop_nm, agent_type, param_descr, def_pct):
    pa.ask(prop_nm, "What is %s's %s?" % (agent_type, param_descr),
           float, default=def_pct, limits=BTWN_ZERO_ONE)
