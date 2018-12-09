from .sensor import ActiveSensor


class Kettle(ActiveSensor):

    def __init__(self, p_kettle_json):
        super().__init__(p_kettle_json)
        self._json['type'] = 'kettle'

    def update(self, p_kettle):
        super().update(p_kettle)
        self._json['kettle_state'] = p_kettle.kettle_state
        self._json['temperature'] = p_kettle.temperature

    def check_rule(self, p_rule):
        i_expression = p_rule.format(id=self.id,
                                     type=self.type,
                                     status=self.status,
                                     address=self.address,
                                     kettle_state=self.kettle_state,
                                     temperature=self.temperature)
        print(i_expression)
        i_value = eval(i_expression)
        if i_value:
            return True
        return False

    def fill_message(self, p_message):
        return p_message.format(id=self.id,
                                type=self.type,
                                status=self.status,
                                address=self.address,
                                kettle_state=self.kettle_state,
                                temperature=self.temperature)

    @property
    def kettle_state(self):
        return self._json.get('kettle_state', 'off')

    @property
    def temperature(self):
        return self._json.get('temperature')
