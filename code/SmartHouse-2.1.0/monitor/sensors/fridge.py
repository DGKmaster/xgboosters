from .sensor import ActiveSensor


class Fridge(ActiveSensor):

    def __init__(self, p_fridge_json):
        super().__init__(p_fridge_json)
        self._json['type'] = 'fridge'

    def update(self, p_fridge):
        super().update(p_fridge)
        self._json['temperature1'] = p_fridge.temperature1
        self._json['temperature2'] = p_fridge.temperature2

    def check_rule(self, p_rule):
        i_expression = p_rule.format(id=self.id,
                                     type=self.type,
                                     status=self.status,
                                     address=self.address,
                                     temperature1=self.temperature1,
                                     temperature2=self.temperature2)
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
                                temperature1=self.temperature1,
                                temperature2=self.temperature2)

    @property
    def temperature1(self):
        return self._json.get('temperature1')

    @property
    def temperature2(self):
        return self._json.get('temperature2')
