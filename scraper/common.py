from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ScraperLogger(metaclass=Singleton):
    def log_error(self, message):
        print(message)

class Serializer:
    @staticmethod
    def custom_serializer(obj):
        if isinstance(obj, RideState):
            return RideState.get_serializable(obj)
        elif isinstance(obj, ThemeParkEnum):
            return ThemeParkEnum.get_serializable(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

class RideState(Enum):
    OPEN = 1
    CLOSED = 2
    BROKEN = 3
    MAINTENANCE = 4

    @staticmethod
    def get_serializable(ride_state_enum):
        return {
            RideState.OPEN: "OPEN",
            RideState.CLOSED: "CLOSED",
            RideState.BROKEN: "BROKEN",
            RideState.MAINTENANCE: "MAINTENANCE",
        }[ride_state_enum]

class ThemeParkEnum(Enum):
    EFTELING = 1
    DISNEY_PARIS = 2

    @staticmethod
    def get_serializable(theme_park_enum):
        return ThemeParkEnum.get_looopings_str(theme_park_enum)

    @staticmethod
    def get_looopings_str(theme_park_enum):
        return {
            ThemeParkEnum.EFTELING:         "efteling",
            ThemeParkEnum.DISNEY_PARIS:     "disneyland"
        }[theme_park_enum]

@dataclass
class SerializedWaitingTimeItem:
    """Serialized waiting time"""
    theme_park: str
    ride_name: str
    waiting_time: int
    ride_state: str
    timestamp: str

@dataclass
class WaitingTimeItem:
    """Processed waiting time"""
    theme_park: ThemeParkEnum
    ride_name: str
    waiting_time: int
    ride_state: RideState
    timestamp: str

class WaitingTimeSource:
    """Interface for a source capable of retrieving current waiting times"""

    def get_current_waiting_times(theme_park_enum: ThemeParkEnum) -> list[WaitingTimeItem]:
        """Retrieve all current waiting times for a theme park"""

        raise NotImplementedError
