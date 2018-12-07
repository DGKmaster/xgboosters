from .sensor import ActiveSensor


class Kettle(ActiveSensor):

    def __init__(self, p_kettle_json):
        super().__init__(p_kettle_json)

    @property
    def type(self):
        return 'kettle'
