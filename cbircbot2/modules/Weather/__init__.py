from cbircbot2.core.module_base import IrcModuleInterface,  IrcCommandType
from cbircbot2.core.client import IrcClient
import urllib
import json
from urllib.request import urlopen
from urllib.parse import urlencode
import os
import requests
import ssl
import certifi



class Weather(IrcModuleInterface):

    MODULE_NAME = "weather"
    AUTHOR = "archdark"
    DESCRIPTION = "show weather using Open Weather API"
    irc = None

    def __init__(self, ):
        super().__init__()




    def start(self, client):
        self.register_cmd("get", self._run_get_weather,  IrcCommandType.CMD_PUBLIC, "Just a Test!")
        self.irc = client

    def end(self):
        pass

    
    def _run_get_weather(self, *args, **kwargs):
        irc = None
        if "client" in kwargs:
            irc = kwargs["client"]

        api: str = irc.params.OPENWEATHER_API
        print(irc.params.OPENWEATHER_API)

        if irc.params.OPENWEATHER_API == "":
            irc.msg_to_channel(irc.params.CHANNEL, "My API KEY was not set, Sorry. no weather for you")
            return
        
        if "data" not in kwargs:
            print("command Failed in Module: {0}".format(self.MODULE_NAME))
            return

        self.consume_weather_api(irc, kwargs['data']['message'], api)

    def consume_weather_api(self, irc: IrcClient, message: str, api: str) -> None:

        args = message

        args = args.split(" ", 3)
        count = len(args) - 3

        if count == 0 or count > 1:
            irc.msg_to_channel(irc.params.CHANNEL, "Please Type City name")
            return

 
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
                
        if req.status_code != 200:
            irc.msg_to_channel(irc.params.CHANNEL, f"{city} is invalid for Open Weather API")
            return
        
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
        msg = f"{name} - {country}, Weather:{weather} - {weather_descr}  Temp: {temp}," \
              f" Min: {temp_min} Max: {temp_max}, " \
              f"Humidity: {humidity}, Wind Speed: {wind_vel}, Wind Degrees: {wind_deg}"
        irc.msg_to_channel(irc.params.CHANNEL, msg)
    
    def on_message(self, *args, **kwargs):
        irc = None
        if "client" in kwargs:
            irc = kwargs["client"]
        
        if  kwargs['message'].startswith('? weather') and "get" not in kwargs['message']:
            city =  kwargs['message'].split(" ", 2)[2]
            kwargs['message'] = f"? weather get {city}"
            self.consume_weather_api(irc, kwargs['message'], irc.params.OPENWEATHER_API)
            return
        return