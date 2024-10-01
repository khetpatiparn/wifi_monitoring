import subprocess
import time

def get_signal_STR():
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    for line in result.stdout.strip().split('\n'):
        if "Signal level" in line:
            signal_level = line.split("Signal level=")[1].split()[0]
        elif "Access Point" in line:
            ap = line.split("Access Point: ")[1].strip()
    return signal_level, ap

def get_NAME():
    result = subprocess.run(["nmcli", "-t", "-f", "NAME",
                            "connection", "show", "--active"],
                            capture_output=True, text=True)
    name = result.stdout.split()[0]
    return name

'''
def get_AP(): # maybe slow
    result = subprocess.run(["nmcli", "-t", "-f", "active,bssid",
                             "dev", "wifi"],capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if "yes:" in line:
            try:
                ap = line.split("yes:")[1].replace("\\","")
                return ap
            except IndexError:
                return "Access point not found"
'''

