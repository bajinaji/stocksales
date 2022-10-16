import pandas as pd


#
# If this guy can make a profit at any given time, he will!
# You probably don't want him as your invester, but luckily he can
# see the future and will never make a loss at worst
#

minTimeToHoldBeforeSell = 30
maxTimeToHoldBeforeSell = 60

#minTimeToHoldBeforeSell = 2
#maxTimeToHoldBeforeSell = 4


# dataFile = "data_test.csv"
dataFile = "data_all.csv"

# test profitability of buying at the given time and selling at any time from time + 59 to time + 1
# timestep is the current time step to assess our position from to determine whether we should
# buy at this timestep or not, and when to sell within the possible timeframe


def returnProfitForPosition(csvData, timeStep):
    # The price we'll be buying at
    buyPrice = csvData.loc[timeStep, 'Price']

    bestSellTime = -1
    bestSellProfit = 0
    bestSellPrice = 0

    # iterate over all possible sell option times (from current time+30 to current time+59) and find highest if available and return it
    # if no profit can be made, return -1
    for i in range(timeStep + minTimeToHoldBeforeSell + 1, min(len(csvData.index) - 1, timeStep + maxTimeToHoldBeforeSell + 1)):
        currentPrice = csvData.loc[i, 'Price']
        # Check if buying at timeStep, and then selling at timeStep+earliestcanSel+i up until max time before sell
        if (currentPrice-buyPrice > bestSellProfit):
            bestSellTime = i
            bestSellPrice = currentPrice
            bestSellProfit = currentPrice-buyPrice

    if (bestSellTime != -1):
        print(
            f'Open at {timeStep} ({buyPrice}), close at {bestSellTime} ({bestSellPrice}), profit of:{bestSellProfit}')

    return {'sellTime': bestSellTime, 'profit': bestSellProfit}


def process():
    currentTimeStep: int = 0
    profit: float = 0

    # Retrieve csv data
    print("Reading data file ...")
    csvData = pd.read_csv("data/" + dataFile, sep=',')

    rows = len(csvData.index)

    # begin processing
    while currentTimeStep + minTimeToHoldBeforeSell < rows:
        buy = returnProfitForPosition(csvData, currentTimeStep)
        if (buy["sellTime"] != -1):
            currentTimeStep = buy["sellTime"] + 1
            profit += buy["profit"]
        else:
            currentTimeStep += 1

    print("...")
    print(f'Profit over entire trading period of {rows} was:{profit}')


if __name__ == "__main__":
    process()
