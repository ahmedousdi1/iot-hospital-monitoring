
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
TOPIC = "rfid/checkin"

NURSES = ["Nurse_A", "Nurse_B", "Nurse_C"]

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()
client.connect(BROKER, PORT)
client.loop_start()

print("RFID node started...")

while True:
    nurse = random.choice(NURSES)

    payload = json.dumps({
        "nurse_id": nurse,
        "action": "checkin"
    })

    client.publish(TOPIC, payload)
    print(f"Published → {nurse} checked in")

    time.sleep(30)