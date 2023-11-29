#!python
# -*- coding: utf-8 -*-

from padmet.classes import PadmetSpec
from padmet.classes import PadmetRef
from padmet.utils.connection.sbmlGenerator import padmet_to_sbml, check
import argparse


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reference",
                        help="padmet ref of metacyc",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="SBML output filename",
                        required=False)

    args = parser.parse_args()

    p_ref = PadmetRef(args.reference) #reads reference padmet

    rxn_list = [x for x in p_ref.dicOfNode if p_ref.dicOfNode[x].type == "reaction"]

    rxn_pwy = {}
    for rxn_id in rxn_list:
        rxn_pwy[rxn_id] = [rlt.id_out for rlt in p_ref.dicOfRelationIn[rxn_id] if rlt.type == "is_in_pathway"]

    pwy_dict = {node.id: node for node in p_ref.dicOfNode.values() if node.type == "pathway"}
    pathway_names = {}
    for pid in pwy_dict:
        if 'COMMON-NAME' in pwy_dict[pid].misc:
            pathway_names[pid] = pwy_dict[pid].misc['COMMON-NAME'][0]
        else:
            print(pid)
            pathway_names[pid] = pid

    with open(args.output, "w") as f:
        f.write("reaction\tpathway-id\tpathway-name\n")
        for elem in rxn_pwy:
            for pwy in rxn_pwy[elem]:
                f.write(elem + "\t" + pwy + "\t" + pathway_names[pwy] + "\n")
