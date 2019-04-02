#------------------------------------------------------------------
# Author: Julian Sullivan
# Purpose: Various functions for decision trees not unique to a class
#------------------------------------------------------------------

# Given a decision tree and a column index, calculate the weighted entropy of the column
def EntropyColumn(self, aAttributeIndex):
    uniqueElements = self.PossibleValues[aAttributeIndex]

    if len(uniqueElements) == 0: return 0.0

    total = len(aData) - 1
    entropy = 0.0
    
    for ele in uniqueElements:
        trues, falses, count = Counts(aData, ele, aAttributeIndex)
        entropy += (count / total) * Entropy(trues, falses, count)

    return entropy

# Returns the number of trues, falses and totals for a given value in a given column 
def Counts(aData, aElement, aAttributeIndex):
    count = 0
    trues = 0
    for data in aData:
        if data[aAttributeIndex] == ele:  count += 1
        if data[len(aData) - 1] == "Yes": trues += 1
    return trues, count - trues, count

def ParentValues(aData):
    trues = 0
    for data in aData:
        if data[len(aData) - 1] == "Yes" or data[len(aData) - 1] == 1: trues += 1
    return trues, (len(aData) - 1) - trues, (len(aData) - 1)

# Returns the information gain of a particular column
def InformationGain(aData, aAttributeIndex, aParentEntropy):
    return aParentEntropy - EntropyColumn(aData, aAttributeIndex)

# Returns the index of the column with the best information gain
def GetBestInformationGain(aData):
    bestInfoGain = -1.0
    bestAttributeIndex = -1

    trues, falses, total = ParentValues(aData)
    parentEntropy = Entropy(trues, falses, total)

    for index in len(aData[0]):
        ig = InformationGain(aData, index, parentEntropy)
        if ig > bestInfoGain:
             bestInfoGain = ig
             bestAttributeIndex = index
