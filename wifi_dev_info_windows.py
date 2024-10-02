from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/wifi_str_api", methods=['GET'])
def get_wifi_data():
    result = subprocess.run(["netsh", "wlan", "show", "interface"], capture_output=True, text=True)

    ssid_pattern = re.search(r"^\s*SSID\s*:\s*(.+)$", result.stdout, re.MULTILINE)
    ap_pattern = re.search(r"^\s*BSSID\s*:\s*(.+)$", result.stdout, re.MULTILINE)
    signal_pattern = re.search(r"^\s*Signal\s*:\s*(\d+)%", result.stdout, re.MULTILINE)

    ssid = ssid_pattern.group(1) if ssid_pattern else "Unknown"
    ap = ap_pattern.group(1) if ap_pattern else "Unknown"
    signal_level = signal_pattern.group(1) if signal_pattern else "Unknown"
    return {"ssid": ssid, "bssid": ap, "signal": signal_level}

# for real time
def update_data():
    while True:
        data = get_wifi_data()
        socketio.emit("wifi_data", data)
        socketio.sleep(1)

@app.route("/wifi_str")
def wifiStrPage():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.start_background_task(target=update_data)
    socketio.run(app, debug=True)
