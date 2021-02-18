class Apriori:
    def __init__(self, thresholdPercentage, fileName):
        self.thresholdPercentage = thresholdPercentage
        self.file = open(fileName, "r")
    def runAlg(self, chunk):
        self.file.seek(0)
        self.dataChunk = (int)(88000 * (chunk / 100))
        self.threshold = (int)(self.dataChunk * (self.thresholdPercentage / 100))
        freqSingletons = self.findFreqSingletons()
        allPairs = {}
        for i in range(len(freqSingletons)):
            for j in range(i + 1, len(freqSingletons)):
                pair = str(freqSingletons[i]) + ',' + str(freqSingletons[j])
                allPairs[pair] = 0
        freqPairs = self.findFreqPairs(allPairs, freqSingletons)
        return freqPairs

    def findFreqSingletons(self):
        allNums = {}
        freqNums = []
        for i in range(self.dataChunk):
            line = self.file.readline()
            nums = list(map(int, line.split()))
            for num in nums:
                if num in allNums:
                    allNums[num] = allNums.get(num) + 1
                    if allNums.get(num) == self.threshold:
                        freqNums.append(num)
                else:
                    allNums[num] = 1
        return freqNums

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
                            pair = str(num1) + ',' + str(num2)
                            if pair in pairs:
                                pairs[pair] = pairs.get(pair) + 1
                            else:
                                pair = str(num2) + ',' + str(num1)
                                pairs[pair] = pairs.get(pair) + 1
                            if pairs[pair] == self.threshold:
                                freqPairs.append(pair)
        return freqPairs
