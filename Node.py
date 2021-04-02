class Node:
    __counter = 0  # 用于生成各个Node的id

    def __init__(self, tag, children_num: int, conditions: list, entropy: float, size: int, id_list: list):
        if children_num != len(conditions):
            raise Exception
        self.children = [Node('', 0, [], 0.0, 0, [])] * children_num if children_num else []
        self.tag = tag
        self.conditions = conditions
        self.entropy = entropy
        self.size = size
        self.__node_id = self.__counter
        self.id_list = id_list
        Node.__counter += 1

    def get_leaves_node(self, leaves_node_list=None):
        """
        寻找所有叶子节点
        :return: list
        """
        if leaves_node_list is None:
            leaves_node_list = list()
        if not len(self.children):
            leaves_node_list.append(self)
        else:
            for child in self.children:
                child.get_leaves_node(leaves_node_list)
        return leaves_node_list

    def get_father_node(self, base_depth=1, node_depth_map=None):
        """
        寻找所有非叶节点及其深度
        @:return dict 深度为key 节点为value
        """
        if node_depth_map is None:
            node_depth_map = {}
        try:
            node_depth_map[base_depth].append(self)
        except KeyError:
            node_depth_map[base_depth] = [self, ]
        for child in self.children:
            if len(child.children):
                child.get_father_node(base_depth + 1, node_depth_map)
        return node_depth_map

    def show(self, n=0):
        """
        在命令行打印打印树
        """
        if len(self.children) == 0:
            print('|   ' * n + '|--- class: ' + str(self.tag))
            # print('|   ' * n + '|--- class: ' + str(self.tag) + ' entropy:', self.entropy, 'size:', self.size)
        else:
            for i in range(len(self.children)):
                print('|   ' * n + '|--- feature: ' + str(self.tag) + ' = ' + str(self.conditions[i]))
                # print('|   ' * n + '|--- feature: ' + str(self.tag) + ' = '
                #       + str(self.conditions[i]) + ' entropy:', self.entropy, 'size:', self.size)
                self.children[i].show(n + 1)

    def generate_dot(self, file_descriptor):
        """
        生产dot文件
        :param file_descriptor: dot文件的文件描述符
        """
        if len(self.children) == 0:
            file_descriptor.write(str(self.__node_id) + '[shape=box, label="class: ' + str(self.tag)
                                  + '\nsample number: ' + str(self.size)
                                  + '\nentropy: ' + str(self.entropy)[:6] + '"];\n')
                                  # + '\nid list: ' + str(self.id_list) + '"];\n')
            return
        else:
            file_descriptor.write(str(self.__node_id) + '[label="feature: ' + str(self.tag)
                                  + '\nsample number: ' + str(self.size)
                                  + '\nentropy: ' + str(self.entropy)[:6] + '"];\n')
            for i in range(len(self.children)):
                self.children[i].generate_dot(file_descriptor)
                file_descriptor.write(str(self.__node_id) + '->' + str(self.children[i].__node_id) + '[label="'
                                      + str(self.conditions[i]) + '"];\n')
