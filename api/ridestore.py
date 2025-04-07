import pytz

class RideStore:
    def get_known_rides(self, theme_park):
        assert theme_park == "efteling", "Only efteling is supported at the moment"

        return [
            "anton-pieck-plein",
            "archipel",
            "baron-1898",
            "carnaval-festival",
            "danse-macabre",
            "de-vliegende-hollander",
            "de-zes-zwanen",
            "diorama",
            "de-oude-tufferbaan",
            "droomvlucht",
            "efteling-museum",
            "fabula",
            "fata-morgana",
            "gondoletta",
            "halve-maen",
            "joris-en-de-draak",
            "kinderspoor",
            "kindervreugd",
            "kleuterhof",
            "max-moritz",
            "pagode",
            "pirana",
            "python",
            "sirocco",
            "nest",
            "sprookjesbos",
            "stoomcarrousel",
            "stoomtrein-marerijk",
            "stoomtrein-ruigrijk",
            "symbolica",
            "villa-volta",
            "virtuele-droomvlucht",
            "vogel-rok",
            "volk-van-laaf"]

    def get_time_zone(self, theme_park):
        time_zone_str = {
            "efteling": "Europe/Amsterdam",
            "disney": "Europe/Paris",
        }[theme_park]

        return pytz.timezone(time_zone_str)

    def get_known_theme_parks(self):
        return [
            "efteling"
        ]

    def validate_ride_name(self, theme_park, ride_name):
        return ride_name in self.get_known_rides(theme_park)

    def validate_theme_park(self, theme_park):
        return theme_park in self.get_known_theme_parks()