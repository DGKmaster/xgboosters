from datetime import datetime


class Sensor:

    def __init__(self, p_sensor_json):
        self._json = p_sensor_json
        self._last_update = datetime.now()

    def update(self, p_sensor):
        self._last_update = datetime.now()
        self._json['status'] = p_sensor.status

    def check_status(self, p_timeout):
        i_timedelta = (datetime.now() - self._last_update)
        i_since_last = (i_timedelta.microseconds + (i_timedelta.seconds + i_timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6
        if i_since_last > p_timeout:
            self._json['status'] = 'offline'

    @property
    def id(self):
        return self._json.get('id')

    @property
    def type(self):
        return self._json.get('type')

    @property
    def status(self):
        return self._json.get('status', 'offline')

    @property
    def address(self):
        return self._json.get('address', str(('localhost', -1)))

    @address.setter
    def address(self, p_address):
        self._json['address'] = str(p_address)


class ActiveSensor(Sensor):

    def __init__(self, p_sensor_json):
        super().__init__(p_sensor_json)

    def __del__(self):
        pass


class PassiveSensor(Sensor):

    def __init__(self, p_sensor_json):
        super().__init__(p_sensor_json)
