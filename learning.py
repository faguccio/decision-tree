import utilities as ut
import time
import numpy as np
from datastruct import Node, DecisionData
import resource



class Tree:
    def __init__(self):
        self.root  = None
        self.acc_before = None
        
    def check_feature(self, data, nth_feature):
        ref = data.X[0][nth_feature]
        for x in data.X[1:]:
            if x[nth_feature] != ref:
                return False
        return True


    def choose_feature(self, data, impurity_measure):
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


 

    def train(self, data, impurity_measure, prune = False, father=None):
        labels = list(data.label_table.keys())
        most_common = max(data.label_table, key=data.label_table.get)
        if len(labels) == 1:
            leaf = Node(father, majority_label=labels[0])
            return leaf
        second_base_case = True
        for i in range(len(data.X[0])):
            if self.check_feature(data, i):
                continue
            else:
                second_base_case = False
                break
        if second_base_case:
            print(f"secondo caso base {most_common}")
            leaf = Node(father, label=most_common)
            return leaf

        index, split_val, best_split = self.choose_feature(data, impurity_measure)
        node = Node(father, most_common)
        node.set_decision(index, split_val)
        node.greater = self.train(best_split[0], impurity_measure, node)
        node.lower = self.train(best_split[1], impurity_measure, node)
        node.majority_label = (most_common)
        
        return node


    
    def distribute_data(self, node, X, y):
        node.set_sub(X, y)
        if node.is_leaf():
            return
        X1, y1, X2, y2 = ut.split_average_light(X, y, node.decData.split_val, node.decData.nth_feature)
        self.distribute_data(node.lower, X1, y1)
        self.distribute_data(node.greater, X2, y2)



    def predict(self, x, node=None):
        if node == None:
            node = self.root
        while not node.is_leaf():
            index = node.decData.nth_feature
            question = node.decData.split_val
            if x[index] > question:
                node = node.greater
            else:
                node = node.lower
        if node.is_leaf():
            return node.decData.majority_label
        else:
            raise "Foglia non foglai"



    def fastAccuracy(self, node):
        good_predicitons = 0
        if (len(node.decData.subX) == 0):
            return 1
        for i in range(len(node.decData.subX)):
            res = self.predict(node.decData.subX[i], node=node)
            if res == node.decData.subY[i]:
                good_predicitons += 1
         
        accuracy = good_predicitons/len(node.decData.subX)
        return accuracy
    
    def accuracy(self, X, y):
        good_predicitons = 0
        for i in range(len(X)):
            res = self.predict(X[i])
            if res == y[i]:
                good_predicitons += 1
    
        accuracy = good_predicitons/len(X)
        return accuracy
    
  
    def prune(self, node, pruneX, pruneY):
        assert(not node.is_leaf())
        if self.acc_before == None:
            self.acc_before = self.accuracy(pruneX, pruneY)
        label = node.majority_label
        leaf = Node(node.father, label)
        Node.steal_parent(leaf, node)
        acc_after = self.accuracy(pruneX, pruneY)
        if acc_after < self.acc_before:
            Node.steal_parent(node, leaf)


    def fastPrune(self, node):
        acc_before = self.fastAccuracy(node)
        label = node.majority_label
        leaf = Node(node.father, label)
        Node.steal_parent(leaf, node)
        acc_after = self.fastAccuracy(node)
        if acc_after < acc_before:
            Node.steal_parent(node, leaf)




    def prune_all_subtree(self, node, pruneX, pruneY):
        if node.is_leaf():
            return
        self.prune_all_subtree(node.greater, pruneX, pruneY)
        self.prune_all_subtree(node.lower, pruneX, pruneY)
        self.prune(node, pruneX, pruneY)
    
    def prune_all_fast(self, node):
        if node.is_leaf():
            return
        self.prune_all_fast(node.greater)
        self.prune_all_fast(node.lower)
        self.fastPrune(node)


    def learn(self, X, y, impurity_measure='entropy', prune = False):
        if prune:
            trainX, trainY, pruneX, pruneY = ut.split_dataset(X,y, percent=0.9)
            data = ut.dataset(trainX, trainY)
            self.root = self.train(data, impurity_measure, prune)
            seconds = time.time()
            #self.prune_all_subtree(self.root, pruneX, pruneY)
            self.distribute_data(self.root, pruneX, pruneY)
            self.prune_all_fast(self.root)
            print(f"pruning time {time.time() - seconds}")
        else:
            data = ut.dataset(X, y)
            self.root = self.train(data, impurity_measure, prune)
     


#fine classe tree
       




if __name__ == "__main__":
    X,y = ut.get_data()
    
    trainX, trainY, pruneX, pruneY = ut.split_dataset(X,y, percent=0.8)
    decTree = Tree()
    decTree.learn(X, y, impurity_measure='gini', prune=True)
    
    print(decTree.root.sub_tree_size())
    decTree.root.sanity()
    print(f"accuracy on training data: {decTree.accuracy(trainX, trainY)}")
    print(f"accuracy on pruning data: {decTree.accuracy(pruneX, pruneY)}")
    
    decTree.distribute_data(decTree.root, pruneX, pruneY)
    #print(f"memory: {process.memory_info().rss / (1024*1024)} Mb")
    print(f"memory: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024} Mb")
    
