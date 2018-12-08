from .sensor import ActiveSensorEmulator


class Fridge(ActiveSensorEmulator):

    def __init__(self, p_fridge_json):
        super().__init__(p_fridge_json)
        self._json['type'] = 'fridge'

    @property
    def temperature1(self):
        return self._json.get('temperature1')

    @property
    def temperature2(self):
        return self._json.get('temperature2')

    @temperature1.setter
    def kettle_state(self, p_temperature):
        self._json['temperature1'] = p_temperature

    @temperature2.setter
    def temperature(self, p_temperature):
        self._json['temperature2'] = p_temperature
