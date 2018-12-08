from .sensor import ActiveSensor


class Router(ActiveSensor):

    def __init__(self, p_router_json):
        super().__init__(p_router_json)
        self._json['type'] = 'router'

    @property
    def inet_state(self):
        return self._json.get('inet_state', 'offline')

    @property
    def in_traffic(self):
        return self._json.get('in_traffic', 0)

    @property
    def out_traffic(self):
        return self._json.get('out_traffic', 0)
