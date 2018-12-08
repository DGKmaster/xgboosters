import time
import sys
import socket
import threading
import pytest

from monitor.monitor import MessageHandler
from monitor.monitor import Monitor
from monitor.message_service import MessageServer
from monitor.config import Config

# Add the folder path to the sys.path list
sys.path.append('../../code/SmartHouse-1.0.0/')


def test_read_config():
    conf = Config('config.yaml')
    assert (conf.server.address == 'localhost')
    assert (conf.server.port == 50000)
    assert (conf.find_sensor_type('kettle').type == 'kettle')
    assert (conf.find_sensor_type('router').type == 'router')
    assert (conf.find_sensor_type('kettle').timeout == 8)
    assert (conf.find_sensor_type('router').timeout == 12)
    assert (conf.find_sensor_type('unknown') is None)


def test_read_config_another():
    conf = Config('config_test.yaml')
    assert (conf.server.address == '127.0.0.1')
    assert (conf.server.port == 40000)
    assert (conf.find_sensor_type('new_sensor').type == 'new_sensor')
    assert (conf.find_sensor_type('new_sensor').timeout == 2)
    assert (conf.find_sensor_type('router').timeout == 12)


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


class A(object):
    def __init__(self):
        self._thread_a = threading.Thread(target=self.do_a)
        self._thread_a.daemon = True
        self._thread_a.start()

    def do_a(self):
        Monitor('config.yaml').run()

    def stop(self, timeout):
        self._thread_a.join(timeout)


class B(object):
    def __init__(self):
        self._thread_a = threading.Thread(target=self.do_a)
        self._thread_a.daemon = True
        self._thread_a.start()

    def do_a(self):
        Monitor('config_test_another_sensor.yaml').run()

    def stop(self, timeout):
        self._thread_a.join(timeout)


@pytest.fixture()
def a():
    return A()


@pytest.fixture()
def b():
    _tester = B()
    return _tester


def test_make_sensor(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # sock.bind(('localhost', 50001))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    a.stop(timeout=0)

    pass


def test_update_sensor(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('localhost', 50002))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(12)
    assert ('offline' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"update","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ('online' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)


def test_check_type_router(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50003))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"3", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("router" == MessageHandler._sensors['3'].type)

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"3", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)

    pass


def test_check_type_kettle(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50004))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("kettle" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)


def test_check_type_kettle(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50004))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("kettle" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=1)


def worker():
    Monitor('config.yaml').run()


if __name__ == "__main__":
    test_read_config()
