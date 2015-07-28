"""
utils.py
Various helpful bits that don't fit elsewhere!
"""

import sys
import logging
import indra.prop_args as props

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

    # And now we set things running!
    env.run()
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


def get_grid_dims(def_dims):
    pass
