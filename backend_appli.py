


import paho.mqtt.client as mqtt
import json
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
from influxdb_client_3 import InfluxDBClient3, Point
import os
from dotenv import load_dotenv

load_dotenv()

# --- Flask + SocketIO setup ---
app = Flask(__name__)
socketio = SocketIO(app)

# --- InfluxDB setup ---
influx = InfluxDBClient3(
    host=os.getenv("INFLUX_HOST"),
    token=os.getenv("INFLUX_TOKEN"),
    database=os.getenv("INFLUX_DATABASE")
)

# --- MQTT credentials ---
BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")


# --- Alert state ---
alert_active = False
alert_time = None

# --- MQTT callbacks ---
def on_connect(client, userdata, flags, rc):
    print("Connected to HiveMQ")
    client.subscribe("patient/#")
    client.subscribe("environment/#")
    client.subscribe("rfid/#")

def on_message(client, userdata, msg):
    global alert_active, alert_time

    topic = msg.topic
    payload = json.loads(msg.payload.decode())

    if topic == "patient/vitals":
        hr = payload["heart_rate"]
        spo2 = payload["spo2"]
        gsr = payload["gsr"]

        # write to InfluxDB
        point = Point("patient_vitals")\
            .tag("room", "room_101")\
            .field("heart_rate", hr)\
            .field("spo2", spo2)\
            .field("gsr", gsr)
        influx.write(record=point)

        # emit to dashboard
        socketio.emit("vitals", {"hr": hr, "spo2": spo2, "gsr": gsr})

        # CODE BLUE rule
        if (hr > 120 or spo2 < 90) and not alert_active:
            alert_active = True
            alert_time = datetime.now()
            print(f"CODE BLUE → HR={hr} | SpO2={spo2}%")
            socketio.emit("alert", {"type": "CODE_BLUE", "hr": hr, "spo2": spo2})

        elif alert_active and hr <= 120 and spo2 >= 90:
            duration = (datetime.now() - alert_time).seconds
            print(f"Patient stabilized after {duration}s")
            alert_active = False
            alert_time = None
            socketio.emit("stabilized", {"duration": duration})

        # stress rule
        if gsr > 0.85:
            print(f"High stress → GSR={gsr}")
            socketio.emit("stress", {"gsr": gsr})

    elif topic == "environment/data":
        temp = payload["temperature"]
        humidity = payload["humidity"]

        # write to InfluxDB
        point = Point("environment")\
            .tag("room", "room_101")\
            .field("temperature", temp)\
            .field("humidity", humidity)
        influx.write(record=point)

        # emit to dashboard
        socketio.emit("environment", {"temp": temp, "humidity": humidity})

        # rules
        if temp > 35:
            print(f"High temp → {temp}°C")
            socketio.emit("env_alert", {"type": "HIGH_TEMP", "temp": temp})

        if humidity > 70:
            print(f"High humidity → {humidity}%")
            socketio.emit("env_alert", {"type": "HIGH_HUMIDITY", "humidity": humidity})

    elif topic == "rfid/checkin":
        nurse = payload["nurse_id"]
        print(f"{nurse} checked in")

        # write to InfluxDB
        point = Point("rfid_checkin")\
            .tag("room", "room_101")\
            .tag("nurse_id", nurse)\
            .field("action", 1)
        influx.write(record=point)

        # emit to dashboard
        socketio.emit("rfid", {"nurse": nurse})

        # response time — only if alert is active
        if alert_active:
            response_time = (datetime.now() - alert_time).seconds
            print(f"{nurse} responded in {response_time}s")
            socketio.emit("response_time", {"nurse": nurse, "seconds": response_time})

# --- Flask route ---
@app.route("/")
def index():
    return render_template("index.html")

# --- MQTT client setup ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

# --- Start server ---
socketio.run(app, host="0.0.0.0", port=5000)