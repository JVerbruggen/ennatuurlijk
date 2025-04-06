from common import *

from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime
from requests import get

BASE_URL_LOOOPINGS = "https://www.looopings.nl/wachten/"

class RideNotFoundException(Exception):
    """Ride was not found"""

    def __init__(self, ride_name):
        super().__init__(f"Ride '{ride_name}' was not found")
        self.ride_name = ride_name

@dataclass
class RawLooopingsWaitingTimeItem:
    """Waiting time fetched from looopings"""
    theme_park: ThemeParkEnum
    ride_name: str
    waiting_time: str
    ride_state: str

class LooopingsScraper(WaitingTimeSource):
    """Web scraper for waiting times on looopings"""

    def _fetch_raw_waiting_times(self, theme_park_enum: ThemeParkEnum):
        theme_park_enum_str = ThemeParkEnum.get_looopings_str(theme_park_enum)

        URL     = BASE_URL_LOOOPINGS + theme_park_enum_str
        page    = get(URL)
        soup    = BeautifulSoup(page.content, "html.parser")

        ride_table          = soup.find(id="rides").find("tbody")
        ride_table_items    = ride_table.find_all("tr")

        raw_waiting_time_item_list = []

        for ride_table_item in ride_table_items:
            ride_name = ride_table_item.find("td", class_="name").text.strip()
            waiting_time = ride_table_item.find("td", class_="waittime").text.strip()
            ride_state = ride_table_item.find("td", class_="state").text.strip()

            raw_waiting_time_item = RawLooopingsWaitingTimeItem(theme_park_enum, ride_name, waiting_time, ride_state)
            raw_waiting_time_item_list += [raw_waiting_time_item]

        return raw_waiting_time_item_list

    def _get_waiting_time(self, raw_waiting_time: str):
        waiting_time = -1

        if raw_waiting_time.isdigit():
            waiting_time = int(raw_waiting_time)

        return waiting_time

    def _get_ride_state(self, raw_state: str):
        ride_state_map = {
            "Open": RideState.OPEN,
            "Gesloten": RideState.CLOSED,
            "Storing": RideState.BROKEN,
            "Onderhoud": RideState.MAINTENANCE
        }

        ride_state = None
        if raw_state in ride_state_map:
            ride_state = ride_state_map[raw_state]

        return ride_state

    def _normalize_ride_name(self, ride_name: str):
        normalize_map = {
            "Anton Pieck Plein (carrousels)": "anton-pieck-plein",
            "Archipel": "archipel",
            "Baron 1898": "baron-1898",
            "Carnaval Festival": "carnaval-festival",
            "Danse Macabre": "danse-macabre",
            "De Vliegende Hollander": "de-vliegende-hollander",
            "De zes Zwanen Rondvaart": "de-zes-zwanen",
            "Diorama": "diorama",
            "De Oude Tufferbaan": "de-oude-tufferbaan",
            "Droomvlucht": "droomvlucht",
            "Efteling Museum": "efteling-museum",
            "Fabula": "fabula",
            "Fata Morgana": "fata-morgana",
            "Gondoletta": "gondoletta",
            "Halve Maen": "halve-maen",
            "Joris en de Draak": "joris-en-de-draak",
            "Kinderspoor": "kinderspoor",
            "Kindervreugd": "kindervreugd",
            "Kleuterhof": "kleuterhof",
            "Max & Moritz": "max-moritz",
            "Pagode": "pagode",
            "PiraÃ±a": "pirana",
            "Python": "python",
            "Sirocco": "sirocco",
            "Nest!": "nest",
            "Sprookjesbos": "sprookjesbos",
            "Stoomcarrousel": "stoomcarrousel",
            "Stoomtrein Marerijk": "stoomtrein-marerijk",
            "Stoomtrein Ruigrijk": "stoomtrein-ruigrijk",
            "Symbolica": "symbolica",
            "Villa Volta": "villa-volta",
            "Virtuele Droomvlucht": "virtuele-droomvlucht",
            "Vogel Rok": "vogel-rok",
            "Volk van Laaf (Monorail)": "volk-van-laaf"
        }

        if ride_name not in normalize_map:
            raise RideNotFoundException(ride_name)

        return normalize_map[ride_name]

    def _can_be_ignored(self, ride_name):
        """An explicit ignore list for rides that should be discarded during processing"""

        return ride_name in [
            "Baron 1898 Single-rider",
            "Danse Macabre Single Rider",
            "De Vliegende Hollander Single-rider",
            "Joris en de Draak Single-rider",
            "Max & Moritz Single-rider",
            "Python Single-rider",
            "Symbolica Single-rider",
            "Volk van Laaf"
        ]

    def _process_raw_waiting_times(self, raw_waiting_time_item_list: list[RawLooopingsWaitingTimeItem]):
        waiting_time_item_list = []

        for raw_waiting_time_item in raw_waiting_time_item_list:
            try:
                normalized_ride_name    = self._normalize_ride_name(raw_waiting_time_item.ride_name)
            except RideNotFoundException as err:
                if self._can_be_ignored(raw_waiting_time_item.ride_name):
                    continue
                else:
                    ScraperLogger().log_error(f"Ride unknown: '{err.ride_name}'")

            waiting_time    = self._get_waiting_time(raw_waiting_time_item.waiting_time)
            ride_state      = self._get_ride_state(raw_waiting_time_item.ride_state)
            timestamp       = datetime.now().isoformat()

            waiting_time_item = WaitingTimeItem(theme_park=raw_waiting_time_item.theme_park,
                                                ride_name=normalized_ride_name,
                                                waiting_time=waiting_time,
                                                ride_state=ride_state,
                                                timestamp=timestamp)
            waiting_time_item_list += [waiting_time_item]

        return waiting_time_item_list

    def get_current_waiting_times(self, theme_park_enum: ThemeParkEnum) -> list[WaitingTimeItem]:
        # Retrieve raw waiting times from Looopings
        raw_waiting_time_item_list = self._fetch_raw_waiting_times(theme_park_enum)

        # Process waiting times into common format
        waiting_time_item_list = self._process_raw_waiting_times(raw_waiting_time_item_list)

        return waiting_time_item_list
