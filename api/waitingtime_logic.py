from collections import defaultdict
from datetime import datetime, timedelta, timezone
import statistics

from waitingtime_store_factory import *
from ridestore import *

class WaitingTimeLogic:
    def __init__(self):
        self._ride_store = RideStore()
        self._waiting_time_store = create_waiting_time_store()

    def _group_entities_per_hour(self, theme_park, entities):
        time_zone_theme_park = self._ride_store.get_time_zone(theme_park)

        hour_buckets = defaultdict(list)
        for record in entities:
            ts = record["timestamp"].replace(tzinfo=pytz.utc)
            ts.tzinfo
            local_ts = ts.astimezone(time_zone_theme_park)
            hour = local_ts.hour
            waiting_time = int(record["waiting_time"])
            hour_buckets["{:02d}:00".format(hour)].append(waiting_time)

        return hour_buckets

    def _get_today_time_bounds(self):
        target_date = datetime.now(timezone.utc)
        start_time = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = target_date + timedelta(days=1)

        return start_time, end_time

    def get_hourly_waiting_times(self, theme_park, ride_name):
        """"Get waiting times grouped per hour"""

        start_time, end_time = self._get_today_time_bounds()

        # Request data from waiting time store
        with create_waiting_time_store() as waiting_time_store:
            entities = waiting_time_store.get_all_ride_waiting_times(theme_park, ride_name, start_time, end_time)

        hour_buckets = self._group_entities_per_hour(theme_park, entities)

        return hour_buckets

    def get_hourly_waiting_time_averages(self, theme_park, ride_name):
        """"Get waiting times averages grouped per hour"""

        start_time, end_time = self._get_today_time_bounds()

        # Request data from azure database
        with create_waiting_time_store() as waiting_time_store:
            entities = waiting_time_store.get_all_ride_waiting_times(theme_park, ride_name, start_time, end_time)

        # Calculate averages
        hour_buckets = self._group_entities_per_hour(theme_park, entities)
        hourly_averages = {}
        for hour in sorted(hour_buckets.keys()):
            times = hour_buckets[hour]
            avg = statistics.mean(times)
            hourly_averages[hour] = avg

        return hourly_averages