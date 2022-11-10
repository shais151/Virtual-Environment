import logging

log = logging.getLogger(__name__)

class weather:
    def __init__(self):
        log.info("Loaded weather")
        self.url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, longitude:float, latitude:float):
        new_url = f"{self.url}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
        log.info(new_url)