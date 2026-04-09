import pytest
from pytest import approx
from logProccesorAdvance import LogEntry, parse_logs, filter_logs_by_level, occurrences_log_level
#We will create a fixture to create a list of LogEntry objects to use in our tests
@pytest.fixture
def get_log_entries():
    logs=[
        "2024-03-16 10:23:45 ERROR kernel: Out of memory",
        "2024-03-16 10:24:01 INFO systemd: Started service",
        "2024-03-16 10:25:10 WARNING disk: Usage at 85%",
        "2024-03-16 10:26:15 ERROR kernel: Failed to allocate memory",
        "2024-03-16 10:27:20 INFO systemd: Stopped service",
        "2024-03-16 10:28:30 WARNING disk: Usage at 90%"
    ]
    log_entries=[LogEntry(*parse_logs(log)) for log in logs]
    return log_entries
def test_parse_logs():
    #We will test if the parse_logs function is able to return an empty list when the log has not the expected size or has an invalid timestamp
    log_invalid_size="2024-03-16 10:23:45 ERROR kernel:"
    assert parse_logs(log_invalid_size)==[]
    log_invalid_timestamp="2024-03-16 600 ERROR kernel: Out of memory"
    assert parse_logs(log_invalid_timestamp)==[]
def test_filter_logs_by_level(get_log_entries):
    #Verify if the filter_logs_by_level function is working correctly with the default case in the fixture created
    filtered_logs=filter_logs_by_level(get_log_entries)
    assert filtered_logs==[get_log_entries[0], get_log_entries[2],get_log_entries[3],get_log_entries[5]]
def test_occurrences_log_level(get_log_entries):
    #Verify if the occurrences_log_level function is working correctly with the default case in the fixture created
    occurrences=occurrences_log_level(get_log_entries)
    assert occurrences=={"ERROR": 2, "INFO": 2, "WARNING": 2}