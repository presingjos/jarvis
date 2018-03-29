from .get_weather import Weather
from .check_internet_connection import have_internet

if have_internet():
    weather = Weather()
    current = weather.get_current_weather()
    later_today = weather.get_later_weather()
