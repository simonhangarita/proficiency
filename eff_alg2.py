"""
You are given an array of timestamps (in seconds) representing when requests were made to a server.
The server can only handle a maximum of 3 requests within any 10-second window.Write a function isThrottled(timestamps) that returns a list of booleans. 
For each request in the input, return True if it is blocked (because it exceeds the limit) and False if it is allowed.
Constraints:
The timestamps are integers in non-decreasing order.
A request at time $T$ is in the same window as a request at time $X$ if $T - 10 < X \le T$.
"""
from calendar import c
from typing import List
from collections import deque
def isThrottled(timestamps:List[int])-> List[bool]:
    is_throttled=[]
    current_window=deque()
    for timestamp in timestamps:
       #we remove the timestamps from the current window that are out of the new 10 seconds boundary defined
       min=timestamp-10
       #this loop will take at most 3 iteration, therefore it doesnt add more than O(1) to the time complexity of the algorithm
       while current_window and current_window[0]<=min:
           current_window.popleft()
       if len(current_window)<3:
           is_throttled.append(False)
           current_window.append(timestamp)
       else:
           is_throttled.append(True)
    return is_throttled

        