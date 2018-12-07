from .sensor import ActiveSensor


class Router(ActiveSensor):

    def __init__(self, p_router_json):
        super().__init__(p_router_json)

    @property
    def type(self):
        return 'router'
