import json
import os
from datetime import datetime

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER", "mqtt.ohstem.vn")
PORT = int(os.getenv("MQTT_PORT", "1883"))
USERNAME = os.getenv("MQTT_USERNAME", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
TOPIC_RESULT = os.getenv("MQTT_TOPIC_RESULT", "face/result")
TOPIC_YOLOBIT = os.getenv("MQTT_TOPIC_YOLOBIT", "V1")

socketio = None
mqtt_client = None
prev = '-1'

def attach_socketio(socketio_instance):
    global socketio
    socketio = socketio_instance


def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)
    client.subscribe(TOPIC_RESULT)
    print(f"Subscribed to {TOPIC_RESULT}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("MQTT disconnected unexpectedly. Reconnecting...")


def on_message(client, userdata, msg):
    global prev
    try:
        payload = msg.payload.decode()
        print("\nReceived:", payload)

        data = json.loads(payload)
        name = data.get("name", "UNKNOWN").upper()

        status = "Recognized" if name != "UNKNOWN" else "Unknown"

        if name != prev:
            # print(f"Status: {status} - {name}")
            client.publish(TOPIC_YOLOBIT, name, retain=True)
            print(f"Published to {TOPIC_YOLOBIT}: {name}")
            prev = name

        event = {
            "name": name,
            "status": status,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }

        if socketio:
            socketio.emit("face_event", event)

    except Exception as exc:
        print("Error:", exc)


def create_client():
    client = mqtt.Client()
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)

    client.reconnect_delay_set(min_delay=1, max_delay=30)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    return client


def start_mqtt(background=False):
    global mqtt_client

    mqtt_client = create_client()
    print("Connecting to broker...")
    mqtt_client.connect(BROKER, PORT, 60)

    if background:
        mqtt_client.loop_start()
    else:
        mqtt_client.loop_forever()

    return mqtt_client


if __name__ == "__main__":
    start_mqtt()
