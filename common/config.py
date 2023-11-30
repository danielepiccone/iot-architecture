import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "test.mosquitto.org")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "test_topic_184982")
MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", 8883)
MQTT_TLS_ENABLED = os.getenv("MQTT_TLS_ENABLED", True)

# Local MQTT Broker
# MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
# MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", 1883)
# MQTT_TLS_ENABLED = os.getenv("MQTT_TLS_ENABLED", False)
