import os
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("index.html")
