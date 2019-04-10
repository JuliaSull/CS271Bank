
import DecisionTree as DT
import random
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
from sklearn import tree
import pandas as pd

# Load in all the data
# Put first row into IndexToString vector
# Put the rest of the rows into the data vector as a list of values.
# This will be a list of ROWS!


def CalcFunc(aArray):
    result = 0
    for i, num in enumerate(aArray):
        if i % 2 == 0: 
            result += num
        else:
            result -= num

    if result > 50:
        return 1
    else:
        return 0

def GenerateTestSet(aName):
    file = open("Data/" + aName + ".csv", "w")

    for i in range(500):
        toCalc = []
        string = ""
        for j in range(10):
            rand = random.randint(1,101)
            toCalc.append(rand)
            string += f"{rand},"
        string += str(CalcFunc(toCalc))
        file.write(string + "\n")

    file.close()

    file = open("Data/" + aName + "Test.csv", "w")

    for i in range(500):
        toCalc = []
        string = ""
        for j in range(10):
            rand = random.randint(1,101)
            toCalc.append(rand)
            string += f"{rand},"
        string += str(CalcFunc(toCalc))
        file.write(string + "\n")

    file.close()

GenerateTestSet("Random")

testSets = [
    ["Data/1_EasySplit", {}, -1, False, False, -1, False, False],
    ["Data/2_MediumSplit", {}, -1, False, False, -1, False, False],
    ["Data/3_HardSplit", {}, -1, False, False, -1, False, False],
    ["Data/4_ExpertSplit", {}, -1, False, False, -1, False, False],
    ["Data/5_NightmareSplit", {0}, 1, False, False, -1, False, False],
    ["Data/Random", {}, -1, False, False, -1, True, True],
    ["Data/Tennis", {0}, -1, True, False, -1, False, False],
    ["Data/Dataset", {0, 4}, 9, False, False, -1, True, False],
    ["Data/Dataset", {0, 1, 2, 4, 10, 12, 13}, 9, False, False, -1, True, True],
]

for i in range(250, 4100, 250):
    testSets.append(["Data/Dataset", {0, 1, 2, 4, 10, 12, 13}, 9, False, True, i, False, False])

records = [[],[]]

for test in testSets:
    print(f"====== Running: {test[0]} ======")
    dTree = DT.DecisionTree()
    dTree.LoadTrainingData(test[0] + ".csv", test[1], test[2], test[5])
    dTree.CreateTree(test[3])

    #print(tree)

    results = dTree.Decide(test[0] + "Test.csv", test[1], test[2])

    print("\n")

    if test[4]:
        records[0].append(test[5])
        records[1].append(results.Accuracy)

    if test[6]:
        sb.heatmap(dTree.ConvertToCorrelMatrix(), xticklabels=dTree.AttributeNames, yticklabels=dTree.AttributeNames, vmin=-1, vmax=1, cmap="seismic")
        plt.show()

    if test[7]:
        sciResults = dTree.DecideSciKit(test[0] + "Test.csv", test[1], test[2])

        dd = [
            ["Custom", "Accuracy", results.Accuracy],
            ["Custom", "Precision", results.Precision],
            ["Custom", "Recall", results.Recall],
            ["SciKit", "Accuracy", sciResults.Accuracy],
            ["SciKit", "Precision", sciResults.Precision],
            ["SciKit", "Recall", sciResults.Recall],
            ]
        df = pd.DataFrame(data=dd, columns=["Type", "Metric", "Value"])

        sb.barplot(x = "Metric", y="Value", hue = "Type", data = df)
        plt.show()
        
sb.set(style="darkgrid")
sb.lineplot(x=records[0], y=records[1])
plt.show()
