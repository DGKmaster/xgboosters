from test_common import *




def worker(message_reg, message_up, message_unreg, port, server, port_server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.connect((server, port_server))
    time.sleep(1)
    print("I am sensor from {}".format(port))
    sock.send(message_reg)

    for i in range(10):
        time.sleep(2)
        sock.send(message_up)

    time.sleep(2)
    sock.send(message_unreg)

def test_perf(monitor_default):
    monitor_default

    count_kettle = 100
    count_router = 100
    create_sensors(count_kettle, count_router)

    time.sleep(10)
    assert (200 == len(MessageHandler._sensors))

    time.sleep(20)

    monitor_default.stop(timeout=0)

def create_sensors(count_kettle, count_router):
    server = 'localhost'
    port_serv = 50000
    begin_port_kettle = 51000
    begin_port_router = 52000

    for i in range(count_kettle):
        index = str(i)
        message1 = b'{"message_type":"register","payload":{"type":"kettle","id":"ketle'+bytes (48 + i)+b'", "status":"online"}}'
        message2 = b'{"message_type":"update","payload":{"type":"kettle","id":"ketle'+bytes (48 + i)+b'", "status":"online"}}'
        message3 = b'{"message_type":"unregister","payload":{"type":"kettle","id":"ketle'+bytes (48 + i)+b'", "status":"online"}}'
        t = threading.Thread(target=worker, args=(message1, message2, message3, begin_port_kettle + i, server, port_serv))
        t.start()

    for i in range(count_router):
        message1 = b'{"message_type":"register","payload":{"type":"router","id":"router'+bytes (48 + i)+b'", "status":"online"}}'
        message2 = b'{"message_type":"update","payload":{"type":"router","id":"router'+bytes (48 + i)+b'", "status":"online"}}'
        message3 = b'{"message_type":"unregister","payload":{"type":"router","id":"router'+bytes (48 + i)+b'", "status":"online"}}'
        t = threading.Thread(target=worker, args=(message1, message2, message3, begin_port_router + i, server, port_serv))
        t.start()




