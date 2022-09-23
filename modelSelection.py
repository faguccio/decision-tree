import decisionTree as lrn
import utilities as ut
import resource

if __name__ == "__main__":
    X,y = ut.get_data()
    trainX, trainY, valX, valY = ut.split_dataset(X, y, 0.7)
    valX, valY, testX, testY = ut.split_dataset(valX, valY, 0.5)


    models = {
            'entropy': lrn.Tree(),
            'gini': lrn.Tree(),
            'entropy, pruning': lrn.Tree() ,
            'gini, pruning': lrn.Tree(),
            }

    models['entropy'].learn(trainX, trainY)
    models['entropy, pruning'].learn(trainX, trainY, prune=True)
    models['gini'].learn(trainX, trainY, impurity_measure='gini')
    models['gini, pruning'].learn(trainX, trainY, impurity_measure='gini', prune=True)


    #print(f"model prun: with {models['entropy, pruning'].accuracy(valX, valY)}")
    #print(f"model: with {models['entropy'].accuracy(valX, valY)}")

    bestval = 0
    bestModel = None
    for k in models.keys():

        acc = models[k].accuracy(valX, valY)
        trainAcc = models[k].accuracy(trainX, trainY)
        print(f"{k} with {acc},   nodes -> {models[k].root.sub_tree_size()}")
        print(f"{k} with {trainAcc}")
        if acc > bestval:
            bestval = acc
            bestModel = k
    
    print(f"best model: {bestModel} with {bestval}")
    print(f"best model, test: {bestModel} with {models[bestModel].accuracy(testX, testY)}") 


    print(f"peak memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024} Mb")
    
