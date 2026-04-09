"""
You are given a list of server log entries as strings in this format:
    "2024-03-16 10:23:45 ERROR kernel: Out of memory"
    "2024-03-16 10:24:01 INFO systemd: Started service"
    "2024-03-16 10:25:10 WARNING disk: Usage at 85%"
1) Parse the logs into structured objects using a class LogEntry with attributes: timestamp, level, source, and message.
2) Filter logs by level (e.g., return only ERROR or WARNING entries).
3) Count occurrences of each log level and return a dictionary.
4) Find the most recent log entry for a given source (e.g., "kernel").
5) Write a generator that yields log entries one by one from a large list without loading all into memory.
"""
from typing import List, Dict, Generator
from datetime import datetime as dt
def parse_logs(log:str)->List[any]:
    """
    This function will parse a log in the specified format and return a list with the different components necessary to create a LogEntry object
    Args:
        log (str): A string in the format "2024-03-16 10:23:45 ERROR kernel: Out of memory"
    Returns:
        List[Any]: A list containing the parsed components [timestamp, level, source, message]
    """
    log_split=log.split()
    timestamp=None
    level=None
    source=None
    message=None
    try:
        timestamp=dt.strptime(log_split[0]+" "+log_split[1], "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print("The timestamp in the log is not in the expected format")
    try:
        level=log_split[2]
        source=log_split[3].replace(":","")
        message=" ".join(log_split[4:])
    except Exception as e:
        print('The log is not in the expected format due to the size of the log')
    if level and source and message and timestamp:
        return [timestamp, level, source, message]
    else:
        return []
class LogEntry:
    def __init__(self,timestamp:str,level:str,source:str,message:str):
        self.timestamp=timestamp
        self.level=level
        self.source=source
        self.message=message
def filter_logs_by_level(logs:List[LogEntry],levels: List[str] = ["ERROR", "WARNING"])->List[LogEntry]:
    """
    This function will filter the logs by level and return only the logs that are either ERROR or WARNING
    Args:
        logs (List[LogEntry]): A list of LogEntry objects
    Returns:
        List[LogEntry]: A list of LogEntry objects that are either ERROR or WARNING
    """
    return [log for log in logs if log.level in levels]
def occurrences_log_level(logs:List[LogEntry])->Dict[str,int]:
    """
    This function will count the ocurrences of each log level and return a dictionary with the count for each level
    Args:
        logs (List[LogEntry]): A list of LogEntry objects)
    Returns:
            Dict[str,int]: A dictionary with the count for each log level
    """
    log_level_count={}
    for log in logs:
        if log.level in log_level_count:
            log_level_count[log.level]+=1
        else:
            log_level_count[log.level]=1
    return log_level_count
def most_recent_log_by_source(logs:List[LogEntry],source:str)->LogEntry:
    """
    This function will find the most recent log entry for a given source and return it
    Args:
        logs (List[LogEntry]): A list of LogEntry objects
        source (str): The source to search for
    Returns:
        LogEntry: The most recent log entry for the given source
    """
    #Previously define two variables to store the most recent log and the most recent timestamp for the given source
    most_recent_log=None
    most_recent_timestamp=None
    for log in logs:
        if log.source==source:
            if most_recent_timestamp is None or log.timestamp>most_recent_timestamp:
                most_recent_log=log
                most_recent_timestamp=log.timestamp
    return most_recent_log
def log_entry_generator(logs:List[str])->Generator[LogEntry,None,None]:
    """
    This function will be a generator that yields log entries one by one from a large list of logs without loading all into memory
    Args:
        logs (List[str]): A list of log strings
    Returns:
        Generator[LogEntry,None,None]: A generator that yields LogEntry objects one by one
    """
    for log in logs:
        parsed_log=parse_logs(log)
        if parsed_log:
            yield LogEntry(*parsed_log)
def main():
    logs=["2024-03-16 10:23:45 ERROR kernel: Out of memory",
        "2024-03-16 10:24:01 INFO systemd: Started service",
        "2024-03-16 10:25:10 WARNING disk: Usage at 85%"]
    parsed_logs=[parse_logs(log) for log in logs]
    log_entries=[LogEntry(*log) for log in parsed_logs if log]
    filter_logs=filter_logs_by_level(log_entries)
    ocurrences=occurrences_log_level(log_entries)
    most_recent_log=most_recent_log_by_source(log_entries,"kernel")
    generator=log_entry_generator(logs)
    for entry in generator:
        print(f"Timestamp: {entry.timestamp}, Level: {entry.level}, Source: {entry.source}, Message: {entry.message}")
if __name__=="__main__":
    main()

