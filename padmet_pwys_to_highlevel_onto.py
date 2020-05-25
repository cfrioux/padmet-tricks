import sys
from padmet.classes import PadmetSpec
from ete3 import Tree
import json
import argparse

"""
For all pathways in padmetRef file,
retrieve its high level ontologies.
Create a json with the ontologies of all pathways
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tree",
                        help="tree ontology of metabolites", required=True)
    parser.add_argument("-j1", "--json1",
                        help="json output level 1 of parents", required=True)
    parser.add_argument("-j2", "--json2",
                        help="json output level 2 of parents", required=True)
    parser.add_argument("-p", "--padmet",
                        help="padmet file", required=True)

    args = parser.parse_args()

    padmet_file = args.padmet
    outfile_l1 = args.json1
    outfile_l2 = args.json2
    tree_file = args.tree

    padmet = PadmetSpec(padmet_file)

    padmet_cpds = [node.id for node in padmet.dicOfNode.values() if node.type == "pathway"]


    p = Tree(tree_file, format=8)
    # p.get_tree_root().name = "Chemicals"
    p.get_tree_root().name = "Pathways"

    # paths = [[a.name for a in i.get_ancestors()] for i in t.search_nodes(name="D-Glucose")] # GLC Glucopyranose
    # for i in paths: 
    #      print(list(reversed(i)))

    # coi="3-HYDROXY-L-KYNURENINE"

    onto = {}
    onto_l2 = {}

    for cpd in padmet_cpds:
        # print(cpd)
        paths = [list(reversed([a.name for a in i.get_ancestors()])) for i in p.search_nodes(name=cpd)] # GLC Glucopyranose
        onto[cpd] = [i[1] for i in paths if len(i) > 1]
        if len(onto[cpd]) == 0:
            onto[cpd] = ["Others"]
        onto_l2[cpd] = [i[2] for i in paths if len(i) > 2]
        if len(onto_l2[cpd]) == 0:
            onto_l2[cpd] = ["Others"]
            # print(cpd, paths)

    # clean duplicates

    for elem in onto:
        onto[elem] = list(set(onto[elem]))

    for elem in onto_l2:
        onto_l2[elem] = list(set(onto_l2[elem]))

    with open(outfile_l1, "w") as g:
        json.dump(onto, g, indent=4, sort_keys=True)

    with open(outfile_l2, "w") as g:
        json.dump(onto_l2, g, indent=4, sort_keys=True)
