import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine, SessionLocal
from app.db import models
from app.api import routes, ws
from app.services.pipeline import EventPipeline

pipeline: EventPipeline | None = None


def seed_devices():
    """初始化设备表（首次启动）。"""
    db = SessionLocal()
    try:
        if db.query(models.Device).count() == 0:
            defaults = [
                ("edge-01", "边缘计算节点", "edge", True, "在线 · 28°C"),
                ("cam-01", "车载摄像头", "camera", True, "在线 · 25FPS"),
                ("cam-02", "固定路侧摄像头", "camera", True, "在线"),
                ("esp32", "ESP32 控制器", "actuator", True, "已连接"),
                ("lux-01", "照度传感器", "sensor", True, "6 lux"),
                ("led", "LED 警示灯", "actuator", True, "待命"),
                ("buzzer", "蜂鸣器", "actuator", True, "待命"),
                ("fill_light", "补光灯节点", "actuator", False, "待命"),
            ]
            for did, name, kind, online, status in defaults:
                db.add(models.Device(id=did, name=name, kind=kind, online=online, status=status))
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)   # 自动建表
    seed_devices()
    global pipeline
    pipeline = EventPipeline(ws.broadcaster)
    # 后台跑推理管线（source: 0=摄像头；replay 模式忽略）
    task = asyncio.create_task(pipeline.run(source=0))
    yield
    pipeline.stop()
    task.cancel()


app = FastAPI(title="NightSight 守夜者 API", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # 前端 Vite
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(routes.router)
app.include_router(ws.router)


@app.get("/")
def root():
    return {"service": "NightSight 守夜者", "docs": "/docs"}
