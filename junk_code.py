from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import learning as lrn
import utilities as ut
import matplotlib.pyplot as plt



X,y = ut.get_data()
trainX, testX, trainY, testY = train_test_split(X,y, test_size = 0.20)
val_x, test_x, val_y, test_y = train_test_split(testX,testY, test_size = 0.40)

decTree     = tree.DecisionTreeClassifier()  # default criterion is gini
decTree     = decTree.fit(trainX,trainY)  #trains the tree
pred        = decTree.predict(val_x)
val_score1   = accuracy_score(val_y, pred)
print(f"validation accuracy score with gini {val_score1}")

decTree2     = tree.DecisionTreeClassifier(criterion = "entropy")
decTree2     = decTree2.fit(trainX,trainY)  #trains the tree
predictions2 = decTree.predict(val_x)
val_score2   = accuracy_score(val_y, predictions2)
print(f"validation accuracy score with entropy {val_score2}")


pred_test1   = decTree.predict(test_x)
test_score1  = accuracy_score(test_y, pred_test1)
print(f"test accuracy score with gini {test_score1}")
pred_test2   = decTree.predict(test_x)
test_score2  = accuracy_score(test_y, pred_test2)
print(f"test accuracy score with entropy {test_score2}")


#since sklearn prunes with cost complexity pruning, which is very time consuming and much more






"""
myDecTree = lrn.learn(X, y, 'gini', prune = False)
pred = myDecTree.predict(x)
print(f"prediction2 {pred}")
"""









"""
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

"""
