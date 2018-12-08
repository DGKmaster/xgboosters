from monitor.sensors import Sensor
from monitor.message_service import MessageClient, MessageServer
import json


class ActiveSensorEmulator(Sensor):

    def __init__(self, p_sensor_json):
        super().__init__(p_sensor_json)
        self._client = MessageClient('localhost', 50000)
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


class PassiveSensorEmulator(Sensor):

    def __init__(self, p_sensor_json, host, port, p_handler_cls):
        super().__init__(p_sensor_json)
        self._server = MessageServer(host, port, p_handler_cls)
        self._server.run_threaded()
