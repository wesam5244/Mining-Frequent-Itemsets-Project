from bitarray import bitarray

"""
This class performs the Multi stage algorithm 
"""

class Multistage:
    def __init__(self, thresholdPercentage, fileName):
        self.thresholdPercentage = thresholdPercentage
        self.file = open(fileName, "r")

    #The two hash functions that will be used
    def firstHashFunction(self, i, j):
        code = (i + j) % 100000
        return code
    def secondHashFunction(self, i, j):
        code = (i * j) % 10000
        return code

    def runAlg(self, chunk):
        self.file.seek(0)
        self.dataChunk = (int)(88162 * (chunk / 100))
        self.threshold = (int)(self.dataChunk * (self.thresholdPercentage / 100))
        firstPassBitVector, freqNums = self.passOne()
        self.file.seek(0)
        secondBitVector = self.passTwo(freqNums, firstPassBitVector)
        self.file.seek(0)
        freqPairs = self.passThree(freqNums, firstPassBitVector, secondBitVector)
        return freqPairs

    #This function performs the first pass of this algorithm which is the same as that of PCY
    def passOne(self):
        allNums = {}
        freqNums = []
        buckets = [0] * 100000
        bitVector = bitarray(len(buckets))
        bitVector.setall(0)
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
                    hashCode = self.firstHashFunction(num1, num2)
                    buckets[hashCode] += 1
                    if buckets[hashCode] == self.threshold:
                        bitVector[hashCode] = 1
        return bitVector, freqNums

    #This function performs the second pass of this algorithm
    def passTwo(self, freqNums, bitVecor):
        """
        With this pass, the file is read again, and with each item in the basket, a pair is created only if the
        current item is frequent, and the second number in the value is hashed to the bucket and bit vector only if
        it is also frequent and the pair as a whole hashes to a value of 1 in the bit vector from the previous pass
        """
        buckets = [0] * 10000
        secondBitVector = bitarray(len(buckets))
        secondBitVector.setall(0)
        for i in range(self.dataChunk):
            line = self.file.readline()
            nums = list(map(int, line.split()))
            for x in range(len(nums)):
                num1 = nums[x]
                if num1 in freqNums:
                    for j in range(x+1, len(nums)):
                        num2 = nums[j]
                        if num2 in freqNums and bitVecor[self.firstHashFunction(num1, num2)] == 1:
                            secondHashCode = self.secondHashFunction(num1, num2)
                            buckets[secondHashCode] += 1
                            if buckets[secondHashCode] == self.threshold:
                                secondBitVector[secondHashCode] = 1
        return secondBitVector

    #This functions performs the third pass of the algorithm
    def passThree(self, freqNums, firstBitVector, secondBitVector):
        candidatePairs = {}
        """
        Over here, all possible pairs are taken of the frequent singletons, but in this case only those 
        are considered candidate pairs if they hash to a value of 1 in both bit vectors 
        """
        for i in range(len(freqNums)):
            for j in range(i + 1, len(freqNums)):
                firstHashCode = self.firstHashFunction(freqNums[i], freqNums[j])
                secondHashCode = self.secondHashFunction(freqNums[i], freqNums[j])
                if firstBitVector[firstHashCode] == 1 and secondBitVector[secondHashCode] == 1:
                    pair = str(freqNums[i]) + ',' + str(freqNums[j])
                    candidatePairs[pair] = 0
        freqPairs = []
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
                            if num1 < num2:
                                pair = str(num1) + ',' + str(num2)
                            else:
                                pair = str(num2) + ',' + str(num1)
                            if pair in candidatePairs:
                                candidatePairs[pair] = candidatePairs.get(pair) + 1
                                if candidatePairs[pair] == self.threshold:
                                    freqPairs.append(pair)
        return freqPairs
