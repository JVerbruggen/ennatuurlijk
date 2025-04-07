from common import *

from azure.data.tables import TableServiceClient, TableClient, TableEntity
from enum import Enum
import os

class AzureTableStoragePublisherState(Enum):
    IDLE = 0,
    CONNECTED = 1,
    DISCONNECTED = 2,

class AzureTableStoragePublisher:
    def __init__(self):
        self.state = AzureTableStoragePublisherState.IDLE

        self._table_client = None

    def __enter__(self):
        assert self.state == AzureTableStoragePublisherState.IDLE

        table_storage_connection_string     = os.getenv("AZURE_TABLE_STORAGE_CONNECTION_STRING")
        table_storage_table_name            = os.getenv("AZURE_TABLE_STORAGE_TABLE_NAME")
        print("CONNTS", table_storage_connection_string)

        table_service_client = TableServiceClient.from_connection_string(table_storage_connection_string)
        self._table_client = table_service_client.get_table_client(table_storage_table_name)

        self.state = AzureTableStoragePublisherState.CONNECTED

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.state == AzureTableStoragePublisherState.CONNECTED

        self._table_client = None

        self.state = AzureTableStoragePublisherState.DISCONNECTED

    def store(self, serialized_waiting_time_item: SerializedWaitingTimeItem):
        assert self.state == AzureTableStoragePublisherState.CONNECTED, "Not connected"

        partition_key = serialized_waiting_time_item.theme_park
        row_key = f"{serialized_waiting_time_item.ride_name}-{serialized_waiting_time_item.timestamp}"

        print("storing stuff")
        entity = TableEntity(
            PartitionKey=partition_key,
            RowKey=row_key,
            theme_park=serialized_waiting_time_item.theme_park,
            ride_name=serialized_waiting_time_item.ride_name,
            waiting_time=serialized_waiting_time_item.waiting_time,
            ride_state=serialized_waiting_time_item.ride_state,
            timestamp=datetime.fromisoformat(serialized_waiting_time_item.timestamp.replace("Z", "+00:00"))
        )

        self._table_client.create_entity(entity=entity)
        print("done storing stuff")

        return True
