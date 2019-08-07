"""Test the behavior of the OpenWeather API"""
import responses

from .models import WeatherApi

weather = WeatherApi()

class TestWeatherApi:

    @responses.activate
    def test_get_weather(self):
        '''
        Test behavior of get_weather method when receiving a valid set of data
        '''

        responses.add(responses.GET, "http://api.openweathermap.org/data/2.5/weather?",
                      json={'coord': {'lon': 12.32, 'lat': 45.44}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}, {'id': 200, 'main': 'Thunderstorm', 'description': 'thunderstorm with light rain', 'icon': '11d'}], 'base': 'stations', 'main': {'temp': 295.19, 'pressure': 1011, 'humidity': 78, 'temp_min': 292.04, 'temp_max': 299.26}, 'visibility': 10000, 'wind': {'speed': 5.7, 'deg': 30}, 'clouds': {'all': 40}, 'dt': 1564733948, 'sys': {'type': 1, 'id': 6779, 'message': 0.0083, 'country': 'IT', 'sunrise': 1564718121, 'sunset': 1564771113}, 'timezone': 7200, 'id': 3167663, 'name': 'Sestière di Santa Croce', 'cod': 200},
                      status=200)
        assert weather.get_weather({"lat":45.44,"lon":12.32}) is not None

    @responses.activate
    def test_get_weather_error(self):
        '''
        Test behavior of get_weather method when receiving an invalid set of data
        '''

        responses.add(responses.GET, "http://api.openweathermap.org/data/2.5/weather?",
                      json={'error':'no output'}, status=200)

        assert weather.get_weather({"lat":45.44,"lon":12.32}) is None