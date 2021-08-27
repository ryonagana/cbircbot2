from cbircbot2.core.module_base import IrcModuleInterface
import os

import asyncio
import tornado.web
import tornado.gen
import tornado.ioloop
from cbircbot2.modules.Web.app.MainHandler import MainHandler


STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template")

class WebServerAsync(object):
    def __init__(self):
        self.app = None
        self.server = None
    
    def run(self):
        self.app = tornado.web.Application([
            (r"/", MainHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': STATIC_PATH})
        ],
                                           template_path=TEMPLATE_PATH,
                                           static_path=STATIC_PATH,
                                           xsrf_cookies=True,
                                           debug=True,
    
                                           )
    
       
    
        #self.server = tornado.web.HTTPServer(self.app)
        #self.server.bind(8888)
        #self.server.start(0)
        
        print(TEMPLATE_PATH)
        print(STATIC_PATH)
        
        self.app.listen(8888)
        tornado.ioloop.IOLoop.current().start()