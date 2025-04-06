from azure_servicebus_consumer import *
from azure_tablestorage import *

import json

from dotenv import load_dotenv

def main():
    load_dotenv()

    tablestorage_publisher = AzureTableStoragePublisher()

    def _process_incoming_waiting_time_message(message):
        waiting_time_message = json.loads(str(message))

        serialized_waiting_time_item = SerializedWaitingTimeItem(
            theme_park=waiting_time_message.get('theme_park'),
            ride_name=waiting_time_message.get('ride_name'),
            waiting_time=waiting_time_message.get('waiting_time'),
            ride_state=waiting_time_message.get('ride_state'),
            timestamp=waiting_time_message.get('timestamp')
        )

        # Store incoming message on the Azure table storage
        result = tablestorage_publisher.store(serialized_waiting_time_item)

        return result

    # Open table storage context
    with tablestorage_publisher:

        # Read through service bus messages and process them
        servicebus_consumer = AzureServiceBusConsumer()
        servicebus_consumer.consume(_process_incoming_waiting_time_message)

if __name__ == "__main__":
    main()
