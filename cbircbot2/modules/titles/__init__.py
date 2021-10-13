from cbircbot2.core.module_base import IrcModuleInterface
import requests
import re
import html
from contextlib import suppress

class titles(IrcModuleInterface):
    
    ID=1002
    MODULE_NAME="titles"
    AUTHOR="archdark"
    DESCRIPTION="any link on channel post the title"
    
    def __init__(self):
        super().__init__()
        
    def start(self, client):
        super().start(client)
    
    def _detect_protocol(self, msg):
        detect = False
        if msg.find("http://")  != -1 or msg.find("https://") != -1 :
            detect = True
        return detect
        
    def _extract_link(self, msg):
        match = re.match(r"(?:(https|http)):\/\/(?:\w{3})(\S+)?", msg, re.IGNORECASE)
        
        if not match:
            return None
        
        return match.group()
        
    def on_message(self, *args, **kwargs):
        message = kwargs["message"]
        
        if not self._detect_protocol(message):
            return
            
        link = self._extract_link(message) 
        
        if not link:
            return
        
        try:
            #blocking redirects avoid ifinite loops when a website is incorrectly redirected
            req = requests.get(link, allow_redirects=False, stream=True)
    
            if req.status_code != 200:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{req.url} Invalid Response: {req.status_code}")
                return
                
            try:
                content_type = req.headers['content-type']
                print(f"content-type: {content_type}")
                
                if content_type.find("text/html") != -1:
                    html_element = req.text
                    title = html_element[ html_element.find('<title>') + 7 : html_element.find('</title>')]
                    self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{html.unescape(title)}")
                    return
                
                elif content_type.find("image/") != -1:
                    if int(req.headers['content-length']) > 100000:
                        self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{link} took too long. aborting")
                        return
                    self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{link} is a {content_type} image")
                    return
            except IndexError:
                print(f"{req.url} has incorrect context-type")

        except requests.exceptions.Timeout:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{req.url} timed out")
        except requests.HTTPError as http:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{req.url} occurred a HTTP Exception Error: {http}")
        return
