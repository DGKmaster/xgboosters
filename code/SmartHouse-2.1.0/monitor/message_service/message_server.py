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
        self.handler_cls(sock)

    def handle_connect(self):
        pass

    def handle_close(self):
        while self.writable():
            self.handle_write()
        self.close()

    def handle_read(self):
        pass

    @staticmethod
    def run_threaded():
        Thread(target=asyncore.loop, args=(1, True)).start()
