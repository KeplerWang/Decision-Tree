from math import log


def entropy(data_list: list) -> float:
    """
    @:param data_list 特征或标签的取值列表
    @:return 香农熵
    """
    length = len(data_list)
    count_map = dict()
    for data in data_list:
        try:
            count_map[data] += 1
        except KeyError:
            count_map[data] = 1
    ent = 0.0
    for key in count_map.keys():
        prob = count_map[key] / length
        ent -= prob * log(prob, 2)
    return ent
