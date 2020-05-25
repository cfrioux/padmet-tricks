import sys
from ete3 import Tree, faces, AttrFace, TreeStyle
import json
from collections import Counter
import argparse

"""
From a tree of ontology, and a list of compounds,
create a json file with all compounds and the 
categories they fall into
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tree",
                        help="tree ontology of metabolites", required=True)
    parser.add_argument("-j", "--json",
                        help="json output", required=True)
    parser.add_argument("-c", "--compounds",
                        help="metabolites file one per line (uncoded)", required=True)

    args = parser.parse_args()

    tree_file = args.tree
    compounds_file = args.compounds
    outfile = args.json

    with open(compounds_file, 'r') as f:
        compounds = [i.strip("\n") for i in f.readlines()]

    ctree = Tree(tree_file, format=8)
    # p.get_tree_root().name = "Chemicals"
    ctree.get_tree_root().name = "Compounds"

    compounds_parent = {}
    pb_compounds = []
    no_ancestor = []

    for elem in compounds:
        try:
            paths = [[a.name for a in i.get_ancestors()] for i in ctree.search_nodes(name=elem)] # GLC Glucopyranose
            if all(i==['Compounds'] for i in paths):
                no_ancestor.append(elem)
            else:
                compounds_parent[elem] = [list(reversed(path))[1] for path in paths]
        except:
            pb_compounds.append(elem)
        # for i in paths: 
        #     print(list(reversed(i)))

    for elem in compounds_parent:
        compounds_parent[elem] = list(set(compounds_parent[elem]))

    with open(outfile, "w") as f:
        json.dump(compounds_parent, f, indent=4)

    all_cats = list(set(sum(compounds_parent.values(), [])))

    parent_to_compounds = {}
    for k,v in compounds_parent.items():
        for x in v:
            parent_to_compounds.setdefault(x,[]).append(k)

    ptc_len = {key: len(value) for key, value in parent_to_compounds.items()}

    sorted_ptc_len = [(k, ptc_len[k]) for k in sorted(ptc_len, key=ptc_len.get, reverse=True)]
    for k, v in sorted_ptc_len:
        print(k, v)
