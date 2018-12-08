from .sensor import ActiveSensor


class Kettle(ActiveSensor):

    def __init__(self, p_kettle_json):
        super().__init__(p_kettle_json)
        self._json['type'] = 'kettle'

    @property
    def kettle_state(self):
        return self._json.get('kettle_state', 'off')

    @property
    def temperature(self):
        return self._json.get('temperature')
