import socket
import threading
import time

server = '127.0.0.1'
port_serv = 50000


def worker(message_reg, message_up, message_unreg, port, du):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.connect((server, port_serv))
    time.sleep(5 + du * 2)
    print("I am Worker {}, I slept for {} seconds".format(port, 5))
    sock.send(message_reg)

    for i in range(10):
        time.sleep(10)
        sock.send(message_up)

    time.sleep(10)
    sock.send(message_unreg)


message1_1 = b'{"message_type":"register","payload":{"type":"router","id":"2", "status":"online"}}'
message1_2 = b'{"message_type":"update","payload":{"type":"router","id":"2", "status":"online"}}'
message1_3 = b'{"message_type":"unregister","payload":{"type":"router","id":"2", "status":"online"}}'


message2_1 = b'{"message_type":"register","payload":{"type":"kettle","id":7", "status":"online"}}'
message2_2 = b'{"message_type":"update","payload":{"type":"kettle","id":"7", "status":"online"}}'
message2_3 = b'{"message_type":"unregister","payload":{"type":"kettle","id":"7", "status":"online"}}'


message3_1 = b'{"message_type":"register","payload":{"type":"router","id":"4", "status":"online"}}'
message3_2 = b'{"message_type":"update","payload":{"type":"router","id":"4", "status":"online"}}'
message3_3 = b'{"message_type":"unregister","payload":{"type":"router","id":"4", "status":"online"}}'


message4_1 = b'{"message_type":"register","payload":{"type":"kettle","id":"5", "status":"online"}}'
message4_2 = b'{"message_type":"update","payload":{"type":"kettle","id":"5", "status":"online"}}'
message4_3 = b'{"message_type":"unregister","payload":{"type":"kettle","id":"5", "status":"online"}}'


message5_1 = b'{"message_type":"register","payload":{"type":"kettle","id":"6", "status":"online"}}'
message5_2 = b'{"message_type":"update","payload":{"type":"kettle","id":"6", "status":"online"}}'
message5_3 = b'{"message_type":"unregister","payload":{"type":"kettle","id":"6", "status":"online"}}'

messages = [[message1_1, message1_2, message1_3],
            [message2_1, message2_2, message2_3],
            [message3_1, message3_1, message3_3],
            [message4_1, message4_2, message4_3],
            [message5_1, message5_2, message5_3]]


if __name__ == "__main__":
    for i in range(0, 5):
        t = threading.Thread(target=worker, args=(messages[i][0], messages[i][1], messages[i][2], 6605 + i, i))
        t.start()



