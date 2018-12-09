from test_common import *

############################################################################
# TESTS FOR VERSION 1.1.0
############################################################################

# Windows: Success
def test_register_sensor_1_1_kettle(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50101))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle", ' \
              b'"id":"kettle1", "status":"online", "kettle_state":"off", "temperature": 0}}'
    sock.send(message)

    time.sleep(2)
    assert (1 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"kettle", ' \
              b'"id":"kettle1", "status":"online", "kettle_state":"off", "temperature": 0}}'
    sock.send(message)

    monitor_default.stop(timeout=0)

# Windows: Success
def test_register_sensor_1_1_router(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50102))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router",' \
              b'"id":"router1", "status":"online",' \
              b'"inet_state":"online", "in_traffic":10,"out_traffic":15}}'
    sock.send(message)

    time.sleep(2)
    assert (1 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"router",' \
              b'"id":"router1", "status":"online",' \
              b'"inet_state":"online", "in_traffic":10,"out_traffic":15}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Success
def test_metrics_sensor_1_1_router_check(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50103))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router",' \
              b'"id":"router1", "status":"online",' \
              b'"inet_state":"online", "in_traffic":10,"out_traffic":15}}'
    sock.send(message)

    time.sleep(2)
    assert ('online' == MessageHandler._sensors['router1'].inet_state)
    assert (10 == MessageHandler._sensors['router1'].in_traffic)
    assert (15 == MessageHandler._sensors['router1'].out_traffic)

    message = b'{"message_type":"unregister","payload":{"type":"router",' \
              b'"id":"router1", "status":"online",' \
              b'"inet_state":"online", "in_traffic":10,"out_traffic":15}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Success
def test_register_sensor_1_1_empty_type(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50104))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"","id":"empty1"}}'
    sock.send(message)

    time.sleep(2)
    assert (0 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"","id":"empty1"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Success
def test_register_sensor_1_1_fridre(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50105))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"fridge","id":"fridge1"}}'
    sock.send(message)

    time.sleep(2)
    assert (0 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"fridge","id":"fridge1"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Success
def test_metrics_sensor_1_1_kettle_check(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50106))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle", ' \
              b'"id":"kettle1", "status":"online", "kettle_state":"off", "temperature": 0}}'
    sock.send(message)

    time.sleep(2)
    assert ('off' == MessageHandler._sensors['kettle1'].kettle_state)
    assert (0 == MessageHandler._sensors['kettle1'].temperature)

    message = b'{"message_type":"unregister","payload":{"type":"kettle", ' \
              b'"id":"kettle1", "status":"online", "kettle_state":"off", "temperature": 0}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Error
def test_update_metrics_sensor_1_1_kettle_check(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50107))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"kettle", ' \
              b'"id":"kettle1", "status":"online", "kettle_state":"off", "temperature": 0}}'
    sock.send(message)


    time.sleep(2)
    message = b'{"message_type":"update","payload":{"type":"kettle", ' \
              b'"id":"kettle1", "status":"online", "kettle_state":"on", "temperature": 50}}'
    sock.send(message)

    time.sleep(3)
    assert ('on' == MessageHandler._sensors['kettle1'].kettle_state)
    assert (50 == MessageHandler._sensors['kettle1'].temperature)

    message = b'{"message_type":"unregister","payload":{"type":"kettle", ' \
              b'"id":"kettle1", "status":"online", "kettle_state":"on", "temperature": 50}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Error
def test_update_metrics_sensor_1_1_router_check(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50108))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router",' \
              b'"id":"router1", "status":"online",' \
              b'"inet_state":"online", "in_traffic":10,"out_traffic":15}}'
    sock.send(message)

    time.sleep(2)
    message = b'{"message_type":"update","payload":{"type":"router",' \
              b'"id":"router1", "status":"online",' \
              b'"inet_state":"offline", "in_traffic":0,"out_traffic":0}}'
    sock.send(message)

    time.sleep(3)
    assert ('offline' == MessageHandler._sensors['router1'].inet_state)
    assert (0 == MessageHandler._sensors['router1'].in_traffic)
    assert (5 == MessageHandler._sensors['router1'].out_traffic)

    message = b'{"message_type":"unregister","payload":{"type":"router",' \
              b'"id":"router1", "status":"online",' \
              b'"inet_state":"online", "in_traffic":10,"out_traffic":15}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

############################################################################


############################################################################
# TESTS FOR VERSION 1.0.0
############################################################################

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