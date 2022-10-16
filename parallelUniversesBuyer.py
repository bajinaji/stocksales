import csv
import pandas as pd
from anytree import Node, RenderTree

winningNode = Node("t")
winningNode.profit = 0

minTimeToHoldBeforeSell = 30
maxTimeToHoldBeforeSell = 60

#minTimeToHoldBeforeSell = 2
#maxTimeToHoldBeforeSell = 4


# dataFile = "data_test.csv"
dataFile = "data_3600.csv"

# Retrieve csv data
print("Reading data file ...")
csvData = pd.read_csv("data/" + dataFile, sep=',')
rows = len(csvData.index)


def createNode(parent):
    n = Node("t", parent=parent)
    n.timeHeld = -1
    n.timeBought = -1
    n.profit = parent.profit
    n.time = None
    n.prevState = "D"
    return n


def processNodes(n):
    global winningNode
    if (n.time == rows):
        if (winningNode.profit < n.profit):
            print("Setting new winner")
            winningNode = n
    else:
        # Model selling - only carry on if make a profit, since otherwise doing nothing would have been better
        if (n.timeHeld > 0 and n.timeHeld >= minTimeToHoldBeforeSell):
            profit = (csvData.loc[n.time, 'Price'] -
                      csvData.loc[n.timeBought, 'Price'])
            if (profit > 0 or n.timeHeld == maxTimeToHoldBeforeSell):
                n2 = createNode(n)
                n2.timeHeld = 0
                n2.timeBought = -1
                n2.profit = n.profit + profit
                n2.time = n.time + 1
                n2.prevState = "S"
                processNodes(n2)

        # Model buying (only if having nothing and have enough time to sell)
        elif (n.timeHeld == 0 and (n.time + minTimeToHoldBeforeSell) < rows):
            n2 = createNode(n)
            n2.time = (n.time + minTimeToHoldBeforeSell + 1)
            n2.timeHeld = minTimeToHoldBeforeSell
            n2.timeBought = n.time
            n2.profit = n.profit
            n2.prevState = "B"
            processNodes(n2)

        # Model holding
        if (n.timeHeld < maxTimeToHoldBeforeSell):
            n2 = createNode(n)
            n2.timeBought = n.timeBought
            n2.timeHeld = n.timeHeld + 1 if n.timeHeld > 0 else 0
            n2.time = n.time + 1
            n2.profit = n.profit
            n2.prevState = "H"
            processNodes(n2)


def process():
    node = Node("base")
    node.time = 0
    node.timeHeld = 0
    node.profit = 0
    node.timeBought = -1
    node.prevState = ""

    processNodes(node)
    print("...")
    print(
        f'Profit over entire trading period of {rows} was:{winningNode.profit}')

    # print(RenderTree(node))

    n = winningNode
    pathAsString = ""
    while (n.parent != None):
        pathAsString = f'[{n.prevState}][{n.parent.time}]' + \
            str(n.profit) + "->" + pathAsString
        n = n.parent

    print(pathAsString)


if __name__ == "__main__":
    process()
