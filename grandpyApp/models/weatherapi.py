import requests
import os

class WeatherApi():
    def __init__(self):
        self.api_key = os.environ.get("WEATHERKEY")
        self.api_link = "http://api.openweathermap.org/data/2.5/weather?"

    def get_weather(self, coordinates):
        payload = {"lat":coordinates['lat'],
                   "lon":coordinates['lon'],
                   "APPID":self.api_key
        }
        raw_output = requests.get(self.api_link, params=payload)
        json_output = raw_output.json()
        try:
            temp_min = round(json_output["main"]["temp_min"]-273.15, 1)
            temp_max = round(json_output["main"]["temp_max"]-273.15, 1)
        except KeyError:
            return None

        return {
            "temp_min": temp_min,
            "temp_max": temp_max,
            "description": json_output["weather"][0]["description"]
        }
