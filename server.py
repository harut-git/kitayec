import json

from tornado import websocket
import tornado.ioloop

import server_modules


class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print "Websocket Opened"

    def on_message(self, message):
        rcv = json.loads(message)
        module_to_run = getattr(server_modules, rcv['action'])
        senden = module_to_run(rcv['params'])
        self.write_message(senden)

    def on_close(self):
        print "Websocket closed"


application = tornado.web.Application([(r"/", EchoWebSocket), ])

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()
