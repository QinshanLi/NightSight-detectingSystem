from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from app.db.database import Base


class RiskEvent(Base):
    __tablename__ = "risk_event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    risk_type = Column(String(32), index=True)      # 五类之一
    level = Column(String(4))                        # 高/中/低
    location = Column(String(64))                    # B2-03 坡道
    channel = Column(String(64))                     # 摄像头/节点编号
    confidence = Column(Float)
    boxes = Column(JSON)                             # 检测框列表
    thumb_path = Column(String(256))                 # 事件截图路径
    frame_idx = Column(Integer)                      # 帧序号
    enhanced = Column(Boolean, default=True)         # 是否经暗光增强


class Device(Base):
    __tablename__ = "device"
    id = Column(String(32), primary_key=True)        # led / buzzer / esp32 ...
    name = Column(String(64))
    kind = Column(String(32))                        # camera / edge / actuator / sensor
    online = Column(Boolean, default=False)
    status = Column(String(64))                      # 在线 · 28°C
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LinkLog(Base):
    __tablename__ = "link_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    event_id = Column(Integer, index=True)
    actuator = Column(String(32))                    # led / buzzer / voice ...
    command = Column(String(32))                     # on / off / flash
    simulated = Column(Boolean, default=True)        # 软件模拟 or 真发 MQTT
    result = Column(String(32), default="已执行")
