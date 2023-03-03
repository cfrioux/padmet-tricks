# padmet-tricks
Some tiny scripts involving padmet to hack metabolic networks

## Creation of a sbml with desired set of reactions only

`subnetwork.py`

Inputs:

* an empty padmet `data/empty.padmet`
* a list of reactions
* a padmet file with the reactions data
* an output SBML file
* option to remove cofactors (defined in the script) from the reactions

```shell
python subnetwork.py --help
```

## Creation of a sbml with desired set of pathways only

`extract_pathways.py`

Inputs:

* an empty padmet `data/empty.padmet`
* a pathway name
* a padmet file with the reactions data
* an output SBML file

```shell
python extract_pathways.py --help
```

## Analyse the ontology of compounds and pathways in metacyc

`cpd_ontology.py` and `pwy_ontology.py`
build a tree with all parent/children relationships used to describe metabolites and metabolic pathways in Metacyc.

`get_high_lvl_cpds.py` and `get_high_lvl_pwys.py` use the previous ontology (nw file) to get the high level parents of a list of compounds/pathways.
`padmet_cpd_to_highlevel_onto.py` and `padmet_pwys_to_highlevel_onto.py` use the previous ontology (nw file) to get the high level parents of all compounds/pathways from a padmet file.

`get_family_metabolites.py` retrieves the families of given compounds and pathways using families ontology (json file).

`analyse_all_mn_cpds.py` and `analyse_all_mn_pwys.py` analyse the pathways or metabolites of directory of metabolic networks and retrieve for each of them the representation of each category of compounds/pathway using a json ontology of Metacyc. 

`onto_json_to_long_format` create tabulated files out of the json ontologies of pathways. 