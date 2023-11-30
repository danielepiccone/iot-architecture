import json
import logging
from common.telemetry_queue import SQSWorker
from common.device_service import DeviceService
from common.models import DeviceState, TelemetryPayload
from common.telemetry_service import TelemetryService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_message(
    payload: str, telemetry_service=TelemetryService(), device_service=DeviceService()
):
    telemetry = TelemetryPayload(**json.loads(payload))
    logger.info(f"Received telemetry: {telemetry}")

    file_name = (
        "/"
        + telemetry.device_id
        + "/"
        + str(round(telemetry.timestamp.timestamp() * 1e3))
        + ".json"
    )
    telemetry_service.put(file_name, telemetry.model_dump_json())

    device = device_service.get_device(telemetry.device_id)

    new_device_state = DeviceState(
        id=telemetry.device_id,
        last_seen=telemetry.timestamp,
        last_temperature=telemetry.temperature,
        last_distance=telemetry.distance,
        firmware_version=telemetry.firmware_version,
        state="ONLINE",
    )

    if device:
        device_service.update_device(
            telemetry.device_id, new_device_state.model_dump_json()
        )
        logger.info(f"Updated device: {new_device_state}")
    else:
        device_service.create_device(
            telemetry.device_id, new_device_state.model_dump_json()
        )
        logger.info(f"Created device: {new_device_state}")


SQSWorker().run(on_message)
