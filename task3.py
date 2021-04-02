import numpy as np
import pydotplus
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


f_data = open('./dataset/Task3/train_data.txt')
f_label = open('./dataset/Task3/train_labels.txt')
test_data = open('./dataset/Task3/test_data.txt')
test_label = open('./dataset/Task3/test_labels.txt', 'w')
x_train_set = list()
y_train_set = list()
x_test_set = list()
for line in f_data.readlines():
    package = [0] * 10000
    for i in line.strip().split(' '):
        package[int(i) - 1] = 1
    x_train_set.append(package)
    y_train_set.append(int(f_label.readline().strip()))

for line in test_data.readlines():
    package = [0] * 10000
    for i in line.strip().split(' '):
        package[int(i) - 1] = 1
    x_test_set.append(package)

f_data.close()
f_label.close()
test_data.close()

x_train_set = np.array(x_train_set, dtype=np.int8)
y_train_set = np.array(y_train_set, dtype=np.int8)

x_train, x_valid, y_valid, y_test = train_test_split(x_train_set, y_train_set, test_size=0.2)
clf = DecisionTreeClassifier(max_depth=17)
clf = clf.fit(x_train, y_valid)
# dot_data = tree.export_graphviz(clf, out_file=None, class_names=['0', '1'], filled=True, rounded=True,
                                # special_characters=True)
# graph = pydotplus.graph_from_dot_data(dot_data)
# graph.write_pdf("./result/Task3/imdb_tree.pdf")
y_valid_pred = clf.predict(x_valid)
print("正确值：\n{0}".format(y_test))
print("预测值：\n{0}".format(y_valid_pred))
print("准确率：%f%%" % (accuracy_score(y_test, y_valid_pred) * 100))

y_test_pred = clf.predict(x_test_set)
for i in y_test_pred:
    test_label.write(str(i)+'\n')
test_label.close()
