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