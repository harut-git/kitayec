import json
import uuid
import tornado.ioloop
import tornado
from tornado.websocket import WebSocketHandler

import server_modules

clients = {}


class WSHandler(WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(WSHandler, self).__init__(application, request, **kwargs)
        self.client_id = str(uuid.uuid4())

    def open(self):
        if len(clients) == 4:
            self.close()
        print 'connection for client {0} opened...'.format(self.client_id)
        clients[self.client_id] = self
        self.write_message(json.dumps({'action': 'take_id',
                                       'params': {'my_id': self.client_id}
                                       }))

    def on_message(self, message):
        rcv = json.loads(message)
        module_to_run = getattr(self, rcv['action'])
        senden = module_to_run(rcv['params'])
        print senden

    def on_close(self):
        clients.pop(self.client_id, None)
        print 'connection closed...'

    def say_word(self, params):
        for i in clients:
            clients[i].write_message(json.dumps({'action': 'show_word',
                                       'params': {'value': params['value']}
                                       }))


application = tornado.web.Application([(r"/", WSHandler), ])

if __name__ == "__main__":
    application.listen(9070)
    tornado.ioloop.IOLoop.instance().start()