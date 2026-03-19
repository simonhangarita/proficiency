#We will model a class that would receive logs in the following format and using instance methods return information about the logs.
#2024-01-15 10:23:45 GET /api/users 200 145ms
from curses import nocbreak
from typing import List,Dict, Any,Tuple
class LogProcessor:
    def __init__(self, logs: List[str]):
        self.logs=logs

    def count_by_status(self) -> Dict[int, int]:
        """
        We will a return a dictionary with the frequency count for each status in the logs
        Returns:
                logs_status (Dict[int,int]): A dictionary which keys correspond to the status and 
                the values correspond to the frequency of appearing of each status
        """
        #We will use a dictionary to store the frequencies for each status in time complexity O(n) in all status, 
        #plus the storage complexity of the dictionary which is O(n) to store all the keys and values
        logs_status_dict={}
        for log in self.logs:
            log_split=log.split()
            try:
                #We first check if the status is already in the dictionary to add +1 to that count. Otherwise we added it with a value of 1
                if int(log_split[4]) in logs_status_dict:
                    logs_status_dict[int(log_split[4])]+=1
                else:
                    logs_status_dict[int(log_split[4])]=1
            except Exception as e:
                #In this case we a have an invalid log because the size of the log didnt match so we print this
                print("Invalid Log, the size didn't match the correct log size")
        return logs_status_dict

    def average_response_time(self, endpoint: str) -> float:
        """
        We have to return the avarage time response for and endpoint in ms and if the endpoint doesn't exist we throw a value error
        Args:
            endpoint (str): an str which should correspond to a valid endpoint used in the logs
        Returns:
            avg_time (float): This number should correspond to the avarage time that the endpoint query takes in ms
        """
        #First we will create an array to store the times of response for this especific endpoint
        response_times=[]
        for log in self.logs:
            log_split=log.split()
            try:
                #We compared first if the log is the one that is being queried
                if log_split[3]==endpoint:
                    try:
                        #We take the time replacing the ms that we get in the log for "" to obtain just the number
                        time=int(log_split[5].replace('ms',''))
                        response_times.append(time)
                    except:
                        print("The time was not save in the log in the expected format")
            except:
                print("Invalid Log, the size didn't match the correct log size")
        #We get the avg time with the with the following operation in time complexity O(n)
        # and in case we have not times we return -1 to throw the exception later
        avg_time= sum(response_times) / len(response_times) if len(response_times)>0 else -1
        if avg_time==-1:
            raise ValueError("Invalid endpoint search")
        return round(avg_time,2)
    def slowest_endpoints(self, n: int) -> List[Tuple[str, float]]:
        """We return the n slower endpoints in avg as a list of tuples (endpoint, avg_ms).
        Args:
            n(int): The number of endpoint that we want to return in the list
        Return:
            n_slower_endpoints:List[Tuple[str,float]] A list with the n slower endpoints represented as a tuple (endpoint, avg_ms)
        """
       
        #A consideration that we have to make is that if we query all this endpoints using the previous algorithm we make,
        #this would take time O(N) for each query where N is the size of the logs, and O(N^2) time in total to create the dictionary.
        #For this reason the best approach would be to imitate the algorithms behavior and build a dictionary in time O(N) 
        #with the avarages, that we can query in time O(1) and therefore the total time in this case would be O(N) to create the dictionary
        endpoint_time_responses=dict()
        for log in self.logs:
            log_split=log.split()
            try:
                #We first check if the status is already in the dictionary to add +1 to that count. Otherwise we added it with a value of 1
                if log_split[3] in endpoint_time_responses:
                    endpoint_time_responses[log_split[3]].append(int(log_split[5].replace('ms','')))
                else:
                    endpoint_time_responses[log_split[3]]=[int(log_split[5].replace('ms',''))]
            except Exception as e:
                #In this case we a have an invalid log because the size of the log didnt match so we print this
                print("Invalid Log, the size didn't match the correct log size")
        #With the previous dictionary now we can create the correct dictionary that stores only the avarage time 
        #that we are going to query with an algoritm that runs in time complexity O(N) the same as the previous one
        #And don't have to worry about zero division in the following algoritm because it doesn't make sense 
        #to have 0 values for an endpoint in the dictionary  endpoint_time_responses
        endpoint_avg_time={endpoint:round(sum(value)/len(value),2) for endpoint,value in endpoint_time_responses.items()}
        #Now we can order the dictionary in time O(Nlog(N)) for the purpose of searching the n slower endpoints
        endpoint_avg_time = dict(sorted(endpoint_avg_time.items(), key=lambda x: x[1], reverse=True))
        n_slower_endpoints=[]
        #We will use a counter variable to control the loop and break it when needed
        counter=0
        for key in endpoint_avg_time.keys():
            if counter==n:
                break
            n_slower_endpoints.append((key,endpoint_avg_time[key]))
            counter+=1
        return n_slower_endpoints




