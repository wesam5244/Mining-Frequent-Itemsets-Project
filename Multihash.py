from bitarray import bitarray

class Multihash:
    def __init__(self, thresholdPercentage, fileName):
        self.thresholdPercentage = thresholdPercentage
        self.file = open(fileName, "r")

    def firstHashFunction(self, i, j):
        code = (i+j) % 5000
        return code

    def secondHashFunction(self, i, j):
        code = (i * j) % 5000
        return code

    def runAlg(self, chunk):
        self.file.seek(0)
        self.dataChunk = (int)(88000 * (chunk / 100))
        self.threshold = (int)(self.dataChunk * (self.thresholdPercentage / 100))
        firstBitVector, secondBitVector, freqNums = self.passOne()
        self.file.seek(0)
        freqPairs = self.passTwo(firstBitVector, secondBitVector, freqNums)
        return freqPairs

    def passOne(self):
        allNums = {}
        freqNums = []
        firstBuckets = [0] * 5000
        firstBitVector = bitarray(len(firstBuckets))
        firstBitVector.setall(0)
        secondBuckets = [0] * 5000
        secondBitVector = bitarray(len(secondBuckets))
        secondBitVector.setall(0)
        for i in range(self.dataChunk):
            line = self.file.readline()
            nums = list(map(int, line.split()))
            for i in range(len(nums)):
                num1 = nums[i]
                if num1 in allNums:
                    allNums[num1] = allNums.get(num1) + 1
                    if allNums.get(num1) == self.threshold:
                        freqNums.append(num1)
                else:
                    allNums[num1] = 1
                for j in range(i+1, len(nums)):
                    num2 = nums[j]
                    firstHashCode = self.firstHashFunction(num1, num2)
                    firstBuckets[firstHashCode] += 1
                    if firstBuckets[firstHashCode] == self.threshold:
                        firstBitVector[firstHashCode] = 1
                    secondHashCode = self.secondHashFunction(num1, num2)
                    secondBuckets[secondHashCode] += 1
                    if secondBuckets[secondHashCode] == self.threshold:
                        secondBitVector[secondHashCode] = 1
        return firstBitVector, secondBitVector, freqNums

    def passTwo(self, firstBitVector, secondBitVector, freqNums):
        candidatePairs={}
        for i in range(len(freqNums)):
            for j in range(i+1, len(freqNums)):
                num1 = freqNums[i]
                num2 = freqNums[j]
                firstHashCode = self.firstHashFunction(num1, num2)
                secondHashCode = self.secondHashFunction(num1, num2)
                if firstBitVector[firstHashCode] == 1 and secondBitVector[secondHashCode] == 1:
                    pair = str(num1) + ',' + str(num2)
                    candidatePairs[pair] = 0
        freqPairs=[]
        for i in range(self.dataChunk):
            line = self.file.readline()
            nums = list(map(int, line.split()))
            for x in range(len(nums)):
                num1 = nums[x]
                if num1 in freqNums:
                    for j in range(x + 1, len(nums)):
                        found = 0
                        num2 = nums[j]
                        if num2 in freqNums:
                            pair = str(num1) + ',' + str(num2)
                            if pair in candidatePairs:
                                candidatePairs[pair] = candidatePairs.get(pair) + 1
                                found = 1
                            else:
                                pair = str(num2) + ',' + str(num1)
                                if pair in candidatePairs:
                                    candidatePairs[pair] = candidatePairs.get(pair) + 1
                                    found = 1
                            if found == 1:
                                if candidatePairs[pair] == self.threshold:
                                    freqPairs.append(pair)
        return freqPairs


