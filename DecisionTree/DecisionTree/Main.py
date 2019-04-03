
import DecisionTree as DT

# Load in all the data
# Put first row into IndexToString vector
# Put the rest of the rows into the data vector as a list of values.
# This will be a list of ROWS!

testSets = [
    ["Data/1_EasySplit.csv", {}, -1],
    ["Data/2_MediumSplit.csv", {}, -1],
    ["Data/3_HardSplit.csv", {}, -1],
    ["Data/4_ExpertSplit.csv", {}, -1],
    ["Data/5_NightmareSplit.csv", {0}, 1],
    ["Data/Tennis.csv", {0}, -1],
    ["Data/Dataset.csv", {0, 4}, 9],
]

for test in testSets:
    tree = DT.DecisionTree()
    tree.LoadTrainingData(test[0], test[1], test[2])
    tree.CreateTree()

    print(tree)