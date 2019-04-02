#------------------------------------------------------------------
# Author: Julian Sullivan
# Purpose: Definitions of decision tree functions and objects
#------------------------------------------------------------------

import io
import copy

# In DecisionNodes, this will be what determines which branch a value
# will go down.
class Question:
    def __init__(self, aDecisionTree, aAttributeIndex, aValue, aBranchOrLeaf = None):
        # The index of the attribute
        self.Attribute = aAttributeIndex
        # The value this will compare to
        self.Value = aValue
        # The branch or leaf to go down
        self.BranchOrLeaf = aBranchOrLeaf
        # Reference to the decision tree it is in
        self.DecisionTree = aDecisionTree

    # If the given value is equal to the
    def Match(self, aRow):
        val = aRow[self.Attribute]
        if IsFloat(val):
            return val <= self.Value
        else:
            return val == self.Value

    def __repr__(self):
        if IsFloat(self.Value):
            return f"{self.DecisionTree.AttributeNames[self.Attribute]} <= {self.Value}?"
        else:
            return f"{self.DecisionTree.AttributeNames[self.Attribute]} == {self.Value}?"


# In final tree, this will split into branches
class DecisionNode:
    def __init__(self, aQuestion, aTrueBranch, aFalseBranch, aDepth):
        # List of questions.
        # If the values are numeric, the questions are in increasing order.
        # This is so it can short circuit as it iterates through questions by using "less than equal"
        self.Question = aQuestion
        self.TrueBranch = aTrueBranch
        self.FalseBranch = aFalseBranch
        self.Depth = aDepth

    # Given a row of data, return the branch to go down and if it is a branch
    def Decide(aData):
        if question.Match(aData):
            return self.TrueBranch, True
        else: 
            return self.aFalseBranch, True

    def __repr__(self):
        spaces = (" " * self.Depth * 4)
        return f"\n{spaces}{self.Question}\n{spaces}True: {self.TrueBranch}\n{spaces}False: {self.FalseBranch}"


# In final tree, this will be a stopping point
class LeafNode:
    def __init__(self, aRowData, aDepth):
        self.Counts = aRowData # TODO: Make this actual counts!
        self.Depth = aDepth

    # Given a row of data, return counts of every value
    def Decide(self, aData):
        return Counts, False

    def __repr__(self):
        spaces = (" " * self.Depth  * 4)
        return f"\n{spaces}LEAF Counts: {self.Counts}"

class TrainingSet:
    def __init__(self, aFileName):
        # A list of lists of values
        self.Data = []
        # Index to string representation of the index
        self.IndexToString = []

def IsFloat(value):
    try:
        float(value)
        return True
    except:
        return False

# Container for the tree and values loaded in
class DecisionTree:
    def __init__(self):
        # The given training data
        self.TrainingData = []
        # The Root of the tree
        self.Root = None
        # The actual name of each column (attribute name)
        self.AttributeNames = []
        # The max depth of the tree
        self.Depth = 0

    # Simply loads data into TrainingData and converts strs into numbers if possible
    # Also sets up PossibleValues and AttributeNames
    def LoadTrainingData(self, aPath):
        def Clean(aStr):
            return aStr.replace("\n", "")

        for i, line in enumerate(open(aPath)):
            words = line.split(",")
            words = list(map(Clean, words))

            if i == 0:
                self.AttributeNames = list(words)
                continue

            for i, word in enumerate(words):
                if IsFloat(word):
                    words[i] = float(word)

            self.TrainingData.append(words)

    def GetPossibleValues(self, aTrainingData):
        possibleValues = [None] * len(self.AttributeNames)
        for row in aTrainingData:
            for j, word in enumerate(row):
                if IsFloat(word):
                    if possibleValues[j] == None: possibleValues[j] = list()
                    possibleValues.append(word)
                else:
                    if possibleValues[j] == None: possibleValues[j] = set()
                    possibleValues[j].add(word)

        # For numbers, the words converted to floats and put into lists.
        # We need to get the unique elements of that list, sort it and
        # break it into groups (less than X, less than Y, less than Z).
        for i, container in enumerate(possibleValues):
            # Words use sets, numbers use lists
            if isinstance(container, list):
                # Unique and sort
                possibleValues[i] = list(set(possibleValues[i]))
                possibleValues[i].sort()

                # If it's a 0/1 boolean, we don't do this. Also, if there are just 3 or less numbers,
                # we simply leave it as a sorted list
                if len(possibleValues[i]) >= 3:
                    newPossible = list()
                    numPosVals = len(possibleValues[i])

                    newPossible.append(possibleValues[i][int(numPosVals / 3 * 1) - 1])
                    newPossible.append(possibleValues[i][int(numPosVals / 3 * 2) - 1])
                    newPossible.append(possibleValues[i][int(numPosVals / 3 * 3) - 1])

                    possibleValues[i] = list(newPossible)

        return possibleValues

    def IsNumeric(self, aAttributeIndex):
        return isinstance(self.PossibleValues[aAttributeIndex], list)

    # Given the number of trues, falses and total rows, return entropy
    def Entropy(self, Trues, Falses, Total):
        return - ((Trues/Total) * log(Trues/Total, 2) + (Falses/Total) * log(Falses/Total, 2))

    def CreateTree(self):
        self.Root = self.CreateTreeRecursive(self.TrainingData, 0)

    def CreateTreeRecursive(self, aDataSet, aDepth):
        gain, question = self.FindBestSplit(aDataSet)

        if aDepth > self.Depth:
            self.Depth = aDepth

        if gain == 0.0:
            return LeafNode(aDataSet, aDepth)

        trues, falses = self.SplitDataSet(aDataSet, question)

        ifTrueBranch = self.CreateTreeRecursive(trues, aDepth + 1)
        ifFalseBranch = self.CreateTreeRecursive(falses, aDepth + 1)

        return DecisionNode(question, ifTrueBranch, ifFalseBranch, aDepth)

    def FindBestSplit(self, aDataSet):
        uniqueValues = self.GetPossibleValues(aDataSet)
        bestInfo = 0.0
        bestQuestion = None
        parentEntropy = 0.79#Entropy()

        for attribute in range(len(aDataSet[0]) - 1):
            for value in uniqueValues[attribute]:
                question = Question(self, attribute, value)

                trues, falses = self.SplitDataSet(aDataSet, question)

                if len(trues) == 0 or len(falses) == 0:
                    continue

                infoGain = self.InfoGain(trues, falses, parentEntropy)

                if infoGain > bestInfo:
                    bestInfo = infoGain
                    bestQuestion = question

        return bestInfo, bestQuestion

    def SplitDataSet(self, aDataSet, aQuestion):
        trues = []
        falses = []
        for row in aDataSet:
            if aQuestion.Match(row):
                trues.append(row)
            else:
                falses.append(row)

        return trues, falses
        
    def InfoGain(self, Trues, Falses, ParentEntropy):

        return 0.75

    def __repr__(self):
        return str(self.Root)