import datetime
import json
import ssl
import uuid
import paho.mqtt.client as mqtt
import time
import random
import logging
from common.config import MQTT_BROKER, MQTT_BROKER_PORT, MQTT_TLS_ENABLED, MQTT_TOPIC
from common.models import TelemetryPayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))

    device_ids = ["device1", "device2", "device3"]
    n_payloads = 10

    for _ in range(n_payloads):
        for device_id in device_ids:
            payload = TelemetryPayload(
                **{
                    "id": str(uuid.uuid4()),
                    "device_id": device_id,
                    "distance": random.randint(0, 100),
                    "temperature": random.randint(-50, 50),
                    "timestamp": datetime.datetime.now(),
                    "firmware_version": "1.0.0",
                }
            )
            client.publish(f"{MQTT_TOPIC}/{device_id}", payload.model_dump_json())
            time.sleep(0.25)
            logger.info(f"Published telemetry: {payload}")

        time.sleep(1)


client = mqtt.Client()
client.on_connect = on_connect

if MQTT_TLS_ENABLED:
    client.tls_set(
        "common/certificates/mosquitto.org.crt", tls_version=ssl.PROTOCOL_TLSv1_2
    )
    client.tls_insecure_set(False)


client.connect(MQTT_BROKER, MQTT_BROKER_PORT, 60)


client.loop_forever()
