"""
This class performs the A-Priori algorithm
"""
class Apriori:
    #Constructor that takes the threshold percentage, ex. 1, 5, or 10, and the name of the file
    def __init__(self, thresholdPercentage, fileName):
        self.thresholdPercentage = thresholdPercentage
        self.file = open(fileName, "r")
    #Actually runs the algorithm itself
    def runAlg(self, chunk):
        #Need to set the file seek to 0 because the algorithm will be run several times on the same file, so
        #every time it needs to be rewinded to the beginning
        self.file.seek(0)
        #Calculate the number of lines to be read, the actual threshold in number of baskets
        self.dataChunk = (int)(88162 * (chunk / 100))
        self.threshold = (int)(self.dataChunk * (self.thresholdPercentage / 100))
        #Call the function that will find the frequent singletons, i.e. the first pass
        freqSingletons = self.findFreqSingletons()
        #First, we generate all the possible pairs of the frequent singletons, and then pass those in the
        #function that finds the frequent pairs from all those possible pairs
        allPairs = {}
        for i in range(len(freqSingletons)):
            for j in range(i + 1, len(freqSingletons)):
                if freqSingletons[i] < freqSingletons[j]:
                    pair = str(freqSingletons[i]) + ',' + str(freqSingletons[j])
                else:
                    pair = str(freqSingletons[j]) + ',' + str(freqSingletons[i])
                allPairs[pair] = 0
        freqPairs = self.findFreqPairs(allPairs, freqSingletons)
        return freqPairs

    #This function finds the frequent singletons in the file based on the threshold and datachunk
    def findFreqSingletons(self):
        """
        I make use of a dictionary that contains all the singletons in the file as keys with the values
        being the count for each of those numbers/keys. The second array, called freqNums, simply stores
        all the frequent singletons
        """
        allNums = {}
        freqNums = []
        for i in range(self.dataChunk):
            line = self.file.readline()
            nums = list(map(int, line.split()))
            for num in nums:
                if num in allNums:
                    allNums[num] = allNums.get(num) + 1
                    #If the adding of one to this number's value makes it reach its threshold,
                    #then it is now a frequent singleton
                    if allNums.get(num) == self.threshold:
                        freqNums.append(num)
                else:
                    allNums[num] = 1
        return freqNums

    """
    This function finds the frequent pairs from a list of all the possible pairs of frequent numbers.
    It goes through the file line by line and searches to see if there is a pair of frequent items 
    in the line, and then incrementing the key that corresponds to that pair 
    """
    def findFreqPairs(self, pairs, freqNums):
        self.file.seek(0)
        freqPairs = []
        for i in range(self.dataChunk):
            line = self.file.readline()
            nums = list(map(int, line.split()))
            for x in range(len(nums)):
                num1 = nums[x]
                if num1 in freqNums:
                    for j in range(x+1, len(nums)):
                        num2 = nums[j]
                        if num2 in freqNums:
                            #This if else statement
                            if num1 < num2:
                                pair = str(num1) + ',' + str(num2)
                            else:
                                pair = str(num2) + ',' + str(num1)
                            if pair in pairs:
                                pairs[pair] = pairs.get(pair) + 1
                                if pairs[pair] == self.threshold:
                                    freqPairs.append(pair)
        return freqPairs
