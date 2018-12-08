from config import Config
from message_service import MessageServer
from monitor import MessageHandler
from monitor import Monitor
import time
import sys
import socket

import threading

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def test_read_config():
    conf = Config('config.yaml')
    assert (conf.server.address == 'localhost')
    assert (conf.server.port == 50000)

def test_make_server():
    conf = Config('config.yaml')
    server = MessageServer(conf.server.address,
                            conf.server.port,
                            MessageHandler)
    assert (server.addr[0] == 'localhost')
    assert (server.addr[1] == 50000)

    return server

def test_make_sensor():
    t = threading.Thread(target=worker, args=())
    t.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50001))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    pass

def test_update_sensor():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50002))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(9)
    assert ('offline' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"update","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ('online' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    pass


def worker():
    Monitor('config.yaml').run()

if __name__ == "__main__":
    test_read_config()
    test_make_server()
    test_make_sensor()
    test_update_sensor()
    sys.exit(0)
