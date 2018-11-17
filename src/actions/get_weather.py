from os.path import dirname, join
import time

import requests
import json
from weather import Weather, Unit


ACTION_WORDS = "weather"
SAYINGS = []


def action(jarvis):
    # Get your location
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location('boston')
    condition = location.condition
    jarvis.say(f"It is {condition.text.lower()}")
    time.sleep(1)
    return False



