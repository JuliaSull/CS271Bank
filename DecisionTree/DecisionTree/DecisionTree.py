#------------------------------------------------------------------
# Author: Julian Sullivan
# Purpose: Definitions of decision tree functions and objects
#------------------------------------------------------------------

# In DecisionNodes, this will be what determines which branch a value
# will go down.
class QuestionEqual:
    def __init__(self, aAttributeIndex, aValue, aBranchOrLeaf = None):
        # The index of the attribute
        self.Attribute = aAttributeIndex
        # The value this will compare to
        self.Value = aValue
        # The branch or leaf to go down
        self.BranchOrLeaf = aBranchOrLeaf

    # If the given value is equal to the
    def Match(aData):
        val = aData[self.Attribute]
        if IsNumeric(val):
            return val <= self.Value
        else:
            return val == self.Value


# In final tree, this will split into branches
class DecisionNode:
    def __init__(self, aQuestionList):
        # List of questions.
        # If the values are numeric, the questions are in increasing order.
        # This is so it can short circuit as it iterates through questions by using "less than equal"
        self.QuestionList = aQuestionList

    # Given a row of data, return the branch to go down and if it is a branch
    def Decide(aData):
        for question in QuestionList:
            if question.Match(aData):
                return question.BranchOrLeaf, True


# In final tree, this will be a stopping point
class LeafNode:
    def __init__(self, aRowData):
        self.Counts = aRowData # TODO: Make this actual counts!

    # Given a row of data, return counts of every value
    def Decide(aData):
        return Counts, False

class TrainingSet:
    def __init__(self, aFileName):
        # A list of lists of values
        self.Data = []
        # Index to string representation of the index
        self.IndexToString = []

# Container for the tree and values loaded in
class DecisionTree:
    def __init__(self, aTrainingData):
        # The given training data
        self.TrainingData = aTrainingData
        # The Root of the tree
        self.Root = None
        # The possible values of the column
        self.PossibleValues = []

    def CreateTree():
        

