class WaitingTimeStore:
    """
    Abstract Waiting Time Store.
    Uses python 'with' context
    """

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def get_all_ride_waiting_times(self, theme_park, ride_name, start_time_utc, end_time_utc):
        """Get all waiting times belonging to a ride"""

        raise NotImplementedError
