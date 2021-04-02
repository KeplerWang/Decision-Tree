from entropy import entropy
from typing import List, Tuple


def split_dataset(dataset: List[list], feature_index: int, value) -> List[list]:
    """
    按照某一特定特征的值对数据进行划分
    :param dataset: 要划分的数据集
    :param feature_index: 参照特征的索引
    :param value: 参照特征的值
    :return: 返回划分结果, 且结果不包含该特征
    """
    sub_dataset = list()
    for data in dataset:
        if data[feature_index] == value:
            temp = data[:feature_index]
            temp.extend(data[feature_index + 1:])
            sub_dataset.append(temp)
    return sub_dataset


def choose_best_feature(dataset: List[list]) -> Tuple[int, float]:
    """
    通过ID3算法, 找出最适合的特征
    :return: 特征的索引、信息增益
    """
    base_entropy = entropy([i[-2] for i in dataset])
    best_feature_index = 0
    max_info_gain = 0.0
    for i in range(len(dataset[0]) - 2):
        sub_entropy = 0.0
        i_value_set = set([example[i] for example in dataset])
        for value in i_value_set:
            sub_dataset = split_dataset(dataset, i, value)
            sub_entropy += len(sub_dataset) / len(dataset) * entropy([example[-2] for example in sub_dataset])
        info_gain = base_entropy - sub_entropy
        if max_info_gain < info_gain:
            best_feature_index = i
            max_info_gain = info_gain
    return best_feature_index, max_info_gain

