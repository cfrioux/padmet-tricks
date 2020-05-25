import sys
import os
import json
import glob
from padmet.utils.sbmlPlugin import convert_from_coded_id
from libsbml import SBMLReader, SBMLDocument
import argparse

"""
Starting from an ontology of pathways into families and a directory of padmet reports for metabolic networks, retrieve for each MN the pathways it contains and add 1 to each family of these pathways
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

    mn_report_dir = args.dir
    json_family = args.json
    outfile = args.output

    pwy_by_mn = {}


    for mn in glob.glob(mn_report_dir + '/*/*pathways*'):
        with open(mn, "r") as f:
            pwy_by_mn[mn] = [i.split("\t")[0] for i in f.readlines()[1:]]

    with open(json_family, "r") as f:
        family_dict = json.load(f) 

    # count_dict = {i:0 for i in list(set(sum(family_dict.values(), [])))}
    families_by_mn = {}

    for mn in pwy_by_mn:
        families_by_mn[mn] = {i:0 for i in list(set(sum(family_dict.values(), [])))}
        families_by_mn[mn]["unknown"] = 0
        for elem in pwy_by_mn[mn]:
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
