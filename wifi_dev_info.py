import subprocess
import time

def get_signal_STR():
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    for line in result.stdout.strip().split('\n'):
        if "Signal level" in line:
            signal_level = line.split("Signal level=")[1].split()[0]
            return signal_level

def get_NAME():
    result = subprocess.run(["nmcli", "-t", "-f", "NAME",
                            "connection", "show", "--active"],
                            capture_output=True, text=True)
    name = result.stdout.split()[0]
    return name

def get_AP(): # maybe slow
    result = subprocess.run(["nmcli", "-t", "-f", "active,bssid",
                             "dev", "wifi"],capture_output=True, text=True)
    ap = result.stdout.split()[0].split("yes:")[1].replace("\\","")
    return ap

