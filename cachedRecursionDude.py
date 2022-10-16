import pandas as pd
from anytree import Node, RenderTree
import os
import sys
import threading

winningNode = Node("t")
winningNode.profit = 0

minTimeToHoldBeforeSell = 30
maxTimeToHoldBeforeSell = 60

#minTimeToHoldBeforeSell = 2
#maxTimeToHoldBeforeSell = 4


#dataFile = "data_test.csv"
dataFile = "data_3600.csv"
dataFile = "data_all.csv"

# Retrieve csv data
print("Reading data file ...")
csvData = pd.read_csv("data/" + dataFile, sep=',')
rows = len(csvData.index)

# list to contain all possible paths
nodes = []

# calculated results for a given day if buy
lookup = []
lookup = [[] for i in range(rows)]
for i in range(0, rows):
    x = [-1 for i in range(maxTimeToHoldBeforeSell+1)]
    lookup[i] = x


def processNodes(time, timeHeld):
    if (time == rows):
        return 0

    global lookup

    if (lookup[time] != None and lookup[time][timeHeld] != -1):
        if (time == 17):
            i = 1
        return lookup[time][timeHeld]

    a = 0
    b = 0
    c = 0
    d = 0
    # if we don't have anything in hand we can buy or not buy
    if (timeHeld == 0):
        # buy!, so set held status
        a = processNodes(time + 1, 1) - csvData.loc[time, 'Price']
        b = 0 + processNodes(time + 1, 0)  # hold with no stock
    else:
        # if can hold
        if (timeHeld < maxTimeToHoldBeforeSell):
            c = processNodes(time + 1, timeHeld + 1)  # hold

        # if can sell
        if (timeHeld > minTimeToHoldBeforeSell):
            d = processNodes(time + 1, 0) + csvData.loc[time, 'Price']

    v = max(a, b, c, d)

    lookup[time][timeHeld] = v

    return v


def process():
    print("Processing...")

    print(processNodes(0, 0))

    print("done")


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    threading.stack_size(4096 * 32768)
    thread = threading.Thread(target=process,
                              args=())
    thread.start()
