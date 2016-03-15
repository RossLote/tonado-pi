import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado
import os
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        
        
class RCWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        test = json.loads(message)

    def on_close(self):
        print("WebSocket closed")
        

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/controller', RCWebSocket),
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()