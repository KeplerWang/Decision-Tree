import pydotplus
import pandas as pd
from Node import Node
from createTree import create_tree
from pruning import pruning


def train(task_name):
    data_id = 1
    if task_name == 'Task1':
        dataset = list()
        file = open('./dataset/Task1/lenses.txt')
        features = [['age', list()], ['prescript', list()], ['astigmatic', list()], ['tear rate', list()]]
        # file = open('./dataset/Task1/melon.txt')
        # features = [['色泽', list()], ['根蒂', list()], ['敲声', list()], ['纹理', list()], ['脐部', list()], ['触感', list()]]
        for line in file.readlines():
            temp = line.strip().split('\t')
            # temp = line.strip().split(',')
            temp.append(data_id)
            for i in range(len(temp[:-2])):
                if not features[i][1].__contains__(temp[i]):
                    features[i][1].append(temp[i])
            dataset.append(temp)
            data_id += 1
        file.close()
    else:
        train_set = pd.read_csv('./dataset/Task2/TrainDT.csv', delimiter=',', encoding='gbk')
        features = list(set(train_set['BSSIDLabel']))
        finLabel = list(set(train_set['finLabel']))
        dataset = list()
        for i in range(len(finLabel)):
            li = [0] * (len(features) + 2)
            li.append(i + 1)
            dataset.append(li)
        for value in train_set.__array__():
            dataset[value[-1] - 1][-2] = value[2]
            dataset[value[-1] - 1][features.index(value[0])] += 1
        for i in range(len(features)):
            features[i] = [features[i], [0, 1]]
    root = Node('root', 1, ['root'], 0.0, 0, [])
    create_tree(root, 0, dataset, features)
    return root.children[0], dataset


def tree_to_pdf(task_name, root, print_flag=False, pruning_flag=False):
    if print_flag:
        root.show()
    if task_name == 'Task1':
        file_path = './result/Task1/lenses' + '{}'.format('_pruning' if pruning_flag else '') + '.dot'
        # file_path = './result/Task1/melon.dot'
    else:
        file_path = './result/Task2/wifi' + '{}'.format('_pruning' if pruning_flag else '') + '.dot'
    file = open(file_path, 'w')
    file.write('digraph tree{\n')
    root.generate_dot(file)
    file.write('}')
    file.close()
    dot_data = open(file_path, 'r').read()
    pydotplus.graph_from_dot_data(dot_data).write_pdf(file_path[:-4] + '_tree.pdf')


if __name__ == '__main__':
    root, dataset = train('Task2')
    tree_to_pdf('Task2', root, print_flag=True)
    tree_to_pdf('Task2', pruning(root, dataset, 15), pruning_flag=True)
