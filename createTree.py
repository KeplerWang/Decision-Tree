from majority import majority_count
from chooseBestFeature import *
from Node import Node
from typing import List


def create_tree(node: Node, child_index: int, dataset: List[list], features: List[list]) -> None:
    """
    递归地创建决策树
    :param node: 当前树的根节点, 此后的孩子节点都基于此
    :param child_index: 树根孩子节点的索引, 即将要新建的节点。在根创建时, 其孩子数已经确定了, 因为在确定最佳划分的特征时, 返回了特征的取值集
    :param dataset: 当前操作的数据集
    :param features: 当前操作的特征集
    """
    # 确定数据集 sub_set 的 sub_index 列上有多少种取值
    set_count = lambda sub_set, sub_index: len(set([i[sub_index] for i in sub_set]))
    current_entropy = entropy([i[-2] for i in dataset])
    current_size = len(dataset)
    # 数据集D中样本全部属于同一类别C 将node标记为C类叶节点
    if set_count(dataset, -2) == 1:
        node.children[child_index] = Node(dataset[0][-2], 0, [], current_entropy, current_size,
                                          [i[-1] for i in dataset])
        return
    # 属性集F为空 将node标记为D中样本数最多的E类叶节点
    elif len(features) == 0:
        node.children[child_index] = Node(majority_count([i[-2] for i in dataset]), 0, [], current_entropy,
                                          current_size, [i[-1] for i in dataset])
        return
    # 数据集D中所有样本在属性集A中所有属性上取值相同 将node标记为D中样本数最多的E类叶节点
    tag = True
    for i in range(len(features)):
        if set_count(dataset, i) != 1:
            tag = False
            break
    if tag:
        node.children[child_index] = Node(majority_count([i[-2] for i in dataset]), 0, [], current_entropy,
                                          current_size, [i[-1] for i in dataset])
        return
    best_feature_index, max_info_gain = choose_best_feature(dataset)
    node.children[child_index] = Node(features[best_feature_index][0], len(features[best_feature_index][1]),
                                      features[best_feature_index][1], current_entropy, current_size, [i[-1] for i in dataset])
    sub_feature = features[:best_feature_index]
    sub_feature.extend(features[best_feature_index + 1:])
    for i in range(len(features[best_feature_index][1])):
        sub_dataset = split_dataset(dataset, best_feature_index, features[best_feature_index][1][i])
        if len(sub_dataset):
            create_tree(node.children[child_index], i, sub_dataset, sub_feature)
        else:
            node.children[child_index].children[i] = Node(majority_count([i[-2] for i in dataset]), 0, [], 0.0, 0, [])
