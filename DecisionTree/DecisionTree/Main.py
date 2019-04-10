
import DecisionTree as DT
import random

# Load in all the data
# Put first row into IndexToString vector
# Put the rest of the rows into the data vector as a list of values.
# This will be a list of ROWS!

testSets = [
    ["Data/1_EasySplit", {}, -1, False],
    ["Data/2_MediumSplit", {}, -1, False],
    ["Data/3_HardSplit", {}, -1, False],
    ["Data/4_ExpertSplit", {}, -1, False],
    ["Data/5_NightmareSplit", {0}, 1, False],
    ["Data/Tennis", {0}, -1, False],
    ["Data/Dataset", {0, 4}, 9, False],
]

for test in testSets:
    print(f"====== Running: {test[0]} ======")
    tree = DT.DecisionTree()
    tree.LoadTrainingData(test[0] + ".csv", test[1], test[2])
    tree.CreateTree(test[3])

    #print(tree)

    tree.Decide(test[0] + "Test.csv", test[1], test[2])

    print("\n")

def GenerateTestSet(aName):
    file = open("Data/" + aName + ".csv", "w")

    for i in range(500):
        string = ""
        for j in range(10):
            string += f"{random.randint(1,101)}"
            if j != 9:
                string += ","
        file.write(string + "\n")

    file.close()