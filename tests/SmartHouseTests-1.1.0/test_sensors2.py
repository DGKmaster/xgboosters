from test_common import *

############################################################################
# TESTS FOR VERSION 1.1.0
############################################################################


def test_update_metrics_sensor_1_1_router_check(monitor_default):
    monitor_default

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 50102))
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

