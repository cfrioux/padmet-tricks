import sys
import os
import argparse
import json
from padmet.utils.sbmlPlugin import convert_from_coded_id
from libsbml import SBMLReader, SBMLDocument

"""
Starting from an ontology of compounds into families and a directory of metabolic networks, retrieve for each MN the metabolites it contains and add 1 to each family of these metabolites
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir",
                        help="directory of metabolic networks",
                        required=True)
    parser.add_argument("-j", "--json",
                        help="json file of family ontologies",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="output filename for families statistics",
                        required=True)

    args = parser.parse_args()


    mn_dir = args.dir
    json_family = args.json
    outfile = args.output

    species_by_mn = {}

    for mn in os.listdir(mn_dir):
        print(mn)
        mn_name = mn.rstrip(".sbml")
        reader = SBMLReader()
        model = reader.readSBML(mn_dir + '/' + mn).getModel()
        species = [convert_from_coded_id(i.getId())[0] for i in model.getListOfSpecies()]
        species_by_mn[mn_name] = species

    with open(json_family, "r") as f:
        family_dict = json.load(f) 

    # count_dict = {i:0 for i in list(set(sum(family_dict.values(), [])))}
    families_by_mn = {}

    for mn in species_by_mn:
        families_by_mn[mn] = {i:0 for i in list(set(sum(family_dict.values(), [])))}
        families_by_mn[mn]["unknown"] = 0
        for elem in species_by_mn[mn]:
            if elem in family_dict:
                for fam in family_dict[elem]:
                    # count_dict[elem] +=1
                    families_by_mn[mn][fam] += 1
            else:
                families_by_mn[mn]["unknown"] += 1

    with open(outfile, "w") as g:
        for mn in families_by_mn:
            for elem in families_by_mn[mn]:
                g.write(mn + '\t' + elem + '\t' + str(families_by_mn[mn][elem]) + '\n')
