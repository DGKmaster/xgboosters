import time
import sys
import socket
import threading
import pytest

# Add the folder path to the sys.path list
sys.path.append('../../code/SmartHouse-1.0.0/')

from monitor.monitor import MessageHandler
from monitor.monitor import Monitor
from monitor.message_service import MessageServer
from monitor.config import Config




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
        Monitor('config_test.yaml').run()

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

    sock.bind(('localhost', 50001))
    sock.set_reuse_addr()

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


def test_update_sensor(a): #error_sometimes
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('localhost', 50002))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))
    assert ('online' == MessageHandler._sensors['1'].status)

    time.sleep(12)
    assert (1 == len(MessageHandler._sensors))
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
    assert (1 == len(MessageHandler._sensors))
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
    assert (1 == len(MessageHandler._sensors))
    assert ("kettle" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)


def test_check_newtype(b): #error
    b

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50005))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("kettle" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    b.stop(timeout=0)


def test_empty_type(a): #error
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50006))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"","id":"4", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)

def test_int_type(a): #error
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50007))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"1","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"1","id":"4", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)

def test_update_unreg_sensor(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50008))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"update","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)

def test_unreg_unreg_sensor(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50009))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    a.stop(timeout=0)

def test_empty_message(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50010))
    sock.connect(('localhost', 50000))

    message = b''
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    a.stop(timeout=0)


def test_signed_id(a):
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50011))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"register","payload":{"type":"","id":"-14", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"","id":"-14", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    a.stop(timeout=0)

def test_incorrect_id(a): #error
    a

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50012))
    sock.connect(('localhost', 50000))

    message = b'gdfagadfgadfg'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    a.stop(timeout=0)


def test_double_sensosrs_(a):
    a

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.bind(('', 50013))
    sock1.connect(('localhost', 50000))

    message = b'{"message_type":"register","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock1.send(message)

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2.bind(('', 50014))
    sock2.connect(('localhost', 50000))

    message2 = b'{"message_type":"register","payload":{"type":"router","id":"5", "status":"online"}}'
    sock2.send(message2)

    time.sleep(1)
    assert (2 == len(MessageHandler._sensors))

    a.stop(timeout=0)


if __name__ == "__main__":
    test_read_config()
