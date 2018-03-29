from os.path import dirname, join

import requests
import json

from .jarvis_error import WeatherError

LAT_LONG_LINK = 'http://freegeoip.net/json'
DARK_SKY_API_KEY = 'f9ba754fb95c8e584cfc10b6f97c600e'

class Weather():

    def __init__(self):
        lat, lon = self.get_location()

        darksky = requests.get('https://api.darksky.net/forecast/{}/{},{}'.format(DARK_SKY_API_KEY, lat, lon))
        self._weather = json.loads(darksky.text)

    def get_current_weather(self):

        # Maybe not hard code these in the future
        try:
            return self._weather['currently']['summary']
        except KeyError as error:
            raise WeatherError('Error in getting current weather', error.args)

    def get_later_weather(self):

        try:
            return self._weather['hourly']['summary']
        except KeyError as error:
            raise WeatherError('Error in getting weather for the rest of the day', error.args)

    def get_location(*args, **kwargs):
        r = requests.get(LAT_LONG_LINK)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        return lat, lon








