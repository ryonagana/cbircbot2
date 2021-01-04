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


    def temp(self, val):
        return "{v} Celsius".format(v=val)

    def speed(self, val):
        return "{v} km/h".format(v=val)

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
        temp =  self.temp(data['main']['temp'])
        temp_max = self.temp(data['main']['temp_max'])
        temp_min = self.temp(data['main']['temp_min'])
        humidity = data['main']['humidity']
        weather = data['weather'][0]['main']
        weather_descr = data['weather'][0]['description']
        wind_vel = self.speed(data['wind']['speed'])
        wind_deg = data['wind']['deg'] + 'degrees'
        country = data['sys']['country']
        msg = "{city_name} - {country}, Weather:{weather} - {weather_descr}  Temp: {temp}, Min: {min} Max: {max}, Humidity: {humidity}, Wind Speed: {speed}, Wind Degrees: {deg}".format(city_name=name,
                                                                                                                                                                                         weather=weather,
                                                                                                                                                                                         weather_descr=weather_descr,
                                                                                                                                                                                         country=country,
                                                                                                                                                                                         temp=temp,
                                                                                                                                                                                         min=temp_min,
                                                                                                                                                                                         max=temp_max,
                                                                                                                                                                                         humidity=humidity,
                                                                                                                                                                                         speed=wind_vel,
                                                                                                                                                                                         deg=wind_deg
                                                                                                                                                                                         )
        irc.msg_to_channel(irc.params.CHANNEL, msg)
