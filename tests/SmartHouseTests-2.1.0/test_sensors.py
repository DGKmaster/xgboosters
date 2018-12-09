from test_common import *

############################################################################
# TESTS FOR VERSION 2.1.0
############################################################################

def test_register_sensor_2_1_fridge(monitor_default):
    monitor_default

    i_fridge = Fridge({'id': 'fridge1', 'status': 'online', 'temperature1': -2, 'temperature2': -10})
    i_fridge.register()

    time.sleep(2)
    assert (1 == len(MessageHandler._sensors))

    i_fridge.unregister()
    del i_fridge

    monitor_default.stop(timeout=0)

def test_metrics_sensor_2_1_fridge_check(monitor_default):
    monitor_default

    i_fridge = Fridge({'id': 'fridge1', 'status': 'online', 'temperature1': -2, 'temperature2': -10})
    i_fridge.register()

    time.sleep(1)
    assert (-2 == MessageHandler._sensors['fridge1'].temperature1)
    assert (-10 == MessageHandler._sensors['fridge1'].temperature2)

    i_fridge.unregister()
    del i_fridge

    monitor_default.stop(timeout=0)

# Windows: Error
def test_update_metrics_sensor_2_1_fridge_check(monitor_default):
    monitor_default

    monitor_default

    i_fridge = Fridge({'id': 'fridge1', 'status': 'online', 'temperature1': -2, 'temperature2': -10})
    i_fridge.register()

    time.sleep(1)
    i_fridge.temperature1 = -3
    i_fridge.temperature2 = -11
    i_fridge.send_update()

    time.sleep(1)
    assert (-3 == MessageHandler._sensors['fridge1'].temperature1)
    assert (-11 == MessageHandler._sensors['fridge1'].temperature2)

    i_fridge.unregister()
    del i_fridge

    monitor_default.stop(timeout=0)

############################################################################

############################################################################
# TESTS FOR VERSION 1.1.0
############################################################################

# Windows: Success
def test_register_sensor_1_1_kettle(monitor_default):
    monitor_default

    i_kettle = Kettle({'id': 'kettle1', 'status': 'online', 'kettle_state': 'off', 'temperature': 0})
    i_kettle.register()

    time.sleep(2)
    assert (1 == len(MessageHandler._sensors))

    i_kettle.unregister()
    del i_kettle

    monitor_default.stop(timeout=0)

# Windows: Success
def test_register_sensor_1_1_router(monitor_default):
    monitor_default

    i_router = Router({'id': 'router1', 'status': 'online'})
    i_router.register()

    time.sleep(2)
    assert (1 == len(MessageHandler._sensors))

    i_router.unregister()
    del i_router

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
    message = b'{"message_type":"register","payload":{"id":"kettle1","type":"kettle","status":"online", "kettle_state":"off", "temperature": 0}}'
    sock.send(message)

    time.sleep(1)
    assert ('off' == MessageHandler._sensors['kettle1'].kettle_state)
    assert (0 == MessageHandler._sensors['kettle1'].temperature)

    message = b'{"message_type":"unregister","payload":{"id":"kettle1","type":"kettle","status":"online", "kettle_state":"off", "temperature": 0}}'

    sock.send(message)

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Error
def test_update_metrics_sensor_1_1_kettle_check(monitor_default):
    monitor_default

    i_kettle = Kettle({'id': 'kettle1', 'status': 'online', 'kettle_state': 'off', 'temperature': 0})
    i_kettle.register()
    time.sleep(1)
    i_kettle.temperature = 110
    i_kettle.send_update()
    time.sleep(1)
    i_kettle.kettle_state = 'boil'
    i_kettle.send_update()

    time.sleep(1)
    assert ('boil' == MessageHandler._sensors['kettle1'].kettle_state)
    assert (110 == MessageHandler._sensors['kettle1'].temperature)


    i_kettle.unregister()
    del i_kettle

    monitor_default.stop(timeout=0)
    time.sleep(0.5)

# Windows: Error
def test_update_metrics_sensor_1_1_router_check(monitor_default):
    monitor_default

    i_router = Router({'id': 'router1', 'status': 'online'})
    i_router.register()

    time.sleep(1)
    i_router.inet_state = 'online'
    i_router.send_update()

    time.sleep(1)
    assert ('online' == MessageHandler._sensors['router1'].inet_state)

    i_router.unregister()
    del i_router

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



def test_check_wrong_config(monitor_test):
    monitor_test

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50008))
    sock.connect(('localhost', 50000))
    message = b'{"message_type":"register","payload":{"type":"router","id":"4", "status":"online"}}'
    sock.send(message)

    time.sleep(1)
    assert (0 == len(MessageHandler._sensors))

    message = b'{"message_type":"unregister","payload":{"type":"router","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_test.stop(timeout=0)


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


def test_update_unreg_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50011))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"update","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)



def test_unreg_unreg_sensor(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 50012))
    sock.connect(('localhost', 50000))

    message = b'{"message_type":"unregister","payload":{"type":"kettle","id":"4", "status":"online"}}'
    sock.send(message)

    monitor_default.stop(timeout=0)
############################################################################