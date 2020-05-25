import json
import argparse
from os import listdir, makedirs
from os.path import isdir
from padmet.utils.sbmlPlugin import convert_from_coded_id

"""
Analyse a list of metabolites given as input (file)
Get the ontology of these compounds
"""

def get_args():
    """
    get arguments of the script and call the main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="text file, one compound per line", required=True)
    parser.add_argument("-j", "--jsononto",
                        help="json ontology of families", required=True)
    parser.add_argument("-o", "--output",
                        help="output file", required=True)
    parser.add_argument("-e", "--encoded",
                        help="identifiers are encoded", action="store_true", default=False)

    args = parser.parse_args()

    run_analysis(args.input, args.jsononto, args.output, args.encoded)

def run_analysis(inp_file, json_onto_file, out_file, encoded):
    """get families of a list of compounds
    
    Args:
        inp_file (str): path to input dir
        json_onto_file (str): json ontology file for compounds
        output_dir (str): path to output dir
        encoded (Bool): encoding of the metabolites names as SBML IDs
    """
    with open(json_onto_file, "r") as f:
        family_dict = json.load(f) 

    res_dict = {}

    # git list of compounds to identify
    with open(inp_file, "r") as f:
        compounds_raw = [i.strip("\n") for i in f.readlines()]

    if encoded:
        compounds = [convert_from_coded_id(i)[0] for i in compounds_raw]
    else:
        compounds = compounds_raw

    for elem in compounds:
        if elem in family_dict:
            res_dict[elem] = family_dict[elem]
        else:
            res_dict[elem] = ["Others"]
    
    # write to file the ontology of compounds in comm_scope for each dir
    with open(out_file, "w") as g:
        for cpd in res_dict:
            g.write(cpd + '\t' + ",".join(res_dict[cpd]) + '\n')

    return

if __name__ == "__main__":
    get_args()