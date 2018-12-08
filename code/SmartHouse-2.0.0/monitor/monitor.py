from .config import Config
import time
import os
import json
import asyncore

from .message_service import MessageServer
from .sensors import instantiate_sensor
from .notifier import Notifier


class MessageHandler(asyncore.dispatcher_with_send):

    _sockets = dict()
    _sensors = dict()

    def __init__(self, p_sock):
        super().__init__(p_sock)
        MessageHandler._sockets[str(self.addr)] = self
        self._notifier = Notifier(Monitor.config.notification_file)

    def handle_read(self):
        print('handler handle_read')
        data = self.recv(8192)
        if data:
            i_json = json.loads(data.decode('utf-8'))
            i_message_type = i_json.get('message_type', 'unknown')
            i_payload = i_json.get('payload', dict())
            if i_message_type == 'register':
                i_sensor = instantiate_sensor(i_payload)
                if i_sensor is not None and i_sensor.type in [x.type for x in Monitor.config.sensors]:
                    i_sensor.address = self.addr
                    MessageHandler._sensors[i_sensor.id] = i_sensor
                    for i_notification in Monitor.config.find_sensor_type(i_sensor.type).notifications:
                        self._notifier.process_notification(i_notification, i_sensor)
            elif i_message_type == 'unregister':
                i_sensor = instantiate_sensor(i_payload)
                if i_sensor is not None:
                    del MessageHandler._sensors[i_sensor.id]
            elif i_message_type == 'update':
                i_sensor = instantiate_sensor(i_payload)
                if i_sensor is not None:
                    MessageHandler._sensors[i_sensor.id].update(i_sensor)
                    for i_notification in Monitor.config.find_sensor_type(i_sensor.type).notifications:
                        self._notifier.process_notification(i_notification, i_sensor)
            else:
                self.send(json.dumps({'message_type': 'error', 'payload': {'text': 'Undefined message type'}}))
            print(str(self.addr) + ': ' + str(i_json))

    def handle_connect(self):
        print('handler handle_connect')

    def handle_close(self):
        print('handler handle_close')
        for k, v in MessageHandler._sensors.items():
            if v.address == str(self.addr):
                del MessageHandler._sensors[k]
        del MessageHandler._sockets[str(self.addr)]
        self.close()

    def handle_write(self):
        print('handler handle_write')


class Monitor:

    config = None

    def __init__(self, p_config_name):
        Monitor.config = Config(p_config_name)
        self._server = MessageServer(Monitor.config.server.address,
                                     Monitor.config.server.port,
                                     MessageHandler)

    def register_sensors(self):
        pass

    def examine_sensors(self):
        pass

    def check_statuses(self):
        for i_id, i_sensor in MessageHandler._sensors.items():
            i_timeout = Monitor.config.find_sensor_type(i_sensor.type).timeout
            i_sensor.check_status(i_timeout)

    def print_sensors(self):
        print("-{sensor:-<20s}-{type:-<20s}-{address:-<20s}-{status:-<20s}-".format(sensor='', type='', address='', status=''))
        print("|{sensor:^20s}|{type:^20s}|{address:^20s}|{status:^20s}|".format(sensor='ID', type='TYPE', address='ADDRESS', status='STATUS'))
        print("-{sensor:-<20s}-{type:-<20s}-{address:-<20s}-{status:-<20s}-".format(sensor='', type='', address='', status=''))
        for i_id, i_sensor in MessageHandler._sensors.items():
            print("|{sensor:<20s}|{type:<20s}|{address:<20s}|{status:<20s}|".format(sensor=i_id, type=i_sensor.type, address=i_sensor.address, status=i_sensor.status))
        print("-{sensor:-<20s}-{type:-<20s}-{address:-<20s}-{status:-<20s}-".format(sensor='', type='', address='', status=''))

    def run(self):
        self._server.run_threaded()
        try:
            while True:
                # register sensor
                self.register_sensors()
                # examine all sensors
                self.examine_sensors()
                # check statuses
                self.check_statuses()
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Running...')
                # print sensor info
                self.print_sensors()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            pass

    def process_request(self, p_data):
        print('request processing')
        print(p_data)

    @staticmethod
    def main(args=None):
        Monitor(args.config).run()
        return 0
