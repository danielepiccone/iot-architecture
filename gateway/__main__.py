import json
import paho.mqtt.client as mqtt
import logging
from common.config import MQTT_BROKER, MQTT_TOPIC, MQTT_BROKER_PORT, MQTT_TLS_ENABLED
from common.telemetry_queue import SQSWorker
import ssl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

telemetry_queue = SQSWorker()


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
    client.subscribe(f"{MQTT_TOPIC}/#")


def on_message(client, userdata, msg):
    logger.info(msg.topic + " " + str(msg.payload))
    device_id = msg.topic.split("/")[-1]
    telemetry_queue.enqueue(msg.payload.decode("utf-8"), device_id)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if MQTT_TLS_ENABLED:
    client.tls_set(
        "common/certificates/mosquitto.org.crt", tls_version=ssl.PROTOCOL_TLSv1_2
    )
    client.tls_insecure_set(False)

client.connect(MQTT_BROKER, MQTT_BROKER_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()
