import asyncore
from threading import Thread


class MessageServer(asyncore.dispatcher):

    def __init__(self, host, port, handler_cls):
        asyncore.dispatcher.__init__(self)
        self.handler_cls = handler_cls
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self._opened_sockets = dict()

    def handle_accepted(self, sock, addr):
        print('handle_accepted')
        self.handler_cls(sock)

    def handle_connect(self):
        print('handle_connect')

    def handle_close(self):
        print('handle_close')
        self.close()

    def handle_read(self):
        print('handle_read')

    @staticmethod
    def run_threaded():
        Thread(target=asyncore.loop).start()
