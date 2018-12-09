from run_common import *




def worker(message_reg, message_up, message_unreg, port, du):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.connect((server, port_serv))
    time.sleep(1)
    print("I am sensor from {}".format(port))
    sock.send(message_reg)

    for i in range(10):
        time.sleep(2)
        sock.send(message_up)

    time.sleep(2)
    sock.send(message_unreg)

def perf_test(monitor_default):
    monitor_default

    count_kettle = 100
    count_router = 100
    create_sensors(count_kettle, count_router)

    time.sleep(30)

    monitor_default.stop(timeout=0)

def create_sensors(count_kettle, count_router):
    server = '127.0.0.1'
    port_serv = 50000
    begin_port_kettle = 51000
    begin_port_router = 52000
    for i in range(count_kettle):
        


if __name__ == "__main__":
    for i in range(1,2):
        t = threading.Thread(target=worker, args=(messages[i][0], messages[i][1], messages[i][2], 6605 + i, i))
        t.start()



