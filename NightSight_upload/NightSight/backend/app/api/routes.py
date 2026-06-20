from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import RiskEvent, Device, LinkLog
from app.schemas.dto import EventOut, DeviceOut, StatItem, ActuatorToggle
from app.services.actuator import actuator
from app.core.config import settings

router = APIRouter(prefix="/api")


@router.get("/events/history", response_model=list[EventOut])
def history(
    risk_type: str | None = Query(None, description="按风险类型筛选；空=全部"),
    limit: int = 50,
    db: Session = Depends(get_db),
):
    q = db.query(RiskEvent).order_by(RiskEvent.ts.desc())
    if risk_type and risk_type != "全部":
        q = q.filter(RiskEvent.risk_type == risk_type)
    return q.limit(limit).all()


@router.get("/events/latest", response_model=list[EventOut])
def latest(after_id: int = 0, db: Session = Depends(get_db)):
    """轮询降级用：取比 after_id 新的事件。"""
    return (db.query(RiskEvent)
              .filter(RiskEvent.id > after_id)
              .order_by(RiskEvent.id.asc()).all())


@router.get("/events/stats", response_model=list[StatItem])
def stats(db: Session = Depends(get_db)):
    rows = (db.query(RiskEvent.risk_type, func.count().label("c"))
              .group_by(RiskEvent.risk_type).all())
    return [StatItem(risk_type=r[0], count=r[1]) for r in rows]


@router.get("/devices", response_model=list[DeviceOut])
def devices(db: Session = Depends(get_db)):
    return db.query(Device).all()


@router.post("/devices/{device_id}/toggle")
def toggle(device_id: str, body: ActuatorToggle, db: Session = Depends(get_db)):
    """前端开关声光设备 → 走联动（模拟或真发 MQTT）。"""
    logs = actuator.trigger([device_id])
    dev = db.query(Device).get(device_id)
    if dev:
        dev.online = body.on
        dev.status = "已开启" if body.on else "待命"
        db.commit()
    return {"ok": True, "simulated": logs[0]["simulated"] if logs else True}


@router.get("/link-logs")
def link_logs(limit: int = 20, db: Session = Depends(get_db)):
    rows = db.query(LinkLog).order_by(LinkLog.ts.desc()).limit(limit).all()
    return [{"ts": r.ts, "event_id": r.event_id, "actuator": r.actuator,
             "command": r.command, "simulated": r.simulated, "result": r.result}
            for r in rows]


@router.get("/system/status")
def system_status():
    """传输链路 + 推理模式，给前端的状态卡。"""
    return {
        "infer_mode": settings.INFER_MODE,
        "model": settings.MODEL_NAME,
        "device": settings.DEVICE,
        "mqtt_enabled": settings.MQTT_ENABLED,
        "transport": {"ws": True, "http": True, "mqtt": settings.MQTT_ENABLED},
    }
