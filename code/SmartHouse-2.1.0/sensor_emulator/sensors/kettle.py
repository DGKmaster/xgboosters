from .sensor import ActiveSensorEmulator


class Kettle(ActiveSensorEmulator):

    def __init__(self, p_kettle_json):
        super().__init__(p_kettle_json)
        self._json['type'] = 'kettle'

    @property
    def kettle_state(self):
        return self._json.get('kettle_state', 'off')

    @property
    def temperature(self):
        return self._json.get('temperature')

    @kettle_state.setter
    def kettle_state(self, p_kettle_state):
        self._json['kettle_state'] = p_kettle_state

    @temperature.setter
    def temperature(self, p_temperature):
        self._json['temperature'] = p_temperature
