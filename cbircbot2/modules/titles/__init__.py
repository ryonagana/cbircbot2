from cbircbot2.core.module_base import IrcModuleInterface
import requests
import re
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
        if msg.find("http://") or msg.find("https://"):
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
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{link} is invalid".format(link=link))
            return
        
            
        req = requests.get(link)
        
        if req.status_code != 200:
            self.irc.msg_to_channel(self.irc.params.CHANNEL, "{link} Invalid Response: {code}".format(code=req.status_code,link=link))
            return
            
        
        html = req.text
    
        title = html[html.find('<title>') + 7 : html.find('</title>')]       
        self.irc.msg_to_channel(self.irc.params.CHANNEL, "{title_str}".format(title_str=title))
        return
        
        
if __name__ == "__main__":
    t = titles()
    
    msg = "falae galera acessa ai http://goOOogle.com acessa ai er"
    
    extract_link = re.compile(r"(?:(https|http)):\/\/(?:\w{3})(\S+)?", re.IGNORECASE)
    match = extract_link.search(msg)
   
    
    #match = re.match(r'''(?:(http|https):\/\/(?:\S)+)?''', msg, re.IGNORECASE)
   # print(match)
    
    #protocol = match.group(2)
    #site = match.group(3)
    
    #full_site = protocol + site
    
    #print(full_site)
     
    
    #if t._detect_protocol(msg):
        #print("teste sucesso")
    #else:
    #    print("failed")  
        
   
   
      
    
    
    #req = requests.get("http://www.uol.com.br")
    #html = req.text
    
    #title = html[html.find('<title>') + 7 : html.find('</title>')]
    
    #print(title)
   
        
      
