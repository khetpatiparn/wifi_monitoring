import time
from wifi_dev_info import *

if __name__ == "__main__":
    try:
        while True:
            ssri = get_signal_STR()
            name = get_NAME()
            ap = get_AP()

            print(name, ap, ssri)

            time.sleep(2)
    except KeyboardInterrupt:
        print("end monitoring")
