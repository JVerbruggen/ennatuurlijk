from looopings import *
from messagequeue import *

from dotenv import load_dotenv

def main():
    load_dotenv()

    theme_park = ThemeParkEnum.EFTELING

    looopings = LooopingsScraper()
    waiting_time_item_list = looopings.get_current_waiting_times(theme_park)

    for x in waiting_time_item_list:
        print(x.ride_name)

    message_queue = AzureServiceBusPublisher()
    message_queue.publish_waiting_time_item_list(waiting_time_item_list)

    print("OK done")

if __name__ == "__main__":
    main()
