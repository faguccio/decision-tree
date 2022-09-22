import math
import random

#random.seed(123)



def xor(a, b):
    return bool( (a and not b) or (b and not a) )

def get_data():
    with open('magic04.data') as file:
        lines = file.readlines()
        y = []

        for i in range(len(lines)):
            line = lines[i].split(",")
            for j in range(len(line) -1):
                line[j] = float(line[j])

            y.append(line.pop(-1)[0])
            lines[i] = line
       
        return lines, y


def split_dataset(X, y, percent=0.8):
    indexes = list(range(len(X)))
    random.shuffle(indexes)
    trainX, trainY, pruneX, pruneY = [], [], [], []
    for i in range(len(X)):
        if i < int(len(X) * percent):
            trainX.append(X[indexes[i]])
            trainY.append(y[indexes[i]])
        else:
            pruneX.append(X[indexes[i]])
            pruneY.append(y[indexes[i]])
    return trainX, trainY, pruneX, pruneY



def entropy(label_table,y):
    entropy = 0
    for label_count in label_table.values():
        entropy -= (label_count/len(y) * math.log(label_count/len(y), 2) )

    return entropy


def gini(label_table,y):
    gini = 0
    for label_count in label_table.values():
        gini += (label_count/len(y) * (1-(label_count/len(y))))

    return gini


def compute_occurencies(y):
        label_table = {}

        for label in y:
            if  label in label_table.keys():
                label_table[label] += 1
            else:
                label_table[label] = 1
       
        return label_table


class dataset:
    def __init__(self, X, y, impurity = 'entropy'):
        self.X = X
        self.y = y
        self.label_table = compute_occurencies(y)
        if impurity == 'gini':
            self.impurity = gini(self.label_table,self.y)
        else:
            self.impurity = entropy(self.label_table,self.y)


"""
X,y = get_data()
data = dataset(X, y)
print(data.impurity)
"""


def info_gain(data_father, data1, data2):
    tot = len(data_father.X)
    res = data_father.impurity - (data1.impurity*len(data1.X) + data2.impurity*len(data2.X))/tot
    return res     



def average(X, nth_feature):
    sum_ = 0
    for x in X:
        sum_ += x[nth_feature]

    return sum_/len(X)



def split_average(data, average, nth_feature, impurity):
    X1, X2 = [], []
    y1, y2 = [], []

    for i in range(len(data.X)):
        if data.X[i][nth_feature] > average :
            X1.append(data.X[i])
            y1.append(data.y[i])
        else:
            X2.append(data.X[i])
            y2.append(data.y[i])
            
    data1 = dataset(X1, y1, impurity)
    data2 = dataset(X2, y2, impurity)
    return data1, data2


def split_average_light(X, y, average, nth_feature):
    X1, X2 = [], []
    y1, y2 = [], []

    for i in range(len(X)):
        if X[i][nth_feature] > average :
            X1.append(X[i])
            y1.append([i])
        else:
            X2.append(X[i])
            y2.append(y[i])
            
    return X1, y1, X2, y2


"""
def find_split(data, fn):
    my_data = data.copy()
    my_data.sort(key=lambda x: x[fn])
    print( entropy(data) - (entropy(data1) + entropy(data2)) / 2)
"""
