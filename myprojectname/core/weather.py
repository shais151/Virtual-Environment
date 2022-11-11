import logging

from myprojectname.core.utils import get_url

log = logging.getLogger(__name__)

class weather:
    def __init__(self):
        log.info("Loaded weather")
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.validOptions = ["temperature", "precipitation", "rain", "showers", "snowfall", "windspeed"]

    def options(self, options):
        isValid = False
        return

    def get_weather(self, longitude:float, latitude:float):
        new_url = f"{self.url}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
        log.info(new_url)
        data = get_url(new_url)
        log.info("Received weather data")
        return data
