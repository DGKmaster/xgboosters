from test_common import *


# Windows: Success
def test_register_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50001))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Success
def test_unregister_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50002))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    monitor_default.stop(timeout=0)


# Windows: Success
def test_status_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('localhost', 50003))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))
    assert ('online' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Error sometimes
def test_status_from_online_to_offline_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('localhost', 50004))

    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(12)
    assert (1 == len(MessageHandler._sensors))
    assert ('offline' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"update","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ('online' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Error sometimes
def test_update_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('localhost', 50005))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(12)

    message = b'{"message_type":"update","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ('online' == MessageHandler._sensors['1'].status)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"1", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Success
def test_empty_message(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50013))
    sock.connect(('localhost', 50000))

    message = b''
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    monitor_default.stop(timeout=0)


# Windows: Success
def test_signed_register_id(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50014))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"register","payload":{"type":"","id":"-14", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"","id":"-14", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Success
def test_signed_unregister_id(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50015))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"register","payload":{"type":"","id":"-14", "status":"online"}}'
    sock.send(message)

    time.sleep(1)

    message = b'{"message_type":"unregister","payload":{"type":"","id":"-14", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    monitor_default.stop(timeout=0)


# Windows: Error
def test_incorrect_id(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50016))
    sock.connect(('localhost', 50000))

    message = b'gdfagadfgadfg'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    monitor_default.stop(timeout=0)


# Windows: Error
def test_double_sensosrs_(monitor_default):
    monitor_default

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.bind(('', 50017))
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

    monitor_default.stop(timeout=0)
