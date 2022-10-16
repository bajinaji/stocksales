import csv
import pandas as pd
from anytree import Node, RenderTree

minTimeToHoldBeforeSell = 30
maxTimeToHoldBeforeSell = 60

minTimeToHoldBeforeSell = 2
maxTimeToHoldBeforeSell = 4

dataFile = "data_test.csv"
#dataFile = "data_3600.csv"

# Retrieve csv data
print("Reading data file ...")
csvData = pd.read_csv("data/" + dataFile, sep=',')
rows = len(csvData.index)

# list to contain all possible paths
nodes = []


def createNode(parent, prevState):
    n = Node("t", parent=parent)
    n.timeHeld = -1
    n.timeBought = -1
    if (parent != None):
        n.profit = parent.profit
    n.time = None
    n.prevState = prevState
    n.profit = 0
    return n


winningNode = createNode(None, "S")


def processNodes(n):
    # remove self from list
    nodes.pop()

    global winningNode
    if (n.time == rows):
        if (winningNode.profit < n.profit):
            print(f'"Setting a new winner with a profit of:{n.profit}')
            winningNode = n
    else:
        # Model selling if can or have to - only carry on if make a profit, since otherwise doing nothing would have been better
        if (n.timeHeld > 0 and (n.timeHeld >= minTimeToHoldBeforeSell or n.timeHeld == maxTimeToHoldBeforeSell)):
            profit = (csvData.loc[n.time, 'Price'] -
                      csvData.loc[n.timeBought, 'Price'])
            # only follow this path if the profit was greater than 0
            if (profit > 0):
                n2 = createNode(n, "S")
                n2.timeHeld = 0
                n2.profit = n.profit + profit
                n2.time = n.time + 1
                nodes.append(n2)

        # Model buying (only if having nothing and have enough time to sell)
        # Can always buy so long as have enough time to sell left
        elif (n.timeHeld == 0 and (n.time + minTimeToHoldBeforeSell) < rows):
            n2 = createNode(n, "B")
            n2.time = (n.time + minTimeToHoldBeforeSell + 1)
            n2.timeHeld = minTimeToHoldBeforeSell
            n2.timeBought = n.time
            n2.profit = n.profit
            nodes.append(n2)

        # Model holding in same position so long as worth considering buying still
        if (n.timeHeld < maxTimeToHoldBeforeSell and (n.time + minTimeToHoldBeforeSell) < rows):
            n2 = createNode(n, "H")
            n2.timeBought = n.timeBought
            n2.timeHeld = n.timeHeld + 1 if n.timeHeld > 0 else 0
            n2.time = n.time + 1
            n2.profit = n.profit
            nodes.append(n2)


def process():
    node = Node("base")
    node.time = 0
    node.timeHeld = 0
    node.profit = 0
    node.timeBought = -1
    node.prevState = ""

    nodes.append(node)

    print("Processing...")

    i = 0
    while (len(nodes) > 0):
        processNodes(nodes[len(nodes)-1])
        i = i + 1
        if (i == 1000):
            print(f'List length:{len(nodes)}')
            i = 0

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
