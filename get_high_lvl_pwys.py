import sys
import json
from ete3 import Tree, faces, AttrFace, TreeStyle
import argparse

"""
From a tree of ontology, and a list of pathways,
create a json file with all pathways and the 
categories they fall into
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tree",
                        help="tree ontology of metabolites", required=True)
    parser.add_argument("-j", "--json",
                        help="json output", required=True)
    parser.add_argument("-p", "--pathways",
                        help="pathways file one per line (uncoded)", required=True)

    args = parser.parse_args()

    tree_file = args.tree
    pathways_file = args.pathways
    outfile = args.json

    with open(pathways_file, 'r') as f:
        pathways = [i.strip("\n") for i in f.readlines()]

    ptree = Tree(tree_file, format=8)
    # p.get_tree_root().name = "Chemicals"
    ptree.get_tree_root().name = "Pathways"

    pathways_parent = {}
    pb_pathways = []
    no_ancestor = []

    for elem in pathways:
        try:
            paths = [[a.name for a in i.get_ancestors()] for i in ptree.search_nodes(name=elem)] # GLC Glucopyranose
            if all(i==['Pathways'] for i in paths):
                no_ancestor.append(elem)
            else:
                pathways_parent[elem] = [list(reversed(path))[2] for path in paths]
        except:
            pb_pathways.append(elem)
        # for i in paths: 
        #     print(list(reversed(i)))

    for elem in pathways_parent:
        pathways_parent[elem] = list(set(pathways_parent[elem]))


    with open(outfile, "w") as f:
        json.dump(pathways_parent, f, indent=4)

    parent_to_pathways = {}
    for k,v in pathways_parent.items():
        for x in v:
            parent_to_pathways.setdefault(x,[]).append(k)

    ptp_len = {key: len(value) for key, value in parent_to_pathways.items()}

    sorted_ptp_len = [(k, ptp_len[k]) for k in sorted(ptp_len, key=ptp_len.get, reverse=True)]
    for k, v in sorted_ptp_len:
        print(k, v)
