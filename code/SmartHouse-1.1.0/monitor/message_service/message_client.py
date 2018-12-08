import asyncore
from threading import Thread
import json


class MessageClient(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect((host, port))
        self.buffer = b''

    def handle_accepted(self, sock, addr):
        pass

    def handle_connect(self):
        pass

    def handle_close(self):
        while self.writable() and self.connected:
            self.handle_write()
        self.close()

    def handle_read(self):
        i_data = self.recv(8192)
        if i_data:
            i_json = json.loads(i_data.decode('utf-8'))
            print(str(i_json))

    def writable(self):
        try:
            if len(self.buffer) > 0:
                return True
        except:
            pass
        return False

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    @staticmethod
    def run_threaded():
        Thread(target=asyncore.loop, args=(1, False)).start()
