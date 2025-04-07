from common import *

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from dataclasses import asdict
import json
import os

RETRIEVE_MESSAGE_COUNT = 500
TIMEOUT_SECONDS = 3

class AzureServiceBusConsumer:
    def consume(self, consumer_function):
        # Open service bus client
        servicebus_queue_name           = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME")
        servicebus_connection_string    = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
        servicebus_client               = ServiceBusClient.from_connection_string(servicebus_connection_string)
        print("CONNSB", servicebus_connection_string)

        with servicebus_client:
            with servicebus_client.get_queue_receiver(servicebus_queue_name) as receiver:
                received_msgs = receiver.receive_messages(max_wait_time=TIMEOUT_SECONDS, max_message_count=RETRIEVE_MESSAGE_COUNT)
                for msg in received_msgs:
                    print("Processing incoming message..")
                    result = consumer_function(msg)

                    if result:
                        receiver.complete_message(msg) # Remove from queue
                    else:
                        ScraperLogger().log_error("Message processing failed")
