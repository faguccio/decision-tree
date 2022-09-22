import utilities as ut
import numpy as np



class Tree:
    def __init__(self, node = None):
        self.root  = node
        self.count = 1
        
    def add_node(self):
        self.count += 1
        
    def check_feature(self, data, nth_feature):
        ref = data.X[0][nth_feature]
        for x in data.X[1:]:
            if x[nth_feature] != ref:
                return False
        return True



    def choose_feature(self, data, impurity_measure):
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


    def learn(self, X, y, impurity_measure='entropy', prune = False):  #potremmo mettere learn e train e prune dentro a tree, come metodi di tree
    #trainset_X, trainset_Y, test_X, test_Y = split_dataset(X,y, percent=0.8)
        if prune:
            trainX, trainY, pruneX, pruneY = split_dataset(X,y, percent=0.8)
            data = ut.dataset(trainX,trainY)
            tree = Tree()
            root = Tree.train(data, impurity_measure, prune)
            tree.root = root
            Tree.prune_all_subtree(self.root, self.root, pruneX, pruneY)
        else:
            data = ut.dataset(X, y)
            tree = Tree()
            root = Tree.train(data, impurity_measure, prune)
            tree.root = root
        return tree #test_X, test_Y
 

    def train(self, data, impurity_measure, prune = False, father=None):
        labels = list(data.label_table.keys())
        most_common = max(data.label_table, key=data.label_table.get)
        if len(labels) == 1:
            leaf = Node(father, majority_label=labels[0])
            return leaf
        second_base_case = True
        for i in range(len(data.X[0])):
            if Tree.check_feature(data, i):
                continue
            else:
                second_base_case = False
                break
        if second_base_case:
            print(f"secondo caso base {most_common}")
            leaf = Node(father, label=most_common)
            return leaf
        index, split_val, best_split = Tree.choose_feature(data, impurity_measure)
        node = Node(father, most_common)
        node.set_decision(index, split_val)
        node.greater = Tree.train(best_split[0], impurity_measure, node)
        Tree.add_node()
        node.lower = Tree.train(best_split[1], impurity_measure, node)
        Tree.add_node()
        node.majority_label = (most_common)
        return node


    def predict(self, x):
        node = self.root
        while not node.is_leaf():
            index    = node.nth_feature
            question = node.split_val
            if x[index] > question:
                node = node.greater
            else:
                node = node.lower
        if node.is_leaf():
            return node.majority_label
            
    """if node.is_leaf():
        return node.label
    index    = node.nth_feature
    question = node.split_val
    if x[index] > question:
        node = node.greater
    else:
        node = node.lower
    return predict(x,node)
"""
 
 
 
    def accuracy(self, node, X, y):
        good_predicitons = 0
        for i in range(len(X)):
            res = predict(X[i])
            if res == y[i]:
                good_predicitons += 1
    
        accuracy = good_predicitons/len(X)
        return accuracy
    
  
    def prune(self, node, pruneX, pruneY):
        assert(not node.is_leaf())
    
        label = node.majority_label
        acc_before = accuracy(node, pruneX, pruneY)
    
        leaf = Node(node.father, label)
    
        acc_after = accuracy(leaf, pruneX, pruneY)
        if acc_after >= acc_before:# and acc_before != 0:
        #print(f"{acc_after/acc_before}   {node.index}")
            node.substitute(leaf)


    def prune_all_subtree(self, node, pruneX, pruneY):
        if node.is_leaf():
            return
        prune_all_subtree(node.greater, pruneX, pruneY)
        prune_all_subtree(node.lower, pruneX, pruneY)
        prune(node, pruneX, pruneY)

#fine classe tree



class Node:
    amount = 0

    def __init__(self, father, majority_label = None, nth_feature = None, split_val = None):
        self.index = Node.amount
        Node.amount += 1
        self.father = father
        self.lower = None
        self.greater = None
            
        #self.label  = label # label e majority label possono essere la stessa cosa
        self.nth_feature = None
        self.split_val   = None
        self.majority_label = majority_label
            
            
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
        




if __name__ == "__main__":
    X,y = ut.get_data()
    
    data_train = ut.dataset(X, y, 'entropy')
    tree = Tree.learn(X, y, 'entropy', prune = False)#ERRORE!! quando faccio prune = false i get a tree con 7265 nodi, altrimenti prune= true mi fa un albero di 8677 nodi
    print(tree.count)
    
    print(tree.root.sub_tree_size())
    tree.root.sanity()
    print(f"accuracy on training data: {accuracy(tree.root, trainX, trainY)}")
    print(f"accuracy on pruning data: {accuracy(tree.root, pruneX, pruneY)}")

    import os, psutil
    process = psutil.Process(os.getpid())
    print(process.memory_info().rss / (1024*1024))  # in bytes
