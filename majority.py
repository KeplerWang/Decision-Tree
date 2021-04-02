def majority_count(label_list: list) -> any:
    """
    @:param label_list 标签列表
    @:return 列表中出现最多标签
    """
    count_map = dict()
    for data in label_list:
        try:
            count_map[data] += 1
        except KeyError:
            count_map[data] = 1
    max_key = -1
    max_value = 0
    for key, value in count_map.items():
        if value >= max_value:
            max_key = key
            max_value = value
    return max_key
