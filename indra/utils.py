"""
utils.py
Various helpful bits that don't fit elsewhere!
"""

import sys
import logging
import indra.prop_args as props


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
