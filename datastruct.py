import utilities as ut

class DecisionData:
    def __init__(self):
        self.nth_feature = None
        self.split_val   = None
        self.majority_label = None 
        self.subX = None
        self.subY = None


    def clone(self):
        clone = DecisionData()
        clone.nth_feature = self.nth_feature 
        clone.split_val   = self.split_val
        clone.majority_label = self.majority_label 
        clone.subX = self.subX
        clone.subY = self.subY
        return clone

    def overwrite(target, source):
        target.nth_feature = source.nth_feature 
        target.split_val   = source.split_val
        target.majority_label = source.majority_label 
        target.subX = source.subX
        target.subY = source.subY

         
        


class Node:
    def __init__(self, father, majority_label = None):
        self.father = father
        self.lower = None
        self.greater = None
        self.decData = DecisionData()
        self.decData.majority_label = majority_label
       
    def set_sub(self,X, y):
        self.decData.subX = X
        self.decData.subY = y

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
            
    def sanity(self):
        self.is_sane()
        if self.is_leaf():
            if self.decData.majority_label == None:
                print(f"individuata foglia senza label, indice: {self.index}")
                raise Exception("Foglia senza label")
            else:
                self.greater.sanity()
                self.lower.sanity()
         
    def set_decision(self, nth, split):
        self.decData.nth_feature = nth
        self.decData.split_val = split


    def steal_parent(target, source):
        data = source.decData.clone()
        if source.father != None:
            if source == source.father.lower:
                source.father.lower = target
            else:
                source.father.greater = target
        target.decData.overwrite(data)
