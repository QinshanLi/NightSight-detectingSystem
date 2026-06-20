"""
事件主流程：推理逐帧 → 风险判定 → 触发联动 → 写库 → WebSocket 广播。
后台任务运行；前端通过 /ws 收到结构化事件。
"""
import asyncio, time
from datetime import datetime
from app.inference.factory import build_inference
from app.services.risk_rules import RiskEngine
from app.services.actuator import actuator
from app.db.database import SessionLocal
from app.db.models import RiskEvent, LinkLog


class EventPipeline:
    def __init__(self, broadcaster):
        self.broadcaster = broadcaster      # WebSocket 广播器
        self.engine = RiskEngine()
        self._running = False

    async def run(self, source=0):
        self._running = True
        infer = build_inference(source=source)
        loop = asyncio.get_event_loop()
        # 推理是阻塞生成器，放线程里跑，逐帧回调
        gen = infer.frames()
        while self._running:
            fr = await loop.run_in_executor(None, lambda: next(gen, None))
            if fr is None:
                break
            await self._handle_frame(fr)
        infer.close()

    async def _handle_frame(self, fr):
        # 始终把检测框推给前端（叠框 + 实时画面）
        await self.broadcaster.broadcast({
            "kind": "frame",
            "frame_idx": fr.frame_idx, "fps": fr.fps, "lux": fr.lux,
            "detections": [d.__dict__ for d in fr.detections],
        })
        # 风险判定
        events = self.engine.evaluate(fr)
        for ev in events:
            await self._emit_event(ev, fr)

    async def _emit_event(self, ev, fr):
        # 1) 联动（软件模拟 / 真发 MQTT）
        link_logs = actuator.trigger(ev["actions"])
        # 2) 入库
        db = SessionLocal()
        try:
            row = RiskEvent(
                ts=datetime.utcnow(), risk_type=ev["risk_type"], level=ev["level"],
                location="B2-03 坡道", channel="cam-01",
                confidence=ev["confidence"], boxes=ev["boxes"],
                frame_idx=fr.frame_idx, enhanced=fr.enhanced,
            )
            db.add(row); db.commit(); db.refresh(row)
            for lg in link_logs:
                db.add(LinkLog(event_id=row.id, actuator=lg["actuator"],
                               command=lg["command"], simulated=lg["simulated"]))
            db.commit()
            event_id = row.id
        finally:
            db.close()
        # 3) WebSocket 推送告警
        await self.broadcaster.broadcast({
            "kind": "alert",
            "id": event_id,
            "type": ev["risk_type"], "level": ev["level"],
            "loc": "B2-03 坡道", "conf": ev["confidence"],
            "boxes": ev["boxes"], "actions": [l["name"] for l in link_logs],
            "ts": time.time(),
        })

    def stop(self):
        self._running = False
