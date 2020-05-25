import sys
from padmet.classes import PadmetSpec
from ete3 import Tree, faces, AttrFace, TreeStyle
import argparse

"""From a padmet ref (metacyc database)
retrieve the ontology of each pathway, recursively.
Build a tree with that ontology
"""

def add_children(tree, node, family_dic):
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
            parent = tree.search_nodes(name = node)[0]
            # add the child of the class name/node
            parent.add_child(name=e)
            # get the children of that child (ie grand children of the original class name)
            # print(tree)
            add_children(tree, e, family_dic)
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

    pwys_id = [node.id for node in padmet.dicOfNode.values() if node.type == "pathway"]

    classes_id = [node.id for node in padmet.dicOfNode.values() if node.type == "class"]

    classes_with_pwys_as_child = {}


    # pathway_classes_instances = set()
    # pathway_classes = {}
    # for pid in pwys_id:
    #     pclasses = [rlt.id_out for rlt in padmet.dicOfRelationIn[pid] if rlt.type == "is_a_class"]
    #     pathway_classes_instances.update(set(pclasses))
    #     pathway_classes[pid] = pclasses

    for pid in pwys_id:
        pclasses = [rlt.id_out for rlt in padmet.dicOfRelationIn[pid] if rlt.type == "is_a_class"]
        if len(pclasses) == 0:
            print(f"Pathway {pid} has no ontology")
        for pclass in pclasses:
            if not pclass in classes_with_pwys_as_child:
                classes_with_pwys_as_child[pclass] = [pid]
            else:
                classes_with_pwys_as_child[pclass].append(pid)


    # classes_parents = {}
    # for cid in classes_id:
    #     try:
    #         ctypes = [rlt.id_out for rlt in padmet.dicOfRelationIn[cid] if rlt.type == "is_a_class"]
    #         # if len(ctypes) != 1:
    #         #     print(cid)
    #         if len(ctypes) == 0 :
    #             print(cid)
    #         classes_parents[cid] = ctypes
    #     except KeyError:
    #         print(f"KE {cid}")


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


    t = Tree(name = "Pathways")

    add_children(t, "Pathways", classes_children)

    for elem in classes_with_pwys_as_child:
        add_children(t, elem, classes_with_pwys_as_child)

    ts = TreeStyle()
    # Do not add leaf names automatically
    ts.show_leaf_name = False
    # ts.show_leaf_name = True
    # Use my custom layout
    ts.layout_fn = my_layout
    ts.mode = "c"
    # ts.arc_start = -360 # 0 degrees = 3 o'clock
    # ts.arc_span = 180
    # t.show(tree_style=ts)
    t.render("mytree.svg", w=300, units="mm",tree_style=ts)


    for node in t.search_nodes(name="PWY-7592"):
        while node:
            print(node.name)
            node = node.up

    print([i.get_ancestors() for i in t.search_nodes(name="PWY-7592")])

    # node = t.search_nodes(name="Arachidonate-Biosynthesis")[0]
    # print(node)


    t.write(outfile=outfile, format=8)

    p = Tree(outfile, format=8)
    p.get_tree_root().name = "Pathways"

    # rf, max_rf, common_leaves, parts_t1, parts_t2 = t.robinson_foulds(p)
    # print( "RF distance is %s over a total of %s" %(rf, max_rf))
    # print( "Partitions in tree2 that were not found in tree1:", parts_t1 - parts_t2)
    # print( "Partitions in tree1 that were not found in tree2:", parts_t2 - parts_t1)