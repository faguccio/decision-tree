import math


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




def entropy(label_table):
    entropy = 0
    for label_count in label_table.values():
        entropy -= (label_count/len(y) * math.log(label_count/len(y), 2) )

    return entropy


def compute_occurencies(y):
        label_table = {}

        for label in y:
            if  label in label_table.keys():
                label_table[label] += 1
            else:
                label_table[label] = 1
       
        return label_table


class dataset:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.label_table = compute_occurencies(y)
        self.entropy = entropy(self.label_table)

    def add(self, x, label):
        self.X.append(x)
        self.y.append(label)


X,y = get_data()
data = dataset(X, y)
print(data.entropy)



def info_gain(data_father, data1, data2):
    tot = len(data_father)
    res = data_fathar.entropy - (data1.entropy*len(data1.X) + data2.entropy*len(data2.X))/tot
    return res     



def average(X, nth_feature):
    sum_ = 0
    for x in X:
        sum_ += x[nth_feature]

    return sum_/len(X)



def split_average(data, average, nth_feature):
    data1 = dataset([], [])
    data2 = dataset([], [])


    for i in range(len(data.X)):
        if data.X[i][nth_feature] > average :
            data1.add(data.X[i], data.y[i])
        else:
            data2.add(data.X[i], data.y[i])
    
    return data1, data2




def find_split(data, fn):
    my_data = data.copy()
    my_data.sort(key=lambda x: x[fn])
    print( entropy(data) - (entropy(data1) + entropy(data2)) / 2)

