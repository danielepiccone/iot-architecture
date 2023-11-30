import datetime
import json
import logging
import time
from common.device_service import DeviceService
from common.models import DeviceState

device_service = DeviceService()

OFFLINE_THRESHOLD_SECONDS = 30
CHECK_INTERVAL_SECONDS = 30

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

while True:
    now = datetime.datetime.now()
    all_devices = [
        DeviceState(**device_state) for device_state in device_service.list_devices()
    ]

    for device in all_devices:
        if device.state == "ONLINE" and device.last_seen < now - datetime.timedelta(
            seconds=OFFLINE_THRESHOLD_SECONDS
        ):
            logger.info(f"Device: {device.id} went offline")
            device.state = "OFFLINE"
            device_service.update_device(device.id, device.model_dump_json())

    time.sleep(CHECK_INTERVAL_SECONDS)
