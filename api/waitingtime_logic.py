from collections import defaultdict
from datetime import datetime, timedelta, timezone

from waitingtime_store_factory import *
from ridestore import *

class WaitingTimeLogic:
    def __init__(self):
        self._ride_store = RideStore()
        self._waiting_time_store = create_waiting_time_store()

    def get_hourly_waiting_times(self, theme_park, ride_name):
        """"Get waiting times grouped per hour"""

        time_zone_theme_park = self._ride_store.get_time_zone(theme_park)

        target_date = datetime.now(timezone.utc)
        start_time = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = target_date + timedelta(days=1)

        # Request data from waiting time store
        with create_waiting_time_store() as waiting_time_store:
            entities = waiting_time_store.get_all_ride_waiting_times(theme_park, ride_name, start_time, end_time)

        hour_buckets = defaultdict(list)
        for record in entities:
            ts = datetime.fromisoformat(record["timestamp"]).replace(tzinfo=pytz.utc)
            ts.tzinfo
            local_ts = ts.astimezone(time_zone_theme_park)
            hour = local_ts.hour
            waiting_time = int(record["waiting_time"])
            hour_buckets["{:02d}:00".format(hour)].append(waiting_time)

        return hour_buckets

    def get_hourly_waiting_time_averages(self, theme_park, ride_name):
        """"Get waiting times averages grouped per hour"""

        time_zone_theme_park = ride_store.get_time_zone(theme_park)

        target_date = datetime.now(timezone.utc)
        # start_time = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = target_date
        end_time = target_date + timedelta(days=1)

        # Request data from azure database
        # filter_query = f"PartitionKey eq '{theme_park}' and timestamp ge datetime'{start_time.isoformat()}' and timestamp lt datetime'{end_time.isoformat()}'"
        with create_waiting_time_store() as waiting_time_store:
            entities = waiting_time_store.get_all_ride_waiting_times(theme_park, ride_name, start_time, end_time)

        # Group data per hour
        hour_buckets = defaultdict(list)
        for record in entities:
            ts = datetime.fromisoformat(record["timestamp"]).replace(tzinfo=pytz.utc)
            ts.tzinfo
            local_ts = ts.astimezone(time_zone_theme_park)
            hour = local_ts.hour
            waiting_time = int(record["waiting_time"])
            hour_buckets["{:02d}:00".format(hour)].append(waiting_time)

        # Calculate averages
        hourly_averages = {}
        for hour in sorted(hour_buckets.keys()):
            times = hour_buckets[hour]
            avg = statistics.mean(times)
            hourly_averages[hour] = avg

        return hourly_averages