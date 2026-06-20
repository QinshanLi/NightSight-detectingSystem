from pydantic import BaseModel
from datetime import datetime


class EventOut(BaseModel):
    id: int
    ts: datetime
    risk_type: str
    level: str
    location: str | None = None
    channel: str | None = None
    confidence: float | None = None
    boxes: list | None = None
    enhanced: bool = True

    class Config:
        from_attributes = True


class DeviceOut(BaseModel):
    id: str
    name: str
    kind: str
    online: bool
    status: str | None = None

    class Config:
        from_attributes = True


class StatItem(BaseModel):
    risk_type: str
    count: int


class ActuatorToggle(BaseModel):
    on: bool
