import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
from Apriori import Apriori
from Multihash import Multihash
from Multistage import Multistage
from PCY import PCY

"""
This is the main function that creates the graphs for each threshold, specifically 1%, 5%, and 10%. 
"""
def createGraph(thresholdPercentage):
    #These first three lines set the x-axs of the graph
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    xaxis = ['1%', '5%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
    plt.xticks(x, xaxis)
    #These next four lines represent the arrays in which the times for each of the algorithms will be stored
    aprioriTimes = []
    pcyTimes = []
    multistageTimes = []
    multihashTimes = []
    #The data chunks upon which the algorithms will be performed
    chunks = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    apriori = Apriori(thresholdPercentage, "retail.txt");
    pcy = PCY(thresholdPercentage, "retail.txt")
    multihash = Multihash(thresholdPercentage, "retail.txt")
    multistage = Multistage(thresholdPercentage, "retail.txt")
    #This for loop performs each algorithm on each data chunk and records the time required for each
    #of them in their respective lists
    for i in range(len(chunks)):
        start_time = time.time()
        apriori.runAlg(chunks[i])
        aprioriTimes.append((time.time() - start_time) * 1000)
        start_time = time.time()
        pcy.runAlg(chunks[i])
        pcyTimes.append((time.time() - start_time) * 1000)
        start_time = time.time()
        multistage.runAlg(chunks[i])
        multistageTimes.append((time.time() - start_time) * 1000)
        start_time = time.time()
        multihash.runAlg(chunks[i])
        multihashTimes.append((time.time() - start_time) * 1000)
    #The plotting of the times on the y-axis and the corresponding labels, after which the graph is created
    plt.plot(x, aprioriTimes, "-b", label="A-Priori", marker='o')
    plt.plot(x, pcyTimes, "-r", label="PCY", marker='o')
    plt.plot(x, multistageTimes, "-y", label="Multistage", marker='o')
    plt.plot(x, multihashTimes, "-g", label="Multihash", marker='o')
    plt.legend(loc="upper left")
    plt.title("Scalability Study for Support Threshold " + str(thresholdPercentage) + "%")
    plt.xlabel("Dataset Size")
    plt.ylabel("Run time (ms)")
    plt.show()

if __name__ == '__main__':
    createGraph(1)
    createGraph(5)
    createGraph(10)

