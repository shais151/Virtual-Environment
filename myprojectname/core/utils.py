import logging
import json
from urllib.request import urlopen

log = logging.getLogger(__name__)


def get_url(url: str):
    log.info("Getting weather data")
    weather = urlopen(url)
    mybytes = weather.read()
    data = mybytes.decode("utf8")
    weather.close()
    return json.loads(data)
