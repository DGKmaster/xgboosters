import time
import sys
import socket
import threading
import pytest

# Add the folder path to the sys.path list
sys.path.append('../../code/SmartHouse-1.0.0/')

from monitor.monitor import MessageHandler
from monitor.monitor import Monitor
from monitor.message_service import MessageServer
from monitor.config import Config


# Create monitor_default from config.yaml
class MonitorDefaultThread(object):
    def __init__(self):
        self._thread_a = threading.Thread(target=self.run_wrapper)
        self._thread_a.daemon = True
        self._thread_a.start()

    def run_wrapper(self):
        Monitor('config.yaml').run()

    def stop(self, timeout):
        self._thread_a.join(timeout)


# Create monitor_default from config_test.yaml
class MonitorTestThread(object):
    def __init__(self):
        self._thread_a = threading.Thread(target=self.run_wrapper)
        self._thread_a.daemon = True
        self._thread_a.start()

    def run_wrapper(self):
        Monitor('config_test.yaml').run()

    def stop(self, timeout):
        self._thread_a.join(timeout)


@pytest.fixture()
def monitor_default():
    return MonitorDefaultThread()


@pytest.fixture()
def monitor_test():
    return MonitorTestThread()
