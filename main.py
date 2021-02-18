import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Apriori import Apriori
from Multihash import Multihash
from Multistage import Multistage
from PCY import PCY


def createGraph(thresholdPercentage):
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    xaxis = ['1%', '5%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
    plt.xticks(x, xaxis)
    aprioriTimes = []
    pcyTimes = []
    multistageTimes = []
    multihashTimes = []
    chunks = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    apriori = Apriori(thresholdPercentage, "retail.txt");
    pcy = PCY(thresholdPercentage, "retail.txt")
    multistage = Multistage(thresholdPercentage, "retail.txt")
    multihash = Multihash(thresholdPercentage, "retail.txt")
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
        print(aprioriTimes)
        print(pcyTimes)
        print(multistageTimes)
        print(multihashTimes)

    plt.plot(x, aprioriTimes, "-b", label="A-Priori", marker='o')
    plt.plot(x, pcyTimes, "-r", label="PCY", marker='o')
    plt.plot(x, multistageTimes, "-y", label="Multistage", marker='o')
    plt.plot(x, multihashTimes, "-g", label="Multihash", marker='o')
    plt.legend(loc="upper left")
    plt.title("Scalability Study for Support Threshold " + str(thresholdPercentage) + "%")
    plt.xlabel("Dataset Size")
    plt.ylabel("Run time (ms)")
    plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    createGraph(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
