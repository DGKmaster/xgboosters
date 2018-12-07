from .sensor import ActiveSensor, PassiveSensor
from .router import Router
from .kettle import Kettle


def instantiate_sensor(p_sensor_json):
    if 'type' in p_sensor_json:
        i_type = p_sensor_json.get('type')
        if i_type in ['kettle']:
            return Kettle(p_sensor_json)
        if i_type in ['router']:
            return Router(p_sensor_json)
    return None
