from .sensor import PassiveSensorEmulator
import asyncore
import json


class PowerSupplyHandler(asyncore.dispatcher_with_send):

    def __init__(self, p_sock):
        super().__init__(p_sock)

    def handle_read(self):
        data = self.recv(8192)
        if data:
            i_json = json.loads(data.decode('utf-8'))
            print(str(self.addr) + ': ' + str(i_json))

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_write(self):
        pass


class PowerSupply(PassiveSensorEmulator):

    def __init__(self, p_power_supply_json, host, port):
        super().__init__(p_power_supply_json, host, port, PowerSupplyHandler)

