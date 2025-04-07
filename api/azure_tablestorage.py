from azure.data.tables import TableServiceClient
from enum import Enum
import os

from waitingtime_store import *

class AzureTableStorageReaderState(Enum):
    IDLE = 0,
    CONNECTED = 1,
    DISCONNECTED = 2,

class AzureTableStorageReader(WaitingTimeStore):
    def __init__(self):
        self.state = AzureTableStorageReaderState.IDLE

        self._table_client = None

    def __enter__(self):
        assert self.state == AzureTableStorageReaderState.IDLE

        table_storage_connection_string     = os.getenv("AZURE_TABLE_STORAGE_CONNECTION_STRING")
        table_storage_table_name            = os.getenv("AZURE_TABLE_STORAGE_TABLE_NAME")

        table_service_client    = TableServiceClient.from_connection_string(table_storage_connection_string)
        self._table_client      = table_service_client.get_table_client(table_storage_table_name)

        self.state = AzureTableStorageReaderState.CONNECTED

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.state == AzureTableStorageReaderState.CONNECTED

        self._table_client = None

        self.state = AzureTableStorageReaderState.DISCONNECTED

    def _run_query(self, query):
        assert self.state == AzureTableStorageReaderState.CONNECTED

        return self._table_client.query_entities(query_filter=query)

    def _validate_query_parameter(self, parameter: str):
        return parameter.isalnum()

    def get_all_ride_waiting_times(self, theme_park, ride_name, start_time_utc, end_time_utc):
        """Get all waiting times belonging to a ride"""

        assert self._validate_query_parameter(theme_park), "Use only alphanumerical input for parameters"
        assert self._validate_query_parameter(ride_name), "Use only alphanumerical input for parameters"

        print("start: ", start_time_utc)
        query = f"PartitionKey eq '{theme_park}' and ride_name eq '{ride_name}' and timestamp ge datetime'{start_time_utc.isoformat()}' and timestamp lt datetime'{end_time_utc.isoformat()}'"
        entities = self._run_query(query)

        return entities