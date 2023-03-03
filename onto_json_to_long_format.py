import argparse
import json
from padmet.utils.sbmlPlugin import convert_from_coded_id
from padmet.classes import PadmetRef

"""
Starting from an ontology of compounds into families and a directory of metabolic networks, retrieve for each MN the metabolites it contains and add 1 to each family of these metabolites
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json",
                        help="json file of family ontologies",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="output filename (tabulated file)",
                        required=True)
    parser.add_argument("-t", "--type",
                        help="type of ontology (either 'pathway' or 'compound')",
                        required=True,
                        choices=["pathway", "compound"])
    parser.add_argument("-p", "--padmet",
                        help="padmet file of the metabolic database",
                        required=True)

    args = parser.parse_args()

    # read inputs
    with open(args.json, "r") as f:
        raw = json.load(f)
    
    p_ref = PadmetRef(args.padmet) #reads reference padmet

    if args.type == "pathway":
        pathway_list =  {node.id: node for node in p_ref.dicOfNode.values() if node.type == "pathway"}
        pathway_names = {}

        for pid in pathway_list:
            if 'COMMON-NAME' in pathway_list[pid].misc:
                pathway_names[pid] = pathway_list[pid].misc['COMMON-NAME'][0]
            else:
                print(pid)
                pathway_names[pid] = pid
        
        with open(args.output, "w") as f:
            f.write(f"pathway_id\tpathway_name\tcategory\n")
            for pid in raw:
                for category in raw[pid]:
                    if pid in pathway_names:
                        f.write(f"{pid}\t{pathway_names[pid]}\t{category}\n")
                    else:
                        print(pid)
                        f.write(f"{pid}\t{pid}\t{category}\n")

    elif args.type == "compound":
        cpd_list =  {node.id: node for node in p_ref.dicOfNode.values() if node.type == "compound"}
        cpd_names = {}
        compounds_no_names = []

        for pid in cpd_list:
            if 'COMMON-NAME' in cpd_list[pid].misc:
                cpd_names[pid] = cpd_list[pid].misc['COMMON-NAME'][0]
            else:
                compounds_no_names.append(pid)
                cpd_names[pid] = pid

        print(f"{len(compounds_no_names)} compounds have no name")

        with open(args.output, "w") as f:
            f.write(f"compound_id\tcompound_name\tcategory\n")
            for pid in raw:
                for category in raw[pid]:
                    if pid in cpd_names:
                        f.write(f"{pid}\t{cpd_names[pid]}\t{category}\n")
                    else:
                        print(pid)
                        f.write(f"{pid}\t{pid}\t{category}\n")