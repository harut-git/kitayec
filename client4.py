import json

import websocket
import thread
import time
import sys

import client_modules


def say_word(word):
    ws.send(json.dumps({'action': 'say_word',
                        'params': {'client_id': client_modules.my_id, 'value': word}
                        }))


def on_message(ws, message):
    rcv = json.loads(message)
    module_to_run = getattr(client_modules, rcv['action'])
    senden = module_to_run(rcv['params'])
    print client_modules.my_id

def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    def run(*args):
        while True:
            time.sleep(5)
        time.sleep(1)
        ws.close()

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:9070",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
