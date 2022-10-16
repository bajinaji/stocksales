# stock sales profit making short sighted guru

### Requirements
Python 3+
pandas installed and accessible (use good old pip)
***
### Run project
- Run "python compulsiveBuyer.py" from a bash shell

***
### Description
This is a pretty simple and not great implementation of buying and selling a single stock with the aim to make a profit at the end of the given time span.
The single stock can be bought, and then has to be held for at least 30 minutes and for no more than 60 minutes.

In my naive implementation my "compulsive" buyer will buy at any point in time when they can make a profit selling 30-60 minutes in the future.
There is no awareness of the distant future, so many opportunities will be missed.
They do make a profit, which is something.


### Caveats
Could implement a heuristic for trying future rounds but factoring in a de-incentive

Factor in the concept of taking earlier options that are slightly less profitable but offer future possible higher returns



brute force!!!!  memory overhead, run time ... also can't be bothered ...
at each position make every possible call recurisely (be it hold, buy or sell)


0123456789

0 0
  1

1 0 0 0 0

2 ^ 65000 ... ish

***
### Options
This seems to be an NP Complete scenario, similar to a travelling salesman problem (although my math is not strong these days), so I toyed with implementing a recursive brute force algorithm that branches at every choice path (to hold, buy or sell depending on situation) that would execute each recursive branch one upon the other ...
This would end up with 2 to the power of 65000 paths in this situation I believe, which is nnnnnot really tenable.

Also currently pondering a working backwards system that can minimize the number of open branches by looking at paths that cross over one another ...
However I've spent 3-4 hours on this, and don't really want to invest too much more time


***
#### Notes:
No test cases or so forth ... didn't seem appropriate for an algorithm implementation example.
Python is not my normal professional general purpose language, so apologies for non optimal implementations, I would generally implement in C# or lua or C++ or Typescript (and yes, javascript was a given option but honestly I don't really rate it highly so was happy to go with python, you'll just have to give a little lee-way)