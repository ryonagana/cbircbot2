from cbircbot2.core.module_base import IrcModuleInterface
import os

import asyncio
import tornado.web
import tornado.gen
import tornado.ioloop

from cbircbot2.modules.Web.app.MainHandler import MainHandler
from cbircbot2.modules.Web.WebServerAsync import WebServerAsync
from threading import  Thread

class Web(IrcModuleInterface):
    
    def __init__(self):
        super().__init__()
        self.web = WebServerAsync()
        self.thread = None
        
    def start(self, client):
        self.thread = Thread(target=self.start_server,args=())
        self.thread.daemon = False
        self.thread.start()
        
    def end(self):
        self.thread.join()
    
    def start_server(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.web.run()