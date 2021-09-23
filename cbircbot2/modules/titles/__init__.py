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
        
        with suppress(requests.exceptions.ConnectTimeout):
            req = requests.get(link, allow_redirects=False, timeout=1, stream=True)

        if req.status_code != 200:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{req.url} Invalid Response: {req.status_code}")
            return

        if int(req.headers['content-length']) > 1000000:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{link} took too long. aborting")
            return
        
        content_type = req.headers['content-type']
        
        if "text/html" not in content_type:
            if "image/jpeg" in content_type:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{link} is a JPEG image")
                return
            else:
                self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{link} is not a valid html page")
                return
        
        html_element = req.text
    
        title = html_element[ html_element.find('<title>') + 7 : html_element.find('</title>')]
        self.irc.msg_to_channel(self.irc.params.CHANNEL, f"{html.unescape(title)}")
        return
