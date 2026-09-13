from fastapi import FastAPI
import paho.mqtt.client as mqtt
import ssl
from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()


app.add_middleware(
CORSMiddleware,
allow_origins=[
"http://localhost:3000",
"http://127.0.0.1:3000",
"https://nexora-kamal-97e6.vercel.app",
"https://nexora-kamal.vercel.app",
"https://nexora-1c8by8a10-kamal-97e6.vercel.app"
],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# ==========================================
# HiveMQ Cloud configuration
# ==========================================

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = 8883

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

MQTT_TOPIC = "home/esp32/light"


# ==========================================
# MQTT client
# ==========================================

mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="fastapi-server"
)

mqtt_client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD
)

# TLS encryption
mqtt_client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED
)


# ==========================================
# MQTT callbacks
# ==========================================

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT broker")
    print("Reason:", reason_code)


def on_disconnect(client, userdata, flags, reason_code, properties):
    print("Disconnected from MQTT broker")


mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect


# ==========================================
# FastAPI startup
# ==========================================

@app.on_event("startup")
def startup():

    print("Connecting to MQTT broker...")

    mqtt_client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        keepalive=60
    )

    # Keep MQTT connection running
    mqtt_client.loop_start()


# ==========================================
# FastAPI shutdown
# ==========================================

@app.on_event("shutdown")
def shutdown():

    print("Disconnecting MQTT...")

    mqtt_client.loop_stop()
    mqtt_client.disconnect()


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message": "ESP32 IoT FastAPI server",
        "mqtt_topic": MQTT_TOPIC
    }


# ==========================================
# Turn light ON
# ==========================================

@app.post("/light/on")
def light_on():

    result = mqtt_client.publish(
        MQTT_TOPIC,
        "ON"
    )

    if result.rc != mqtt.MQTT_ERR_SUCCESS:

        return {
            "success": False,
            "message": "Failed to publish MQTT message"
        }

    return {
        "success": True,
        "device": "ESP32",
        "light": "ON"
    }


# ==========================================
# Turn light OFF
# ==========================================

@app.post("/light/off")
def light_off():

    result = mqtt_client.publish(
        MQTT_TOPIC,
        "OFF"
    )

    if result.rc != mqtt.MQTT_ERR_SUCCESS:

        return {
            "success": False,
            "message": "Failed to publish MQTT message"
        }

    return {
        "success": True,
        "device": "ESP32",
        "light": "OFF"
    }


# ==========================================
# Health check
# ==========================================

@app.get("/health")
def health():

    return {
        "fastapi": "running",
        "mqtt": mqtt_client.is_connected()
    }