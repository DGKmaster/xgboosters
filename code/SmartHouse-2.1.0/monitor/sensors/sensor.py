from datetime import datetime
import json
from ..message_service import MessageClient


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

    def check_rule(self, p_rule):
        return False

    def fill_message(self, p_message):
        return p_message.format(id=self.id,
                                type=self.type,
                                status=self.status,
                                address=self.address)

    @property
    def id(self):
        return self._json.get('id')

    @property
    def type(self):
        return self._json.get('type')

    @property
    def status(self):
        return self._json.get('status', 'unknown')

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
        self._client = MessageClient(self.address.split(':')[0], int(self.address.split(':')[1]))
        self._client.run_threaded()

    def register(self):
        i_json = {
            "message_type": "register",
            "payload": self._json
        }
        self._client.buffer = bytes(json.dumps(i_json), 'utf-8')

    def unregister(self):
        i_json = {
            "message_type": "unregister",
            "payload": {
                "id": self.id,
                "type": self.type
            }
        }
        self._client.buffer = bytes(json.dumps(i_json), 'utf-8')

    def send_update(self):
        i_json = {
            "message_type": "update",
            "payload": self._json
        }
        self._client.buffer = bytes(json.dumps(i_json), 'utf-8')
