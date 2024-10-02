from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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

#@app.route("/wifi_str")
#def wifiStrPage():
#    return render_template("index.html")

@app.route("/wifi_str_api", methods=['GET'])
def get_wifi_data():
    ssid = get_NAME()
    signal_level, bssid = get_signal_STR()
    return {"ssid": ssid, "bssid": bssid, "signal": signal_level}

# for real time
def update_data():
    while True:
        data = get_wifi_data()
        socketio.emit("wifi_data", data)
        socketio.sleep(1)

if __name__ == "__main__":
    socketio.start_background_task(target=update_data) 
    socketio.run(app, debug=True) # False if deploy
