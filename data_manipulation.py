from typing import List, Dict,Any,Tuple
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
    
def missing_number(nums:List[int])->int:
    """
    We have to find the missing number in a given list of integers that contains all numbers from 1 to n except one.
    Args:
        nums (List[int]): A list of integers containing all numbers from 1 to n except one.
    Returns:
        int: The missing number in the list.
    """
    #We use a set to query information in O(1) considering that all the elements should be different
    #So the time complixity for this function is O(n) which is the time that requires to create the set and search for the missing number
    nums_set=set(nums)
    n=len(nums)+1
    for i in range(1,n+1):
        if i not in nums_set:
            return i
def max_sum_subarray(nums:List[int], k:int)->int:
    """
    Return max sum of subarray of size k
    Args:
        nums (List[int]): A list of integers.
        k (int): The size of the subarray.
    Returns:
        int: The maximum sum of a subarray of size k.
    """
    #We first check if is possible due to the size of the array and the size of the subarray asked
    if len(nums)<k:
        return 0
    max_sum=0
    #We will have this variable to avoid a recalculation of the sum that takes O(k) for each iteration
    current_sum=sum(nums[0:k])
    for i in range(len(nums)-k+1):
        if i==0:
            max_sum=current_sum
        else:
            current_sum=current_sum-nums[i-1]+nums[i+k-1]
            if current_sum>max_sum:
                max_sum=current_sum
    return max_sum
def top_k_users(transactions:List[Dict[Any,Any]], k:int)->List[Tuple[str, int]]:
    """
    Return top k users by total spending
    Args:
        transactions (List[Dict[Any,Any]]): A list of dictionaries containing user and amount information.
        k (int): The number of top users to return.
    Returns:
        List[Tuple[str,int]]: A list of tuples containing the k users with the most spended amount.
    """
    spending_dict={}
    for transaction in transactions:
        if transaction['user'] in spending_dict:
            spending_dict[transaction['user']]+=transaction['amount']
        else:
            spending_dict[transaction['user']]=transaction['amount']
    spending_dict_sorted=sorted(spending_dict.items(),key=lambda x:x[1],reverse=True)
    top_k_users=[]
    count=0
    for clave,valor in spending_dict_sorted:
        if count>=k:
            break
        count+=1
        top_k_users.append((clave,valor))
    return top_k_users
def daily_totals(transactions:List[Dict[Any,Any]])->Dict[str, int]:
    """
    Return the total amount spend daily
    Args:
        transactions (List[Dict[Any,Any]]): A list of dictionaries containing user and amount information.
    Returns:
        Dict[str, int]: A dictionary that contains the string of the date and the amount spend that day
    """
    daily_total={}
    for transaction in transactions:
        if transaction['timestamp'] in daily_total:
            daily_total[transaction['timestamp']]+=transaction['amount']
        else:
            daily_total[transaction['timestamp']]=transaction['amount']
    return daily_total
def flag_large_transactions(transactions:List[Dict[Any,Any]])->List[Dict[Any,Any]]:
    """
    Return transactions such that the amount is 3 times greater that the user avarage until that point
    Args:
        transactions (List[Dict[Any,Any]]): A list of dictionaries containing user and amount information.
    Returns:
       List[Dict[Any, Any]]: A list that contains the transactions that we detect as fraudulent
    """
    #We will have a dictionary to store the avarage spending for user until that point and to keeep it update it we will store 
    #Not only the avarage but the number of transactions for that user
    average_transaction={}
    fraudulent_transactions=[]
    for transaction in transactions:
        if transaction["user"] in average_transaction:
            average,number=average_transaction[transaction["user"]]
            #Before we determined or new avarage we look if it could be clasified as a fraudelent transaction
            if transaction["amount"]>3*average:
                fraudulent_transactions.append(transaction)
            average=((average*number)+transaction["amount"])/(number+1)
            number+=1
            average_transaction[transaction["user"]]=(average,number)
        else:
            average_transaction[transaction["user"]]=(transaction["amount"],1)
    return fraudulent_transactions



