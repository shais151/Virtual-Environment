import logging

from myprojectname.core.utils import get_url

log = logging.getLogger(__name__)

class weather:
    def __init__(self):
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.validOptions = ["temperature_2m", "precipitation", "rain", "showers", "snowfall", "windspeed_10m"]
        log.info("Loaded weather")

    def check_options(self, options):
        optionlist = []
        for option in options:
            if option in self.validOptions:
                optionlist.append(option)
        return options

    def get_weather(self, latitude:float, longitude:float, options:str):
        options = self.check_options(options=options.split(","))
        if len(options) <= 0:
            return "No options provided"
        new_url = f"{self.url}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
        log.info(new_url)
        data = get_url(new_url)
        log.info("Received weather data")
        return data