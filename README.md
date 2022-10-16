# stock sales profit making samples
## Thoughts
This seems to be an NP Complete scenario, similar to a travelling salesman problem (although my math is not strong these days), so as you see I've tried effectively brute force methods progressing to limiting the number of calls as much as possible using memoization.
<br><br><br>
## 1. Compulsive Buyer
### Requirements
* Python 3+
* pandas installed and accessible (use good old pip)
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
Well ... it basically sucks
He runs quickly, 30t, and is guaranteed not to make a loss ... that's as good as it gets.

***
<br><br><br>
## 2. Parallel Universes Buyer

### Requirements
* Python 3+
* pandas
* anytree
***
### Run project
- Run "python parallelUniverseBuyer.py" from a bash shell

***
### Description
Brute force at it's best
Uses a list rather than recursion, but does nothing smart, so runs at ... 2 * t..ish.
Runs fine on my tiny test data I created ... I didn't have the patience for it to finish even with the 3600 set.
Just to show my thinking, really.

### Caveats
Well ... this one basically doesn't finish ... at least not in my life time
***
<br><br><br>
## Cached Recursive Buyer
### Requirements
* Python 3+
* pandas
* anytree
***
### Run project
- Run "python cachedRecursionDude.py" from a bash shell
***
### Description
Okay, this one runs ... so long as we allow a massive stack size (I wish stack were interchangeable with heap).
At least, having identified the overlapping sub problems I was able to memoize the data.
So still not perfect in any sense, but this caches the data to ensure limited recursion, and runs at  O(N*(maxtoHold-minToHold)) to account for every possible state at each possible time.
I'd like to have converted into a linear solution, of course, but this is a step in the right direction 
***
<br><br><br>
## Backwards Buyer
### Requirements
* Python 3+
* pandas
* anytree
***
### Run project
- Run "python backwardsBuyer.py" from a bash shell
***
### Description
Finally one I'm happy with.
It was itching in my mind that we could cache backwards ... but I couldn't quite see it in my head.
However, I ralized we can go from the end, work backwards wherever a sale can be made, adding the value from anything ahead that is the best
path, adding 0 for states when cannot make a sale ... and iterate
This is much more efficient, needing only t * (maxHold-minHold) actions, and a constant memory overhead really only of tracking the best path, and (maxHold-minHold) tests in the current iteration for each possible outcome
***
<br><br><br><br><br>
***
## Notes:
No test cases or so forth ... didn't seem appropriate for an algorithm implementation example that is not going to be worked on be multiple people or that necessarily even work!
Python is not my normal professional general purpose language, so apologies for non optimal implementations, I would generally implement in C# or lua or C++ or Lisp or Typescript (and yes, javascript was a given option but honestly I don't really rate it highly so was happy to go with python, you'll just have to give a little lee-way)