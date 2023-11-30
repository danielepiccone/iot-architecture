import datetime
from typing import Literal, Optional
from pydantic import BaseModel


class TelemetryPayload(BaseModel):
    id: str
    device_id: str
    temperature: int
    distance: int
    timestamp: datetime.datetime
    firmware_version: str


class DeviceState(BaseModel):
    id: str
    firmware_version: str
    state: Literal["ONLINE", "OFFLINE"]
    last_seen: datetime.datetime
    last_temperature: Optional[int]
    last_distance: Optional[int]
