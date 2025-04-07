from azure_tablestorage import *
from waitingtime_store import *

def create_waiting_time_store() -> WaitingTimeStore:
    return AzureTableStorageReader()