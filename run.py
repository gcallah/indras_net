
import argparse

def run(model_nm):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    print("hello {}! more of me to come!".format(model_nm))


parser = argparse.ArgumentParser(description="parser for command-line savvy users")
parser.add_argument('model_nm', metavar="model_nm", type=str, help="the name of the model you want to run")
args = parser.parse_args()

run(args.model_nm)

