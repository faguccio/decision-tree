import learning as lrn
import utilities as ut
import resource

if __name__ == "__main__":
    X,y = ut.get_data()
    trainX, trainY, valX, valY = ut.split_dataset(X, y, 0.7)
    valX, valY, testX, testY = ut.split_dataset(valX, valY, 0.5)

    decTreeGini = lrn.Tree()
    decTreeEnt = lrn.Tree()
    decTreeGini.learn(trainX, trainY, impurity_measure='gini', prune=True)
    decTreeEnt.learn(trainX, trainY, prune=True)
    decTreeGiniHair = lrn.Tree()
    decTreeEntHair = lrn.Tree()
    decTreeGiniHair.learn(trainX, trainY, impurity_measure='gini')
    decTreeEntHair.learn(trainX, trainY)
    

    print(f"accuracy on train data (entropy): {decTreeEntHair.accuracy(trainX, trainY)}")
    print(f"accuracy on train data (gini): {decTreeGiniHair.accuracy(trainX, trainY)}")
    print(f"accuracy on train data (entropy, pruning): {decTreeEnt.accuracy(trainX, trainY)}")
    print(f"accuracy on train data (gini, pruning): {decTreeGini.accuracy(trainX, trainY)}")


    print(f"accuracy on val data (entropy): {decTreeEntHair.accuracy(valX, valY)}")
    print(f"number of nodes: {decTreeEntHair.root.sub_tree_size()}")
    print(f"accuracy on val data (gini): {decTreeGiniHair.accuracy(valX, valY)}")
    print(f"number of nodes: {decTreeGiniHair.root.sub_tree_size()}")
    print(f"accuracy on val data (entropy, pruning): {decTreeEnt.accuracy(valX, valY)}")
    print(f"number of nodes: {decTreeEnt.root.sub_tree_size()}")
    print(f"accuracy on val data (gini, pruning): {decTreeGini.accuracy(valX, valY)}")
    print(f"number of nodes: {decTreeGini.root.sub_tree_size()}")


    


    print(f"peak memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024} Mb")
    

