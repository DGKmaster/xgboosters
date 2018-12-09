from .sensors import Kettle, Router, Fridge, PowerSupply
import time

"""
i_power_supply1 = PowerSupply({'id': 'supply1', 'status': 'online'}, 'localhost', 50001)
i_power_supply2 = PowerSupply({'id': 'supply2', 'status': 'online'}, 'localhost', 50002)
"""
i_kettle = Kettle({'id': 'kettle1', 'status': 'online', 'kettle_state': 'off', 'temperature': 0})
i_kettle.register()
time.sleep(5)
i_router = Router({'id': 'router1', 'status': 'online'})
i_router.register()
i_kettle.temperature = 110
i_kettle.send_update()
time.sleep(2)
i_kettle.kettle_state = 'boil'
i_kettle.send_update()
i_fridge = Fridge({'id': 'fridge1', 'status': 'online', 'temperature1': -2, 'temperature2': -10})
i_fridge.register()
time.sleep(3)
i_kettle.unregister()
del i_kettle
time.sleep(4)
i_router.inet_state = 'online'
i_router.send_update()
time.sleep(5)
i_router.unregister()
del i_router
time.sleep(2)
del i_fridge
"""
del i_power_supply1
del i_power_supply2
"""