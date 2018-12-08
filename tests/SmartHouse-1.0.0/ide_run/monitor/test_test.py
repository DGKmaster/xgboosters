from config import Config
from message_service import MessageServer
from monitor import MessageHandler


def test_read_config():
    conf = Config('config.yaml')
    assert (conf.server.address == 'localhost')
    assert (conf.server.port == 50000)

def test_make_server():
    conf = Config('config.yaml')
    server = MessageServer(conf.server.address,
                            conf.server.port,
                            MessageHandler)
    assert (server.addr[0] == 'localhost')
    assert (server.addr[1] == 50000)


if __name__ == "__main__":
    test_read_config()
    test_make_server()
