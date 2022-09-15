import utilities as ut



class Node:
    amount = 0

    def __init__(self, father, label=None):
        self.index = Node.amount
        Node.amount += 1
        
        self.father = father
        self.label = label

        self.nth_feature = None
        self.split_val = None

        self.greater_child = None
        self.lower_child = None
        
    
    def set_decision(self, nth, split):
        self.nth_feature = nth
        self.split_val = split

    def set_children(self, greater, lower):
        self.greater_child = greater
        self.lower_child = lower

    def is_leaf(self):
        return self.greater_child == None

    def is_sane(self):
        if self.is_leaf():
            if self.lower_child != None:
                raise Exception("Foglia malata")

    def sanity(self):
        self.is_sane()
        if self.is_leaf():
            if self.label == None:
                print(self.index)
                raise Exception("Foglia senza label")

        else:
            if not (self.greater_child != None and self.lower_child != None):
                raise Exception("Node with missing child")
            
            self.greater_child.sanity()
            self.lower_child.sanity()

            

def check_feature(data, nth_feature):
    ref = data.X[0][nth_feature]
    for x in data.X[1:]:
        if x[nth_feature] != ref:
             return False
    
    return True




def choose_feature(data, impurity_measure):
    if len(data.X) < 2:
        raise Exception("FUCK MY ASS")

    best_info_gain = 0
    index = -1
    split_val = 0
    best_split = []
    for nth_feature in range(len(data.X[0])):
        average = ut.average(data.X, nth_feature)
        data1, data2 = ut.split_average(data, average, nth_feature, impurity_measure)

        info_gain = ut.info_gain(data, data1, data2)
        if abs(info_gain) > abs(best_info_gain):
            best_split = [data1, data2]
            best_info_gain = info_gain
            split_val = average
            index = nth_feature
            
    print("best info gain ")
    print (best_info_gain)
    #print("data1 length = " + str(len(data2.X)))
    #print("data2 length = " + str(len(data2.X)))
        
    return index, split_val, best_split


def larn(X, y, impurity_measure='entropy'):
    data = ut.dataset(X,y)
    return learn(data,impurity_measure)


def learn(data, impurity_measure, father=None):
    labels = list(data.label_table.keys())
    if len(labels) == 1:
        leaf = Node(father, label=labels[0])
        return leaf

    second_base_case = True
    for i in range(len(data.X[0])):
        if check_feature(data, i):
            continue
        else:
            second_base_case = False
            break

    if second_base_case:
        most_common = max(label_table, key=label_table.get)
        print(f"secoondo caso base {most_common}")
        leaf = Node(father, label=most_common) 
        return leaf
        
    
    index, split_val, best_split = choose_feature(data, impurity_measure)
    
    node = Node(father)
    node.set_decision(index, split_val)
    node.set_children(learn(best_split[0], node), learn(best_split[1], node))
    
    return node

def predict(x, node):
    if node.is_leaf():
        return node.label
    index    = node.nth_feature
    question = node.split_val
    if x[index] > question:
        node = node.greater_child
    else:
        node = node.lower_child
    return predict(x,node)
    

X,y = ut.get_data()
#data = ut.dataset(X, y)
#root = larn(X,y)
aline = X[-50]
data_gini = ut.dataset(X,y,'gini')
root = larn(X,y,'gini')
print(data_gini.y[-50])
print(predict(aline,root))
print(root.amount)
root.sanity()
