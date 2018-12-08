from config import Config
from message_service import MessageServer
from monitor import MessageHandler
from monitor import Monitor
import time
import socket
import pytest
import threading
from multiprocessing import Process


def test_read_config():
    conf = Config('config.yaml')
    assert (conf.server.address == 'localhost')
    assert (conf.server.port == 50000)

def test_read_config_another():
    conf = Config('config_test.yaml')
    assert (conf.server.address == '127.0.0.1')
    assert (conf.server.port == 40000)

def test_make_server():
    conf = Config('config.yaml')
    server = MessageServer(conf.server.address,
                            conf.server.port,
                            MessageHandler)
    assert (server.addr[0] == 'localhost')
    assert (server.addr[1] == 50000)

    return server

def test_make_server_from_test_conf():
    conf = Config('config_test.yaml')
    server = MessageServer(conf.server.address,
                            conf.server.port,
                            MessageHandler)
    assert (server.addr[0] == '127.0.0.1')
    assert (server.addr[1] == 40000)

    return server

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

def test_make_sensor():
    trd = threading.Thread(target=worker, args=())
    stop_trd = StoppableThread(trd)
    stop_trd.start()

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

    stop_trd.stop()

    pass

def test_update_sensor():
    trd = Process(target=worker, args=())
    trd.start()

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

    trd.terminate()

def test_check_type_router():
    trd = Process(target=worker, args=())
    trd.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50003))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"3", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("router" == MessageHandler._sensors['3'].type)

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"3", "status":"online"}}'
    sock.send(message)

    trd.terminate()

    pass

def test_check_type_kettle():
    trd = Process(target=worker, args=())
    trd.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50004))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("kettle" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    trd.terminate()


def worker():
    Monitor('config.yaml').run()

if __name__ == "__main__":
    test_read_config()
