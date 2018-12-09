from test_common import *

############################################################################
# TESTS FOR VERSION 1.1.0
############################################################################



############################################################################

############################################################################
# TESTS FOR VERSION 1.0.0
############################################################################
# Windows: Success
# Linux: Success
def test_read_config_address():
    conf = Config('config.yaml')
    assert (conf.server.address == 'localhost')


# Windows: Success
# Linux: Success
def test_read_config_port():
    conf = Config('config.yaml')
    assert (conf.server.port == 50000)


# Windows: Success
# Linux: Success
def test_read_config_sensor_type():
    conf = Config('config.yaml')
    assert (conf.find_sensor_type('kettle').type == 'kettle')
    assert (conf.find_sensor_type('router').type == 'router')


# Windows: Success
# Linux: Success
def test_read_config_sensor_timeout():
    conf = Config('config.yaml')
    assert (conf.find_sensor_type('kettle').timeout == 8)
    assert (conf.find_sensor_type('router').timeout == 12)


# Windows: Success
# Linux: Success
def test_read_config_sensor_unknown_type():
    conf = Config('config.yaml')
    assert (conf.find_sensor_type('unknown') is None)


# Windows: Success
# Linux: Success
def test_read_another_config_address():
    conf = Config('config_test.yaml')
    assert (conf.server.address == '127.0.0.1')


# Windows: Success
# Linux: Success
def test_read_another_config_port():
    conf = Config('config_test.yaml')
    assert (conf.server.port == 40000)


# Windows: Success
# Linux: Success
def test_read_another_config_sensor_type():
    conf = Config('config_test.yaml')
    assert (conf.find_sensor_type('new_sensor').type == 'new_sensor')


# Windows: Error
# Linux: Error
def test_read_another_config_sensor_timeout():
    conf = Config('config_test.yaml')
    assert (conf.find_sensor_type('kettle').timeout == 2)
    assert (conf.find_sensor_type('router').timeout == 12)


# Windows: Success
# Linux: Success
def test_read_another_config_sensor_unknown_type():
    conf = Config('config_test.yaml')
    assert (conf.find_sensor_type('unknown') is None)


# Windows: Error
# Linux: Error
def test_read_config_empty_addreess_address():
    conf = Config('config_empty_address.yaml')
    assert (conf.server.address is None)


# Windows: Error
# Linux: Error
def test_read_config_empty_addreess_port():
    conf = Config('config_empty_address.yaml')
    assert (conf.server.port is None)


# Windows: Error
# Linux: Sometimes
def test_read_config_empty_addreess_type():
    conf = Config('config_empty_address.yaml')
    assert (conf.find_sensor_type('router').type == 'router')


# Windows: Error
# Linux: Sometimes
def test_read_config_empty_adreess_timeout():
    conf = Config('config_empty_address.yaml')
    assert (conf.find_sensor_type('router').timeout == 12)


# Windows: Error
# Linux: Success
def test_read_config_empty_sensors_address():
    conf = Config('config_empty_sensors.yaml')
    assert (conf.server.address == 'localhost')


# Windows: Error
# Linux: Error
def test_read_config_empty_sensors_port():
    conf = Config('config_empty_sensors.yaml')
    assert (conf.server.port == 40000)


# Windows: Error
# Linux: Error
def test_read_config_empty_sensors():
    conf = Config('config_empty_sensors.yaml')
    assert (conf.sensors is None)


# Windows: Error
# Linux: Error
def test_read_config_empty_config_address():
    conf = Config('config_empty_config.yaml')
    assert (conf.server.address is None)


# Windows: Error
# Linux: Error
def test_read_config_empty_config_port():
    conf = Config('config_empty_config.yaml')
    assert (conf.server.port is None)


# Windows: Error
# Linux: Error
def test_read_config_empty_config_sensors():
    conf = Config('config_empty_config.yaml')
    assert (conf.sensors is None)
############################################################################