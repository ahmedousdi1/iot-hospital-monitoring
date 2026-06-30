import paho.mqtt.client as mqtt
import random
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")
TOPIC = "patient/vitals"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()
client.connect(BROKER, PORT)
client.loop_start()

print("Patient node started...")

while True:
    heart_rate = random.randint(60, 140)
    spo2 = random.randint(85, 100)
    gsr = round(random.uniform(0.4, 1.0), 2)

    payload = json.dumps({
        "heart_rate": heart_rate,
        "spo2": spo2,
        "gsr": gsr
    })

    client.publish(TOPIC, payload)
    print(f"Published → HR={heart_rate} | SpO2={spo2}% | GSR={gsr}")

    time.sleep(2)