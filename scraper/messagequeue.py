from common import *

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from dataclasses import asdict
import json
import os

class AzureServiceBusPublisher:
    def publish_waiting_time_item_list(self, waiting_time_item_list: list[WaitingTimeItem]):
        # Open service bus client
        servicebus_queue_name           = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME")
        servicebus_connection_string    = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
        print("CONN", servicebus_connection_string)
        servicebus_client               = ServiceBusClient.from_connection_string(servicebus_connection_string)

        with servicebus_client:
            sender = servicebus_client.get_queue_sender(queue_name=servicebus_queue_name)

            with sender:
                for waiting_time_item in waiting_time_item_list:
                    message_data = json.dumps(asdict(waiting_time_item), default=Serializer.custom_serializer)
                    message = ServiceBusMessage(message_data)
                    sender.send_messages(message)

        message_count = len(waiting_time_item_list)
        print(f"{message_count} messages sent!")
