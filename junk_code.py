
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

