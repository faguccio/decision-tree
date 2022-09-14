import utilities as ut

data = ut.get_data()
nodiq = [0]


class tree:
    def __init__(self, nth, val, father=None, label=None):
        self.nth_feature = nth 
        self.split_val = val

        self.greater_child = None
        self.lower_child = None
        self.father = father
        self.label=label




def check_label(data):
    ref = data[0][-1]
    for x in data:
        if (x[-1] != ref):
            return False, None

    return True, ref


def check_feature(data, nth_feature):
    ref = data[0][nth_feature]
    for x in data[1:]:
        if x[nth_feature] != ref:
             return False
    
    return True


def learn(data, father):
    nodiq[0] += 1 
    

    if len(data) < 1:
        raise "GAIA TROIA"

    entropy_father = ut.entropy(data)
    best_info_gain = 0
    best_split = []
    split_val = 0
    index = -1

    check, label = check_label(data)
    if check:
        node = tree(0,0, father=father, label=label)
        return node

    for i in range(len(data[0])-1):
        if check_feature(data, i):
            continue

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


node = learn(data, None)
print(nodiq)
