# Utilizing memoization to cache the sub problems
# Okay, still not optimal ... but about as good as I can do right now
# Hold a cache that's t wide, with as many possible scenarios as exist (0-time to max hold a stock)
# This one actually works, guys

import pandas as pd
import sys
import threading

minTimeToHoldBeforeSell = 30
maxTimeToHoldBeforeSell = 60

#minTimeToHoldBeforeSell = 2
#maxTimeToHoldBeforeSell = 4


#dataFile = "data_test.csv"
dataFile = "data_3600.csv"
#dataFile = "data_all.csv"

# Retrieve csv data
print("Reading data file ...")
csvData = pd.read_csv("data/" + dataFile, sep=',')
stock_price = list(csvData.values[:, 1])

# calculated results for everypossible result at every possible time
# Default to -1 to indicate no cached value present
lookup = []
lookup = [[] for i in range(len(stock_price))]
for i in range(0, len(stock_price)):
    x = [-1 for i in range(maxTimeToHoldBeforeSell+1)]
    lookup[i] = x


def processNodes(time, timeHeld):
    # If at end of time return 0 since nothing can be done once we
    # are out of time
    if (time == len(stock_price)):
        return 0

    global lookup

    # If the result has already been cached, use it and don't peform expensive recursion
    if (lookup[time] != None and lookup[time][timeHeld] != -1):
        return lookup[time][timeHeld]

    # Clear the four possible results (yes, could just use a list, but this is fine)
    a = 0
    b = 0
    c = 0
    d = 0
    # if we don't have anything in hand we can buy or ... not buy! ... always
    if (timeHeld == 0):
        # buy!, so set held status
        a = processNodes(time + 1, 1) - csvData.loc[time, 'Price']
        b = 0 + processNodes(time + 1, 0)  # hold with no stock
    # If we are holding, depending on how long for we can
    # sell or hold, sometimes both
    else:
        # if can hold
        if (timeHeld < maxTimeToHoldBeforeSell):
            c = processNodes(time + 1, timeHeld + 1)  # hold

        # if can sell
        if (timeHeld > minTimeToHoldBeforeSell):
            d = processNodes(time + 1, 0) + csvData.loc[time, 'Price']

    # The maximum from whichever calls were made is the best!
    v = max(a, b, c, d)

    # Cache the value for this time for this 'state' (0 (meaning no stock to-how long can hold for)
    lookup[time][timeHeld] = v

    return v


def process():
    print("Processing...")

    print("Best profit is:" + str(processNodes(0, 0)))

    print("done")


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    threading.stack_size(4096 * 32768)
    thread = threading.Thread(target=process,
                              args=())
    thread.start()
