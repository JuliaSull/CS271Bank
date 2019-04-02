
import DecisionTree as DT

# Load in all the data
# Put first row into IndexToString vector
# Put the rest of the rows into the data vector as a list of values.
# This will be a list of ROWS!

tree = DT.DecisionTree()

tree.LoadTrainingData("Data/EasySplit.csv")
tree.CreateTree()

print(tree)