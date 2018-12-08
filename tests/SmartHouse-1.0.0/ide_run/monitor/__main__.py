import argparse
import sys
from monitor import Monitor

if __name__ == "__main__":
    # Parse script arguments
    parser = argparse.ArgumentParser(description="Get scenario generator parameters.")
    parser.add_argument("-c", "--config", help="Config file name", default='config.yaml', required=False)
    args = parser.parse_args(sys.argv[1:])

    sys.exit(Monitor.main(args))
