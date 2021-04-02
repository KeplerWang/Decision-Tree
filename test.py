import pandas as pd
from Node import Node
from pruning import pruning
from train import train


def test(data: list, features: list, tree: Node):
    if not len(tree.children):
        return tree.tag
    else:
        for i in range(len(tree.children)):
            if data[features.index(tree.tag)] == tree.conditions[i]:
                return test(data, features, tree.children[i])


if __name__ == '__main__':
    train_set = pd.read_csv('./dataset/Task2/TrainDT.csv', delimiter=',', encoding='gbk')
    features = list(set(train_set['BSSIDLabel']))
    finLabel = list(set(train_set['finLabel']))
    test_set = pd.read_csv('./dataset/Task2/TestDT.csv', delimiter=',', encoding='gbk')
    test_dataset = list()
    for i in range(len(finLabel)):
        li = [0] * (len(features) + 2)
        li.append(i + 1)
        test_dataset.append(li)
    for value in train_set.__array__():
        test_dataset[value[-1] - 1][-2] = value[2]
        test_dataset[value[-1] - 1][features.index(value[0])] += 1
    root, dataset = train('Task2')
    root = pruning(root, dataset, 0)
    correct = 0
    number = len(test_dataset)
    for data in test_dataset:
        if test(data, features, root) == data[-2]:
            correct += 1
    print(0, correct, number, '%.2f%%' % (correct/number*100))
