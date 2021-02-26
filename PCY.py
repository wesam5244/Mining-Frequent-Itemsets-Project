from bitarray import bitarray
"""
This class performs the PCY algorithm 
"""


class PCY:
    #Constructor that takes in the threshold percentage and the name of the file
    def __init__(self, thresholdPercentage, fileName):
        self.thresholdPercentage = thresholdPercentage
        self.file = open(fileName, "r")

    #The hash function that will be used to create the buckets
    def hashFunction(self, i, j):
        code = (i+j) % 100000
        return code

    #Function that actually runs the algorithm
    def runAlg(self, chunk):
        self.file.seek(0)
        self.dataChunk = (int)(88162 * (chunk / 100))
        self.threshold = (int)(self.dataChunk * (self.thresholdPercentage / 100))
        bitVector, freqNums = self.passOne()
        self.file.seek(0)
        freqPairs = self.passTwo(freqNums, bitVector)
        return freqPairs

    #This function performs the first pass of the PCY algorithm
    def passOne(self):
        """
        For this pass, there are four main variables used. The first one, allNums, is a dictionary that stores each
        singleton as the key and its frequency as the value. The second variable, freqNums, is a simple list that
        stores all the frequent singletons. The third variable, buckets, is an array that represents the buckets that
        the pairs are hashed to. Each index in the list represents that specific bucket, ex. index 0 consists of the count
        of all the pairs that hashed to bucket 0. The fourth variable, bitVector, is the bit vector which will store
        0 or 1 at each index based on if that specific bucket is frequent or not
        :return:
        """
        allNums = {}
        freqNums = []
        buckets = [0] * 100000
        bitVector = bitarray(len(buckets))
        bitVector.setall(0)
        """
        Following the PCY algorithm, along with adding 1 to the frequency of each item in a basket, I also create all the 
        possible pairs from the items in that basket and hash them to the buckets 
        """
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
                    hashCode = self.hashFunction(num1, num2)
                    buckets[hashCode] += 1
                    #If the bucket has now become frequent, we sit the bit vectore at that index to be 1
                    if buckets[hashCode] == self.threshold:
                        bitVector[hashCode] = 1
        #In this case, we return the bit vector rather than the buckets as that will be used in the next pass in
        #order to save memory
        return bitVector, freqNums

    #This function performs the second pass of the PCY algorithm
    def passTwo(self, freqNums, bitVector):
        candidatePairs={}
        """
        Unlike A-Priori algorithm, PCY does not consider all possible pairs of the frequent singletons to be a candidate
        pair. In this for loop, we do create all the possible pairs from the frequent singletons, but we also only
        add those pairs as candidate pairs that satisfy the requirement of hashing to a value of 1 in the bit vector 
        """
        for i in range(len(freqNums)):
            for j in range(i+1, len(freqNums)):
                hashCode = self.hashFunction(freqNums[i], freqNums[j])
                if (bitVector[hashCode] == 1):
                    if freqNums[i] < freqNums[j]:
                        pair=str(freqNums[i]) + ',' + str(freqNums[j])
                    else:
                        pair=str(freqNums[j]) + ',' + str(freqNums[i])
                    candidatePairs[pair] = 0
        #Now, we find the frequency of all the candidate pairs, similar to A-Priori
        freqPairs=[]
        for i in range(self.dataChunk):
            line = self.file.readline()
            nums = list(map(int, line.split()))
            for x in range(len(nums)):
                num1 = nums[x]
                if num1 in freqNums:
                    for j in range(x+1, len(nums)):
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


