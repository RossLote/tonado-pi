import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado
import os
import json
from RPi import GPIO as pi


PINS = [4, 17, 27, 22]

pi.setmode(pi.BCM)
for pin in PINS:
    pi.setup(pin, pi.OUT)

FORWARD_RIGHT_PIN = pi.PWM(PINS[0], 100)
FORWARD_LEFT_PIN = pi.PWM(PINS[1], 100)
BACKWARD_RIGHT_PIN = pi.PWM(PINS[2], 100)
BACKWARD_LEFT_PIN = pi.PWM(PINS[3], 100)

FORWARD_RIGHT_PIN.start(0)
FORWARD_LEFT_PIN.start(0)
BACKWARD_RIGHT_PIN.start(0)
BACKWARD_LEFT_PIN.start(0)

def updatePins(left, right):

    if right > 0:
        FORWARD_RIGHT_PIN.ChangeDutyCycle(abs(right))
        BACKWARD_RIGHT_PIN.ChangeDutyCycle(0)

    elif right < 0:
        FORWARD_RIGHT_PIN.ChangeDutyCycle(0)
        BACKWARD_RIGHT_PIN.ChangeDutyCycle(abs(right))

    else:
        FORWARD_RIGHT_PIN.ChangeDutyCycle(0)
        BACKWARD_RIGHT_PIN.ChangeDutyCycle(0)

    if left > 0:
        FORWARD_RIGHT_PIN.ChangeDutyCycle(abs(left))
        BACKWARD_RIGHT_PIN.ChangeDutyCycle(0)

    elif left < 0:
        FORWARD_RIGHT_PIN.ChangeDutyCycle(0)
        BACKWARD_RIGHT_PIN.ChangeDutyCycle(abs(left))

    else:
        FORWARD_RIGHT_PIN.ChangeDutyCycle(0)
        BACKWARD_RIGHT_PIN.ChangeDutyCycle(0)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class RCWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        data = json.loads(message)
        updatePins(data['left'], data['right'])

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
