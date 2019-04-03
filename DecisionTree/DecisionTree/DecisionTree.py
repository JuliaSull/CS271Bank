#------------------------------------------------------------------
# Author: Julian Sullivan
# Purpose: Definitions of decision tree functions and objects
#------------------------------------------------------------------

import io
import copy
import math

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
    def __init__(self, aQuestions, aBranches, aDepth):
        # List of questions.
        # If the values are numeric, the questions are in increasing order.
        # This is so it can short circuit as it iterates through questions by using "less than equal"
        self.Questions = aQuestions
        self.Branches = aBranches
        self.Depth = aDepth

    # Given a row of data, return the branch to go down and if it is a branch
    def Decide(self, aData):
        for i, question in enumerate(self.Questions):
            if question.Match(aData):
                return self.Branches[i].Decide(aData)
        return self.Branches[0].Decide(aData)

    def __repr__(self):
        spaces1 = (" " * (self.Depth + 0) * 4)
        retStr = ""
        for i, branch in enumerate(self.Branches):
            retStr += f"{spaces1}{self.Questions[i]}\n"
            retStr += f"{branch}"
        return retStr

# In final tree, this will be a stopping point
class LeafNode:
    def __init__(self, aRowData, aDepth):
        self.Counts = self.CalculateCounts(aRowData)
        self.Depth = aDepth

    def CalculateCounts(self, aRowData):
        counts = {}
        for row in aRowData:
            val = row[len(row) - 1]
            counts.setdefault(val, 0)
            counts[val] += 1

        return counts

    # Given a row of data, return counts of every value
    def Decide(self, aData):
        return self.Counts

    def __repr__(self):
        spaces = (" " * self.Depth  * 4)
        return f"{spaces}LEAF Counts: {self.Counts}\n"

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
        # The unique values of the full TrainingData set
        self.GlobalUniqueValues = []
        # all the questions for the full training data set
        self.GlobalQuestions = []

    def Decide(self, aPath, aIgnoredIndexes, aTargetIndex):
        def Clean(aStr):
            return aStr.replace("\n", "")

        testData = []

        for i, line in enumerate(open(aPath)):
            if i == 0:
                continue
            words = line.split(",")
            words = list(map(Clean, words))

            for i, word in enumerate(words):
                if IsFloat(word):
                    words[i] = float(word)

            final = []
            for index, word in enumerate(words):
                if index not in aIgnoredIndexes and index != aTargetIndex:
                    final.append(word)
            if aTargetIndex >= 0:
                final.append(words[aTargetIndex])

            testData.append(final)

        total = 0
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        P = 0
        N = 0
        for row in testData:
            counts = self.Root.Decide(row)
            answer = row[len(row)-1]

            guessedTrue = "Yes" in counts.keys() or 1 in counts.keys()
            guessedFalse = "No" in counts.keys() or 0 in counts.keys()
            wasTrue = answer == "Yes" or answer == 1
            wasFalse = answer == "No" or answer == 0

            print(f"Row: {row} | Counts: {counts} | Matches?: {guessedTrue == wasTrue}")

            total += 1

            if wasTrue: P += 1
            else: N += 1

            if P == 0: P = 1

            if guessedTrue and wasTrue: TP += 1
            elif guessedFalse and wasFalse: TN += 1
            elif guessedTrue and wasFalse: FP += 1
            elif guessedFalse and wasTrue: FN += 1

        print(f"Accuracy: {((TP + TN) / (P + N)) * 100}%")
        print(f"Precision: {(TP / (TP + FP)) * 100}")
        print(f"Recall: {(TP / P) * 100}")

        print(f"       | true  | false | ACTUAL")
        print(f"-------|-------|-------|")
        print(f" true  |{TP}|{FN}|")
        print(f"-------|       |       |")
        print(f" false |{FP}|{TN}|")
        print(f" GUESS")




    # Simply loads data into TrainingData and converts strs into numbers if possible
    # Also sets up PossibleValues and AttributeNames
    def LoadTrainingData(self, aPath, aIgnoredIndexes, aTargetIndex):
        def Clean(aStr):
            return aStr.replace("\n", "")

        for i, line in enumerate(open(aPath)):
            words = line.split(",")
            words = list(map(Clean, words))

            if i == 0:
                for index, word in enumerate(words):
                    if index not in aIgnoredIndexes and index != aTargetIndex:
                        self.AttributeNames.append(word)
                if aTargetIndex >= 0:
                    self.AttributeNames.append(words[aTargetIndex])
                continue

            for i, word in enumerate(words):
                if IsFloat(word):
                    words[i] = float(word)

            final = []
            for index, word in enumerate(words):
                if index not in aIgnoredIndexes and index != aTargetIndex:
                    final.append(word)
            if aTargetIndex >= 0:
                final.append(words[aTargetIndex])

            self.TrainingData.append(final)

    def GetChildPossibleValues(self, aDataSet):
        possibleValues = [None] * len(self.AttributeNames)
        for row in aDataSet:
            for i, word in enumerate(row):
                if IsFloat(word):
                    if possibleValues[i] == None: possibleValues[i] = list()
                    for question in self.GlobalQuestions[i]:
                        if question.Match(row):
                            possibleValues[i].append(question.Value)
                            break
                else:
                    if possibleValues[i] == None: possibleValues[i] = set()
                    for question in self.GlobalQuestions[i]:
                        if question.Match(row):
                            possibleValues[i].add(question.Value)
                            break

        for i, valList in enumerate(possibleValues):
            if isinstance(possibleValues[i], list):
                possibleValues[i] = list(set(possibleValues[i]))
                possibleValues[i].sort()

        return possibleValues

    def GetPossibleValues(self, aTrainingData):
        possibleValues = [None] * len(self.AttributeNames)
        for row in aTrainingData:
            for j, word in enumerate(row):
                if IsFloat(word):
                    if possibleValues[j] == None: possibleValues[j] = list()
                    possibleValues[j].append(word)
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

    def GetQuestions(self):
        for i, values in enumerate(self.GlobalUniqueValues):
            for val in values:
                while len(self.GlobalQuestions) - 1 < i: self.GlobalQuestions.append([])
                self.GlobalQuestions[i].append(Question(self.TrainingData, i, val))

    def CreateTree(self):
        self.GlobalUniqueValues = self.GetPossibleValues(self.TrainingData)
        self.GetQuestions()
        self.Root = self.CreateTreeRecursive(self.TrainingData, 0)

    def CreateTreeRecursive(self, aDataSet, aDepth):
        childUniqueValues = self.GetChildPossibleValues(aDataSet)
        if not self.CanSplit(aDataSet, childUniqueValues, self.GlobalUniqueValues):
            return LeafNode(aDataSet, aDepth)

        giniIndex, attributeIndex = self.FindBestSplit(aDataSet, childUniqueValues)

        if aDepth > self.Depth:
            self.Depth = aDepth

        questions = []
        
        for att in childUniqueValues[attributeIndex]:
            questions.append(Question(self, attributeIndex, att))

        splitSets = [None] * len(questions)
        for row in aDataSet:
            for i, question in enumerate(questions):
                if question.Match(row):
                    if splitSets[i] == None:
                        splitSets[i] = []
                    splitSets[i].append(row)
                    break

        branches = []
        for i in range(len(splitSets)):
            branches.append(self.CreateTreeRecursive(splitSets[i], aDepth + 1))

        return DecisionNode(questions, branches, aDepth)

    def CanSplit(self, aDataSet, uniqueValues, globalUniqueValues):
        if len(uniqueValues[len(uniqueValues) - 1]) == 1:
            return False 

        for attribute in range(len(uniqueValues) - 1):
            if IsFloat(globalUniqueValues[attribute]):
                # If all of the values are part of the same global set, we'll get through
                # the whole loop
                question = Question(aDataSet, attribute, globalUniqueValues[attribute])
                answerAbs = 0
                for row in aDataSet:
                    matches = question.Match(row)

                    # If we've been counting up and then we suddenly count down, we know there's at least two groups
                    if matches and answerAbs < 0:       return True
                    elif not matches and answerAbs > 0: return True

                    # Count up if matches, down if it doesn't.
                    if matches: answerAbs += 1
                    else:       answerAbs -= 1
            else:
                if len(uniqueValues[attribute]) > 1:
                    return True

        return False

    def FindBestSplit(self, aDataSet, uniqueValues):
        bestInfo = 2.0
        bestAttribute = -1

        for attribute in range(len(aDataSet[0]) - 1):
            if len(uniqueValues[attribute]) == 1:
                continue

            giniIndex = self.GiniIndex(aDataSet, attribute, uniqueValues)
            if giniIndex < bestInfo:
                bestInfo = giniIndex
                bestAttribute = attribute

        return bestInfo, bestAttribute

    def GiniIndex(self, aDataSet, aAttributeIndex, aPossibleValues):
        uniqueElements = aPossibleValues[aAttributeIndex]

        if len(uniqueElements) == 1: return 0.0

        total = len(aDataSet)
        entropy = 0.0
    
        for ele in uniqueElements:
            trues, falses, count = self.Counts(aDataSet, ele, aAttributeIndex)
            if count == 0:
                continue
            individualGini = (1 - (trues / count)**2 - (falses / count)**2)
            totalPercent = (count / total)
            entropy += totalPercent * individualGini

        return entropy

    # Returns the number of trues, falses and totals for a given value in a given column 
    def Counts(self, aData, aElement, aAttributeIndex):
        count = 0
        trues = 0
        for data in aData:
            if data[aAttributeIndex] == aElement:  
                count += 1
                if data[len(data) - 1] == "Yes" or data[len(data) - 1] == 1: 
                    trues += 1
        return trues, count - trues, count

    def __repr__(self):
        return str(self.Root)