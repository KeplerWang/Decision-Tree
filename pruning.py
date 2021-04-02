import copy
from Node import Node
from typing import List
from majority import majority_count


def lost_func(tree: Node, alpha: float):
    leaves_node_list = tree.get_leaves_node()
    c_t = 0.0
    t = len(leaves_node_list)
    for leaf in leaves_node_list:
        c_t += leaf.size * leaf.entropy
    c_alpha_t = c_t + alpha * t
    return c_alpha_t


def pruning(tree: Node, dataset: List[list], alpha: float):
    copy_tree = copy.deepcopy(tree)
    father_map = copy_tree.get_father_node()
    keys = list(father_map.keys())
    keys.reverse()
    for key in keys:
        nodes = father_map[key]
        for node in nodes:
            original_lost = lost_func(tree, alpha)
            sub_dataset = [dataset[i - 1] for i in node.id_list]
            node.tag = majority_count([i[-2] for i in sub_dataset])
            node.children = []
            new_lost = lost_func(copy_tree, alpha)
            if new_lost <= original_lost:
                tree = copy.deepcopy(copy_tree)
    return tree

