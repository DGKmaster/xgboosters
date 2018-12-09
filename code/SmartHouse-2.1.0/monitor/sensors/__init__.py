from .sensor import ActiveSensor, PassiveSensor, Sensor
from .router import Router
from .kettle import Kettle
from .fridge import Fridge


def instantiate_sensor(p_sensor_json):
    if 'type' in p_sensor_json:
        i_type = p_sensor_json.get('type')
        if i_type in ['kettle']:
            return Kettle(p_sensor_json)
        if i_type in ['router']:
            return Router(p_sensor_json)
        if i_type in ['fridge']:
            return Fridge(p_sensor_json)
        if i_type in ['passive']:
            return PassiveSensor(p_sensor_json)
        if i_type in ['active']:
            return ActiveSensor(p_sensor_json)
    return None
