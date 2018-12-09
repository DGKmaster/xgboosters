from test_common import *
import collections



############################################################################
# TESTS FOR VERSION 2.0.0
############################################################################

def test_check_notify_overheat_2_0(monitor_default):
    monitor_default

    with open('../../code/SmartHouse-2.0.0/notification.log') as infile:
        counts1 = collections.Counter(l.strip() for l in infile)

    time.sleep(0.5)
    i_kettle = Kettle({'id': 'kettle1', 'status': 'online', 'kettle_state': 'off', 'temperature': 0})
    i_kettle.register()

    i_kettle.temperature = 110
    i_kettle.send_update()

    time.sleep(2)
    with open('../../code/SmartHouse-2.0.0/notification.log') as infile:
        counts2 = collections.Counter(l.strip() for l in infile)

    assert (len(counts1) + 1 == len(counts2))

    i_kettle.unregister()
    del i_kettle

    monitor_default.stop(timeout=0.5)

############################################################################