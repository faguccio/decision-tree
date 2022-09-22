from sklearn import tree
import numpy as np
import learning as lrn


decTree = tree.DecisionTreeClassifier()  # default criterion is gini
decTree = decTree.fit(X,y)  #trains the tree
x = np.array([49.5, 36.2, 100.0, 34.0, 87.0, 42.0, 47.5, 79.2, 50.0, 180.0])
pred = decTree.predict(x)
print(f""pred)


myDecTree = lrn.learn(X, y, 'gini', prune = False)










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
