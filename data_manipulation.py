from typing import List, Dict,Any
import heapq
def cumulative_sum(lst:List[int])->List[int]:
    """
    Given a list of transaction amounts, return the running total (cumulative sum) at each step.
    Args:
        lst (List[int]): A list of integers representing transaction amounts.
    Returns:
            List[int]: A list of integers representing the cumulative sum at each step.
    """
    cumulative_sums=[]
    running_total=0
    for amount in lst:
        running_total+=amount
        cumulative_sums.append(running_total)
    return cumulative_sums
def filter_and_sort(data:List[Dict[Any]])->List[Dict[Any]]:
    """
    Given a list of dicts like [{'user': 'A', 'amount': 120}, ...], filter those with amount > 100 and sort them by amount descending.
    Args:
        data (List[Dict[Any]]): A list of dictionaries containing user and amount information.
    Returns:
        List[Dict[Any]]: A list of dictionaries filtered and sorted by amount.
    """
    filter_data=[dic for dic in data if dic['amount']>100]
    filter_data = sorted(filter_data, key=lambda x: x["amount"],reverse=True)
    return filter_data
    

