#------------------------------------------------------------------
# Author: Julian Sullivan
# Purpose: Various functions for decision trees not unique to a class
#------------------------------------------------------------------

def IsNumeric(aValue):
    return isinstance(aValue, int) or isinstance(aValue, float)

# Given the number of trues, falses and total rows, return entropy
def Entropy(Trues, Falses, Total):
    return - ((Trues/Total) * log(Trues/Total, 2) + (Falses/Total) * log(Falses/Total, 2))

# Given a data set and a column index, return a list of unique elements
def UniqueElements(aData, aAttributeIndex):
    retSet = set()
    for data in aData:
        retSet.add(aData[aAttributeIndex])
    return retSet

def UniqueElementsNumeric(aData, aAttributeIndex):
    retSet = set()
    sortedValues = []

    for data in aData:
        sortedValues.append(data[aAttributeIndex])

    sortedValues = list(set(sortedValues)).sort()

    if len(sortedValues) < 3:
        return set(sortedValues)
    else:
        retSet.add(sortedValues[int(len(sortedValues) / 3) - 1])
        retSet.add(sortedValues[int(len(sortedValues) / 3 * 2) - 1])
        retSet.add(sortedValues[int(len(sortedValues)) - 1])

# Given a data set and a column index, calculate the weighted entropy of the column
def EntropyColumn(aData, aAttributeIndex):
    if IsNumeric(aData[0][aAttributeIndex]):
        uniqueElements = UniqueElementsNumeric(aData, aAttributeIndex)
    else:
        uniqueElements = UniqueElements(aData, aAttributeIndex)

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
