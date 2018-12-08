import pytest
import argparse
import sys
from config import Config


def test_read_config():
    conf = Config('config.yaml')
    assert (conf.server.address == 'localhost')
    assert (conf.server.port == 50000)


if __name__ == "__main__":
    test_read_config()
