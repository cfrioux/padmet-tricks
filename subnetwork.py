from padmet.classes import PadmetSpec
from padmet.classes import PadmetSpec
from padmet.classes import PadmetRef
from padmet.utils.connection.sbmlGenerator import padmet_to_sbml, check
from padmet.utils.sbmlPlugin import convert_from_coded_id
import argparse

RXN_LIST=['R_S__45__ADENMETSYN__45__RXN', 'R_RXN0__45__268']


COFACTORS = ['M_NAD_c','M_ATP_c', 'M_NADH_c', 'M_NADPH_c', 'M_NADP_c', 'M_AMP_c', 'M_ADP_c', 'M_WATER_c', 'M_Pi_c']

def reduce_network(padmet_file:str, empty_padmet:str, reaction_list:list, sbml_output:str, del_cof:bool=False):
    """Create a sbml starting with the desired reactions.

    Args:
        padmet_file (str): path to padmet containing all reactions
        empty_padmet (str): path to empty padmet that will be filled
        reaction_list (list): list of reactions to be retrieved
        sbml_output (str): path to sbml file to be written
    """
    p_ref = PadmetRef(padmet_file)
    p_spec = PadmetSpec(empty_padmet)

    # retrieve reactions from a given pathway
    # rxn_list = [rlt.id_in for rlt in p_ref.dicOfRelationOut[args.pathway] if rlt.type == "is_in_pathway" and p_ref.dicOfNode[rlt.id_in].type == "reaction"]

    reaction_list = [convert_from_coded_id(i)[0] for i in reaction_list]

    for rxn_id in reaction_list:
        p_spec.copyNode(p_ref, rxn_id)
    # p_spec.generateFile("plop.padmet")

    cofactor_list = [convert_from_coded_id(i)[0] for i in COFACTORS]

    if del_cof:
        for rxn_id in reaction_list:
            cof_linked_rlt = [rlt for rlt in p_spec.dicOfRelationIn[rxn_id] if rlt.id_out in cofactor_list]
            for rel in cof_linked_rlt:
                p_spec._delRelation(rel)

    padmet_to_sbml(p_spec, sbml_output, sbml_lvl=3, verbose=True)

    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reference",
                        help="padmet ref from which reactions will be retrieved",
                        required=True)
    parser.add_argument("-e", "--empty",
                        help="empty padmet to be filled",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="SBML output filename",
                        required=True)
    parser.add_argument("-l", "--listofrxn",
                        help="File with reactions, one per line",
                        required=False)
    parser.add_argument("-d", "--delcof",
                        help="Delete cofactors",
                        required=False,
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    if args.listofrxn:
        with open(args.listofrxn, 'r') as f:
            rxn_list = [i.strip('\n') for i in f.readlines()]
    else:
        rxn_list = RXN_LIST

    reduce_network(padmet_file=args.reference, empty_padmet=args.empty, reaction_list=rxn_list, sbml_output= args.output, del_cof=args.delcof)
