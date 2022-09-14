import matplotlib.pyplot as plt

def get_data():
    with open('magic04.data') as file:
        lines = file.readlines()


        for i in range(len(lines)):
            line = lines[i].split(",")
            
            for j in range(len(line) -1):
                line[j] = float(line[j])

            line[-1] = line[-1][0]
            lines[i] = line
       
        return lines

data = get_data()

def wechoose8():
    ffg = []
    ffh = []

    n = 8

    for x in data:
        if (x[-1] == 'g'):
            ffg.append( x[n])
        else:
            ffh.append(x[n])


    #plt.subplot(211)
    #plt.plot(ffg)
    #plt.subplot(212)
    plt.hist(ffh, bins=40,  histtype="step", color='black')
    plt.hist(ffg, bins=40,  histtype="step", color='green')
    plt.show()


import math

"""
for x in data:
    if x[-1] == 'g':
        gcount +=1
    else:
        hcount += 1
                      
entropy = - (gcount/len(data) * math.log(gcount/len(data), 2) + hcount/len(data) * math.log(hcount/len(data), 2) )
"""


def entropy(data):
    gcount = 0
    hcount = 0

    for x in data:
        if x[-1] == 'g':
            gcount +=1
        else:
            hcount += 1
    
    if gcount < 1 or hcount < 1:
        return 0

    entropy = - (gcount/len(data) * math.log(gcount/len(data), 2) + hcount/len(data) * math.log(hcount/len(data), 2) )

    return entropy


#sort(key=get_first)
'''
for feature_n in range(10):
    summen = 0
    for x in data:
        summen += x[feature_n]

    average = summen / len(data)

    greater = 0
    greater_g = 0
    greater_h = 0

    for x in data:
        if x[feature_n] > average :
            greater +=1
            
            if x[-1] == 'g':
                greater_g += 1
            else:
                greater_h += 1




    entropy =  - (greater_g/len(data) * math.log(greater_g/len(data), 2) + greater_h/len(data) * math.log(greater_h/len(data), 2) )

    print(entropy)
'''

def average(data, nth_feature):
    sum_ = 0
    for x in data:
        sum_ += x[nth_feature]

    return sum_/len(data)



def split_average(data, average, nth_feature):
    data1 = []
    data2 = []

    for x in data:
        if x[nth_feature] > average :
            data1.append(x)
        else:
            data2.append(x)
    
    return data1, data2




def find_split(data, fn):
    my_data = data.copy()
    my_data.sort(key=lambda x: x[fn])
    

    


    print( entropy(data) - (entropy(data1) + entropy(data2)) / 2)

