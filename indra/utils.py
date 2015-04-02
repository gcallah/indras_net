"""
utils.py
Various helpful bits that don't fit elsewhere!
"""


def gen_file_names(model_nm):
    """
    Generate our standard list of I/O spots.
    """
    prog_file = model_nm + ".py"
    log_file = model_nm + ".log"
    prog_file = model_nm + ".props"
    rsul_file = model_nm + ".out"
    return (prog_file, log_file, prog_file, rsul_file)
