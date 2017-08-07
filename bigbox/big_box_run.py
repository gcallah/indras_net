"""
A script that runs big_box_model. It simulates the market economy
of consumers, mom and pops, and big boxes.
"""

import indra.utils as utils
import indra.prop_args as props
import bigbox.big_box_model as bb

# set up some file names:
MODEL_NM = "BigBoxModel"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_grid_dims(pa, 50)
        utils.get_agent_num(pa, "num_consumers", "consumers",
                            bb.NUM_GOODS * 5 + 1)
        utils.get_agent_num(pa, "num_mom_and_pops", "mom and pop stores",
                            bb.NUM_GOODS)
        pa.ask("allowance", "What are the consumers' daily allowances?", 
               int, default=2)
    # right now, big box gets a multiple of m&p expenses and endowment
        pa.ask("endowment", "What are the small shops' initial endowments?", 
               int, default=30)
        pa.ask("expenses", "What are the small shops' expenses per period?",
               int, default=10)
        pa.ask("bb_start_period", "At what period should big boxes appear?",
               int, default=20, limits=(1, 100))
        pa.ask("pref_for_mp",
               "What's the consumer preference for mom and pops?",
               float, default=0.2, limits=(0.0, 1.0))
    # Now we create a town for our agents to act in:
    env = bb.EverytownUSA(pa.get("grid_width"),
                          pa.get("grid_height"),
                          model_nm=MODEL_NM,
                          props=pa)
    # Now we loop creating multiple agents with numbered names
    # based on the number of agents of that type to create:
    for i in range(pa.get("num_consumers")):
        env.add_agent(bb.Consumer("consumer" + str(i),
                                  goal=(i % bb.NUM_GOODS),
                                  init_state=0,
                                  allowance=pa.get("allowance")))
    for i in range(pa.get("num_mom_and_pops")):
        env.add_agent(bb.MomAndPop("mom_and_pop" + str(i),
                                   goal=(i % bb.NUM_GOODS),
                                   endowment=pa.get("endowment"),
                                   expenses=pa.get("expenses"),
                                   adj=pa.get("pref_for_mp")
                                   ))
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
