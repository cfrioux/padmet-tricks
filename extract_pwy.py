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
    parser.add_argument("-s", "--species",
                        help="padmet species",
                        required=True)
    parser.add_argument("-p", "--pathway",
                        help="pathway name",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="SBML output filename",
                        required=False)

    args = parser.parse_args()

    if args.output:
        outfile = args.output
    else:
        outfile = args.pathway.lower() + ".sbml"

    p_ref = PadmetRef(args.reference) #reads reference padmet
    p_spec = PadmetSpec(args.species) #reads organism padmet

    rxn_list = [rlt.id_in for rlt in p_ref.dicOfRelationOut[args.pathway] if rlt.type == "is_in_pathway" and p_ref.dicOfNode[rlt.id_in].type == "reaction"]

    for rxn_id in rxn_list:
        print(rxn_id)
        p_spec.copyNode(p_ref, rxn_id)
    padmet_to_sbml(p_spec, outfile, sbml_lvl=2, verbose=True)
