from test_common import *

############################################################################
# TESTS FOR VERSION 2.0.0
############################################################################

def test_check_notify_inet_state_2_0(monitor_default):
    monitor_default

    with open('notification.log') as infile:
        counts1 = collections.Counter(l.strip() for l in infile)

    i_router = Router({'id': 'router1', 'status': 'online'})
    i_router.register()

    time.sleep(1)
    i_router.inet_state = 'online'
    i_router.send_update()

    time.sleep(1)
    with open('notification.log') as infile:
        counts2 = collections.Counter(l.strip() for l in infile)

    assert (len(counts1) + 1 == len(counts2))

    i_router.unregister()
    del i_router

    monitor_default.stop(timeout=0)

def test_check_notify_overheat_2_0(monitor_default):
    monitor_default

    with open('notification.log') as infile:
        counts1 = collections.Counter(l.strip() for l in infile)

    i_kettle = Kettle({'id': 'kettle1', 'status': 'online', 'kettle_state': 'off', 'temperature': 0})
    i_kettle.register()

    time.sleep(1)
    i_kettle.temperature = 110
    i_kettle.send_update()

    time.sleep(1)
    with open('notification.log') as infile:
        counts2 = collections.Counter(l.strip() for l in infile)

    assert (len(counts1) + 1 == len(counts2))

    i_kettle.unregister()
    del i_kettle

    monitor_default.stop(timeout=0)

def test_check_notify_boil_2_0(monitor_default):
    monitor_default

    with open('notification.log') as infile:
        counts1 = collections.Counter(l.strip() for l in infile)

    i_kettle = Kettle({'id': 'kettle1', 'status': 'online', 'kettle_state': 'off', 'temperature': 0})
    i_kettle.register()

    time.sleep(1)
    i_kettle.kettle_state = 'boil'
    i_kettle.send_update()

    time.sleep(1)
    with open('notification.log') as infile:
        counts2 = collections.Counter(l.strip() for l in infile)

    assert (len(counts1) + 1 == len(counts2))

    i_kettle.unregister()
    del i_kettle

    monitor_default.stop(timeout=0)


############################################################################