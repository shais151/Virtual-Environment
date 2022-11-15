import logging

from urllib.parse import quote, urlencode
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

    def get_weather(self, latitude:float = 51.5002, longitude:float = -0.1262, options:str = "temperature_2m"):
        options = self.check_options(options=options.split(","))
        if len(options) <= 0:
            return "No options provided"

        data = {"latitude": latitude, "longitude": longitude}
        query = urlencode(data, True)
        query = quote(query, safe='=&')

        new_url = f"{self.url}?latitude={latitude}&longitude={longitude}&hourly={options}"
        log.info(new_url)
        data = get_url(new_url)
        log.info("Received weather data")
        return data