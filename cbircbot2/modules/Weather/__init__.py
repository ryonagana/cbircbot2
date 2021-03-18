from cbircbot2.core.module_base import IrcModuleInterface
import urllib
import json
from urllib.request import urlopen
from urllib.parse import urlencode
import os
import requests
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import ssl
import certifi

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Weather(IrcModuleInterface):

    MODULE_NAME = "weather"
    AUTHOR = "archdark"
    DESCRIPTION = "show weather using Open Weather API"
    irc = None

    def __init__(self, ):
        super().__init__()




    def start(self, client):
        self.register_cmd("get", self.consume_weather_api, self.CMD_PUBLIC, "Just a Test!")
        self.irc = client

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

        args = args.split(" ", 3)
        count = len(args) - 3

        if count == 0 or count > 1:
            irc.msg_to_channel(irc.params.CHANNEL, "Please Type City name")
            return

        api  = os.environ['OPEN_WEATHER_API']
        http = 'http://'
        if irc.params.SSL_ENABLED:
            http = 'https://'



        url = http + "api.openweathermap.org/data/2.5/weather?"

        city = args[3] #city name
        url_data = {'q': city, 'appid': api, 'units': 'metric' }

        req = None

        with requests.Session() as s:
            if irc.params.SSL_ENABLED:
                req = s.get(url, params=url_data, verify=ssl.get_default_verify_paths().cafile)
            else:
                req = s.get(url, params=url_data)

        data = json.loads(req.text)
        print(data)

        name = data['name']

        temp = "{temp}C".format(temp=data['main']['temp'])
        temp_max = "{max}C".format(max=data['main']['temp_max'])
        temp_min = "{min}C".format(min=data['main']['temp_min'])
        humidity = data['main']['humidity']
        weather = data['weather'][0]['main']
        weather_descr = data['weather'][0]['description']
        wind_vel = "{speed} km/h".format(speed=data['wind']['speed'])
        wind_deg = "{wind} deg.".format(wind=data['wind']['deg'])
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
