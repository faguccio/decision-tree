import utilities as ut
import random
import numpy as np

random.seed(123)


class Node:
    amount = 0

    def __init__(self, father):
        self.index = Node.amount
        Node.amount += 1
        self.father = father
        self.lower = None
        self.greater = None

    def is_leaf(self):
        return self.lower == None and self.greater == None

    def is_sane(self):
        if ut.xor ((self.lower == None), (self.greater == None)):
            print(f"Individuato nodo non sano, indice {self.index}")
            raise Exception("Nodo non sano!}")
   
    def sub_tree_size(self): 
        if self.is_leaf():
            return 1
        return self.lower.sub_tree_size() + self.greater.sub_tree_size()
    


class decNode(Node):

    def __init__(self, father, label=None):
        super().__init__(father)
        self.label  = label
        self.nth_feature = None
        self.split_val   = None
        self.majority_label = None
        
    def set_decision(self, nth, split):
        self.nth_feature = nth
        self.split_val = split

    def sanity(self):
        self.is_sane()
        if self.is_leaf():
            if self.label == None:
                print(f"individuata foglia senza label, indice: {self.index}")
                raise Exception("Foglia senza label")
            
        else:
            self.greater.sanity()
            self.lower.sanity()

    def substitute(self, target):
        self.father = target.father
        # Delete children by erasing references
        self.lower.father = None
        self.greater.father = None
        self.lower = target.lower
        self.greater = target.greater
        
        self.majority_label = target.majority_label
        self.nth_feature = target.nth_feature
        self.split_val   = target.split_val
        self.label = target.label
        



def check_feature(data, nth_feature):
    ref = data.X[0][nth_feature]
    for x in data.X[1:]:
        if x[nth_feature] != ref:
             return False
    return True



def choose_feature(data, impurity_measure):
    if len(data.X) < 2:
        raise Exception("FUCK MY ASS")

    best_info_gain = None
    index = -1
    split_val = 0
    best_split = []
    for nth_feature in range(len(data.X[0])):
        average = ut.average(data.X, nth_feature)
        data1, data2 = ut.split_average(data, average, nth_feature, impurity_measure)
        info_gain = ut.info_gain(data, data1, data2)
        if best_info_gain == None or info_gain > best_info_gain:
            best_split = [data1, data2]
            best_info_gain = info_gain
            split_val = average
            index = nth_feature
   
    return index, split_val, best_split


def learn(X, y, impurity_measure='entropy', prune = False):
    if prune:
        trainX, trainY, pruneX, pruneY = split_prune(X,y, percent=0.8)
        data = ut.dataset(trainX,trainY)
        root = train(data, impurity_measure, prune)
        prune_all_subtree(root, root, pruneX, pruneY)
    else:    
        data = ut.dataset(X,y)
        root = train(data, impurity_measure, prune)
    return root
 

def train(data, impurity_measure, prune = False, father=None):
    labels = list(data.label_table.keys())
    most_common = max(data.label_table, key=data.label_table.get)
    if len(labels) == 1:
        leaf = decNode(father, label=labels[0])
        return leaf
    second_base_case = True
    for i in range(len(data.X[0])):
        if check_feature(data, i):
            continue
        else:
            second_base_case = False
            break
    if second_base_case:
        print(f"secoondo caso base {most_common}")
        leaf = decNode(father, label=most_common) 
        return leaf
    index, split_val, best_split = choose_feature(data, impurity_measure)
    node = decNode(father)
    node.set_decision(index, split_val)
    node.greater = train(best_split[0], node)
    node.lower = train(best_split[1], node)
    node.majority_label = (most_common)
    return node



def predict(x, node):
    if node.is_leaf():
        return node.label
    index    = node.nth_feature
    question = node.split_val
    if x[index] > question:
        node = node.greater
    else:
        node = node.lower
    return predict(x,node)



def split_prune(X,y, percent=0.8):
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
 
 
 
def accuracy(node, X, y):
    
    good_predicitons = 0
    for i in range(len(X)):     
        res = predict(X[i], node)
        if res == y[i]:
            good_predicitons += 1
    
    accuracy = good_predicitons/len(X)
    return accuracy
    
  
def prune(node, root,pruneX, pruneY):
    assert(not node.is_leaf())
    
    label = node.majority_label
    acc_before = accuracy(root, pruneX, pruneY)  
    leaf = decNode(node.father, label)

    acc_after = accuracy(leaf, pruneX, pruneY)
    if acc_after >= acc_before:# and acc_before != 0:   
        #print(f"{acc_after/acc_before}   {node.index}")
        node.substitute(leaf)


def prune_all_subtree(node, root, pruneX, pruneY):
    if node.is_leaf():
        return
    prune_all_subtree(node.greater, root, pruneX, pruneY)
    prune_all_subtree(node.lower, root, pruneX, pruneY)
    prune(node, root, pruneX, pruneY)


if __name__ == "__main__":
    X,y = ut.get_data()

    trainX, trainY, pruneX, pruneY = split_prune(X, y)

    data_train = ut.dataset(X, y, 'gini')
    root = learn(X, y, 'gini', prune=True)

    print(root.sub_tree_size())
    root.sanity()
    print(f"accuracy on training data: {accuracy(root, trainX, trainY)}")
    print(f"accuracy on pruning data: {accuracy(root, pruneX, pruneY)}")

    import os, psutil
    process = psutil.Process(os.getpid())
    print(process.memory_info().rss / (1024*1024))  # in bytes
