from test_common import *

############################################################################
# TESTS FOR VERSION 1.1.0
############################################################################

############################################################################


############################################################################
# TESTS FOR VERSION 1.0.0
############################################################################
# Windows: Success
# Linux: Success
def test_check_type_router(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50006))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"3", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))
    assert ("router" == MessageHandler._sensors['3'].type)

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"3", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)

    pass


# Windows: Success
# Linux: Success
def test_check_type_kettle(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50007))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (1 == len(MessageHandler._sensors))
    assert ("kettle" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Error
# Linux: Error
def test_check_newtype(monitor_test):
    monitor_test

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50008))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("kettle" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_test.stop(timeout=0)


# Windows: Error
# Linux: Error
def test_empty_type(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50009))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Error
# Linux: Error
def test_int_type(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50010))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"1","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert ("" == MessageHandler._sensors['4'].type)

    message = b'{"message_type":"unregister","payload":{"type":"1","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Success
# Linux: Success
def test_update_unreg_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50011))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"update","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)


# Windows: Success
# Linux: Success
def test_unreg_unreg_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50012))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
############################################################################