from bitarray import bitarray

class Multistage:
    def __init__(self, thresholdPercentage, fileName):
        self.thresholdPercentage = thresholdPercentage
        self.file = open(fileName, "r")

    def firstHashFunction(self, i, j):
        code = (i + j) % 10000
        return code
    def secondHashFunction(self, i, j):
        code = (i * j) % 1000
        return code

    def runAlg(self, chunk):
        self.file.seek(0)
        self.dataChunk = (int)(88000 * (chunk / 100))
        self.threshold = (int)(self.dataChunk * (self.thresholdPercentage / 100))
        firstPassBitVector, freqNums = self.passOne()
        self.file.seek(0)
        secondBitVector = self.passTwo(freqNums, firstPassBitVector)
        self.file.seek(0)
        freqPairs = self.passThree(freqNums, firstPassBitVector, secondBitVector)
        return freqPairs

    def passOne(self):
        allNums = {}
        freqNums = []
        buckets = [0] * 10000
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

    def passTwo(self, freqNums, bitVecor):
        buckets = [0] * 1000
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

    def passThree(self, freqNums, firstBitVector, secondBitVector):
        candidatePairs = {}
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
