
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

TOPIC = "environment/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()
client.connect(BROKER, PORT)
client.loop_start()

print("Environment node started...")

while True:
    temperature = round(random.uniform(18, 38), 1)
    humidity = round(random.uniform(30, 80), 1)

    payload = json.dumps({
        "temperature": temperature,
        "humidity": humidity
    })

    client.publish(TOPIC, payload)
    print(f"Published → Temp={temperature}°C | Humidity={humidity}%")

    time.sleep(5)