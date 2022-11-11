import logging

import urllib.request

log = logging.getLogger(__name__)

def get_url(url:str):
    log.info("Getting weather data")
    weather = urllib.request.urlopen(url)
    mybytes = weather.read()
    data = mybytes.decode("utf8")
    weather.close()
    return data