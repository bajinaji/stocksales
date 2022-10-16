import pandas as pd
import numpy as np

#dataFile = "data_3600.csv"
dataFile = "data_test.csv"

# Retrieve csv data
print("Reading data file ...")
csvData = pd.read_csv("data/" + dataFile, sep=',')
stock_price = list(csvData.values[:, 1])


# min_hold = 30 + 1  # min hold time
# max_hold = 60 + 1  # max hold time
min_empty = 1  # min time step that you can be not holding the stock

min_hold = 2 + 1  # min hold time
max_hold = 4 + 1  # max hold time

# start at the end of the list, and build up the optimal thing to do at each time step

# Buy = True, Do nothing = False, Don't know yet = None
best_action = [None] * len(stock_price)

# From each point, where should we go next.
# If the action is do nothing, we will go to the next element in the list
# If the action is buy, we will go to the sell element
next_index = [None] * len(stock_price)

# What is the max profit we can make from that index by following the optimal path
max_profit_from_index = [0] * len(stock_price)


def processStocks():
    # start at the end of the stock price list and work backwards
    for i in range(len(stock_price)-1, -1, -1):

        # Skip all the lines where we can't fit in a trade TODO: move out of the loop ???
        if i + min_hold > len(stock_price) - 1:
            next_index[i] = i + 1
            best_action[i] = False
            continue

        # Need to work out the highest total profit of all the points from i to i+max_hold
        # The points from i to min_hold won't have any additional trades
        # The points from min_hold to max_hold will have 1 additional trade
        total_profits = [0]*(max_hold+1)

        # set values where cannot trade to best value from next time iteration (0 steps ahead to min hold time where cannot sell)
        for j in range(0, min_hold):
            total_profits[j] = max_profit_from_index[i+j+1]

        # set values if traded at all possible times from min hold time to max hold time + best choice in next time iteration
        for j in range(min_hold, min(max_hold+1, len(stock_price)-i)):
            total_profits[j] = stock_price[i+j] - stock_price[i]
            if i+j+1 < len(max_profit_from_index):
                total_profits[j] += max_profit_from_index[i+j+1]

        m = max(total_profits)
        # there may be more than one max TODO: check if there are ? Does it matter?  Will hold all best, but just use the first for now
        max_index = [k for k, j in enumerate(total_profits) if j == m]

        next_index[i] = i + max_index[0] + 1
        max_profit_from_index[i] = m

        # TODO: maybe we don't need the best action, we can read it off from the where the next index is, but whatever, lets have it for now
        best_action[i] = max_index[0] > (min_hold - 1)

        # best path, output backwards, of course
        print(
            f"Starting at index: {i}, max profit: {max_profit_from_index[i]:.4f}, holding till index: {i+max_index[0]+1}")


def process():
    print("Processing...")

    processStocks()

    print("done")


if __name__ == "__main__":
    process()