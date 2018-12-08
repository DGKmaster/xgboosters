import os
import yaml


class Sensor:

    def __init__(self, p_sensor_json):
        self._json = p_sensor_json

    @property
    def type(self):
        return self._json.get('type')

    @property
    def timeout(self):
        return self._json.get('timeout', 30)


class Server:

    def __init__(self, p_server_json):
        self._json = p_server_json

    @property
    def address(self):
        return self._json.get('address', 'localhost:8080').split(':')[0]

    @property
    def port(self):
        return int(self._json.get('address', 'localhost:8080').split(':')[1])


class Config:

    def __init__(self, p_file_name):
        p_file_name = os.path.normpath(p_file_name)
        if os.path.exists(p_file_name):
            with open(p_file_name) as f:
                self._json = yaml.load(f)
        else:
            self._json = dict()

    @property
    def server(self):
        return Server(self._json.get('server', dict()))

    @property
    def sensors(self):
        return [Sensor(x) for x in self._json.get('sensors', list())]

    def find_sensor_type(self, p_type):
        for x in self.sensors:
            if x.type == p_type:
                return x
        return None
