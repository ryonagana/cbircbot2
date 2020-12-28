from cbircbot2.core.module_base import IrcModuleInterface
import urllib
import json
from urllib.request import urlopen
from urllib.parse import urlencode
import os

class Weather(IrcModuleInterface):
    def __init__(self, irc=None):
        super().__init__(self, irc)
        self.irc = irc
        self.MODULE_NAME = "weather"
        self.AUTHOR = "ryonagana"
        self.DESCRIPTION = "Default Hello World!"



    def start(self, client):



        self.register_cmd("weather", self.consume_weather_api, self.CMD_PUBLIC, "Just a Test!")

    def end(self):
        pass

    def consume_weather_api(self, *args, **kwargs):




        irc = None
        if "client" in kwargs:
            irc = kwargs["client"]

        if "OPEN_WEATHER_API" not in os.environ:
            irc.msg_to_channel(irc.params.CHANNEL, "My API KEY was not set, Sorry. no weather for you")
            return

        if "data" not in kwargs:
            print("command Failed in Module: {0}".format(self.MODULE_NAME))
            return

        args = kwargs['data']['message']

        args = args.split(" ", 2)
        count = len(args) - 2

        if count == 0 or count > 1:
            irc.msg_to_channel(irc.params.CHANNEL, "Please Type City name")
            return

        api  = os.environ['OPEN_WEATHER_API']
        url = "http://api.openweathermap.org/data/2.5/weather?"


        city = args[2] #city name
        url_data = {'q': city, 'appid': api, 'units': 'metric' }

        url_data  = urllib.parse.urlencode(url_data)
        url_api = url + url_data
        consume_api = urlopen(url_api).read().decode('utf-8')
        data = json.loads(consume_api)

        name = data['name']
        temp = data['main']['temp']
        temp_max =  data['main']['temp_max']
        temp_min = data['main']['temp_min']
        humidity = data['main']['humidity']
        weather = data['weather'][0]['main']
        weather_descr = data['weather'][0]['description']
        wind_vel = data['wind']['speed']
        wind_deg = data['wind']['deg']
        msg = "{0} - {1}, {2}. Temp: {3} Max: {4} Min: {5}, Humidity: {6} Wind: {7}km/h Wind Degrees {8}".format(name, weather, weather_descr, temp, temp_max, temp_min, humidity, wind_vel, wind_deg)
        irc.msg_to_channel(irc.params.CHANNEL, msg)
