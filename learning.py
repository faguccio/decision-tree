import utilities as ut






class Node:
    amount = 0

    def __init__(self, father, label=None):
        amount += 1
        
        self.father = father
        self.label = label

        self.nth_feature = None
        self.split_val = None

        self.greater_child = None
        self.lower_child = None
        
    
    
    def set_decision(nth, split):
        self.nth_feature = nth
        self.split_val = split


    def set_children(greater, lower):
        self.greater_child = greater
        self.lower_child = lower

    def is_leaf():
        return self.greater_child == None

    def sanity():
        if is_leaf():
            if self.label == None:
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





X,y = ut.get_data()
data = dataset(X, y)
print(data.entropy)

root = Node()


def choose_feature():
    pass


def larn(X, y, impurity_measure='entropy'):
    return 0


def learn(data, father=None):
   
    labels = data.label_table.keys()
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
        print(most_common)
        leaf = Node(father, label=most_common) 
        return leaf 


    for njasnvoi:
        average = ut.average(data, i)
        data1, data2 = ut.split_average(data, average, i)

        if len(data1) < 1 or len(data2) < 1:
            print(len(data1), len(data2))
            print(data2)
            print(data1)
            raise "GAIA TROIA infame"


        info_gain = entropy_father - (ut.entropy(data1) + ut.entropy(data2))/2
       
        if info_gain > best_info_gain:
            best_split = [data1, data2]
            best_info_gain = info_gain
            split_val = average
            index = i

    
    node = tree(i, split_val, father)
    node.greater_child = data1
    node.lower_child = data2
    print(entropy_father, best_info_gain)

    learn(data1, node)
    learn(data2, node)
    return node




learn(data.X, data.y)
print(root.amount)