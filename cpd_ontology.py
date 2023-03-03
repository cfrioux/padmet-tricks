import sys
from padmet.classes import PadmetSpec
from ete3 import Tree, faces, AttrFace, TreeStyle
import argparse


"""From a padmet ref (metacyc database)
retrieve the ontology of each compound, recursively.
Build a tree with that ontology
"""

def add_children(tree, node, family_dic, existing):
    """Recursively add the children of an item.

    Args:
        tree (Tree): Tree object
        node (str): node of interest
        family_dic (dict): dictionary of parent/child relationships

    Returns:
        Tree: updated tree
    """
    if node in family_dic:
        # for all children of this class
        for e in family_dic[node]:
            # get the node associated to the considered class name
            # parent = tree.search_nodes(name = node)[0]
            # add the child of the class name/node
            for parent in tree.search_nodes(name = node):
                if not (parent,e) in existing:
                    parent.add_child(name=e)
                    existing.append((parent,e))
            # [parent.add_child(name=e) for parent in tree.search_nodes(name = node)]
            # get the children of that child (ie grand children of the original class name)
            # print(tree)
            add_children(tree, e, family_dic, existing)
    else:
        # print(f"{node} has no child")
        return tree

def my_layout(node):
    """Customise the layout of a tree node

    Args:
        node (node): tree node
    """
    if node.is_leaf():
        # If terminal node, draws its name
        name_face = AttrFace("name")
    else:
        # If internal node, draws label with smaller font size
        name_face = AttrFace("name", fsize=10)
    # Adds the name face to the image at the preferred position
    faces.add_face_to_node(name_face, node, column=0, position="branch-right")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--padmet",
                        help="padmet file (of the whole metacyc DB)",
                        required=True)
    parser.add_argument("-t", "--tree",
                        help="output filename for tree",
                        required=True)
    parser.add_argument("-s", "--svg",
                        help="output filename for tree viz",
                        required=True)

    args = parser.parse_args()


    padmet_file = args.padmet #"metacyc_231.padmet"
    outfile = args.tree #"pathways_onto.nw"
    tree_file = args.svg #"pwy_tree.svg" #

    padmet = PadmetSpec(padmet_file)

    cpd_id = [node.id for node in padmet.dicOfNode.values() if node.type == "compound"]

    classes_id = [node.id for node in padmet.dicOfNode.values() if node.type == "class"]

    classes_with_cpd_as_child = {}

    # all child relationships between a class and a compound
    # the key is the class, the value is the list of children compounds IDs
    for mid in cpd_id:
        try:
            mclasses = [rlt.id_out for rlt in padmet.dicOfRelationIn[mid] if rlt.type == "is_a_class"]
            if len(mclasses) == 0:
                print(f"Metabolite {mid} has no ontology")
            for mclass in mclasses:
                if not mclass in classes_with_cpd_as_child:
                    classes_with_cpd_as_child[mclass] = [mid]
                else:
                    classes_with_cpd_as_child[mclass].append(mid)
        except KeyError:
            print(f"Key error: {mid}")

    # all child relationships between the classes of classes.dat
    # the key is the parent, the value is a list of children
    classes_children = {}
    for cid in classes_id:
        try:
            ctypes = [rlt.id_out for rlt in padmet.dicOfRelationIn[cid] if rlt.type == "is_a_class"]
            for ctype in ctypes:
                if not ctype in classes_children:
                    classes_children[ctype] = [cid]
                else:
                    classes_children[ctype].append(cid)
        except KeyError:
            print(f"{cid} has no parents")


    # t = Tree(name = "Chemicals")
    t = Tree(name = "Compounds")

    already_done = []
    # add_children(t, "Chemicals", classes_children)
    add_children(t, "Compounds", classes_children, already_done)

    for elem in classes_with_cpd_as_child:
        add_children(t, elem, classes_with_cpd_as_child, already_done)


    for node in t.search_nodes(name="GLC"):
        while node:
            print(node.name)
            node = node.up

    [i.get_ancestors() for i in t.search_nodes(name="GLC")]

    # node = t.search_nodes(name="GLC")[0]
    # print(node)


    t.write(outfile=outfile, format=8)

    # p = Tree(outfile, format=8)
    # # p.get_tree_root().name = "Chemicals"
    # p.get_tree_root().name = "Compounds"

    # # paths = [[a.name for a in i.get_ancestors()] for i in t.search_nodes(name="D-Glucose")] # GLC Glucopyranose
    # # for i in paths: 
    # #      print(list(reversed(i)))


    # paths = [[a.name for a in i.get_ancestors()] for i in p.search_nodes(name="D-Glucose")] # GLC Glucopyranose
    # for i in paths: 
    #     print(list(reversed(i)))

    # ts = TreeStyle()
    # # Do not add leaf names automatically
    # ts.show_leaf_name = False
    # # ts.show_leaf_name = True
    # # Use my custom layout
    # ts.layout_fn = my_layout
    # ts.mode = "c"
    # # ts.arc_start = -360 # 0 degrees = 3 o'clock
    # # ts.arc_span = 180
    # # t.show(tree_style=ts)
    # p.render(tree_file, w=300, units="mm",tree_style=ts)


    # rf, max_rf, common_leaves, parts_t1, parts_t2 = t.robinson_foulds(p)
    # print( "RF distance is %s over a total of %s" %(rf, max_rf))
    # print( "Partitions in tree2 that were not found in tree1:", parts_t1 - parts_t2)
    # print( "Partitions in tree1 that were not found in tree2:", parts_t2 - parts_t1)