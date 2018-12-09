from .sensor import ActiveSensor


class Router(ActiveSensor):

    def __init__(self, p_router_json):
        super().__init__(p_router_json)
        self._json['type'] = 'router'

    def update(self, p_router):
        super().update(p_router)
        self._json['inet_state'] = p_router.inet_state
        self._json['in_traffic'] = p_router.in_traffic
        self._json['out_traffic'] = p_router.out_traffic

    def check_rule(self, p_rule):
        i_expression = p_rule.format(id=self.id,
                                     type=self.type,
                                     status=self.status,
                                     address=self.address,
                                     inet_state=self.inet_state,
                                     in_traffic=self.in_traffic,
                                     out_traffic=self.out_traffic)
        i_value = eval(i_expression)
        if i_value:
            return True
        return False

    def fill_message(self, p_message):
        return p_message.format(id=self.id,
                                type=self.type,
                                status=self.status,
                                address=self.address,
                                inet_state=self.inet_state,
                                in_traffic=self.in_traffic,
                                out_traffic=self.out_traffic)

    @property
    def inet_state(self):
        return self._json.get('inet_state', 'offline')

    @property
    def in_traffic(self):
        return self._json.get('in_traffic', 0)

    @property
    def out_traffic(self):
        return self._json.get('out_traffic', 0)
