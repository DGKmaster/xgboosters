from test_common import *


############################################################################
# TESTS FOR VERSION 1.0.0
############################################################################
# Windows: Success
# Linux: Success
def test_make_server_check_address():
    conf = Config('config.yaml')
    server = MessageServer(conf.server.address,
                           conf.server.port,
                           MessageHandler)
    assert (server.addr[0] == 'localhost')


# Windows: Success
# Linux: Error
def test_make_server_check_port():
    conf = Config('config.yaml')
    server = MessageServer(conf.server.address,
                           conf.server.port,
                           MessageHandler)
    assert (server.addr[1] == 50000)


# Windows: Success
# Linux: Success
def test_make_server_from_test_conf_check_address():
    conf = Config('config_test.yaml')
    server = MessageServer(conf.server.address,
                           conf.server.port,
                           MessageHandler)
    assert (server.addr[0] == '127.0.0.1')


# Windows: Success
# Linux: Error
def test_make_server_from_test_conf_check_port():
    conf = Config('config_test.yaml')
    server = MessageServer(conf.server.address,
                           conf.server.port,
                           MessageHandler)
    assert (server.addr[1] == 40000)
############################################################################