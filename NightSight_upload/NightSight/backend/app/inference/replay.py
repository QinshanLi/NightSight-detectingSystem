"""
回放推理：读成员A离线跑好的 event_labels.json，按时间轴产出帧结果。
无 GPU、现场不稳定时的稳妥降级路径——与前端协议完全一致。

event_labels.json 约定格式：
{
  "fps": 25,
  "frames": [
    {"frame_idx": 0, "lux": 6, "detections": [
        {"cls": "person", "conf": 0.91, "x": 0.30, "y": 0.46, "w": 0.18, "h": 0.20}
    ]},
    ...
  ]
}
"""
import json, time
from app.core.config import settings
from app.inference.base import BaseInference, Detection, FrameResult


class ReplayInference(BaseInference):
    def __init__(self, labels_path: str | None = None):
        path = labels_path or settings.REPLAY_LABELS
        with open(path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.fps = self.data.get("fps", 25)

    def frames(self):
        interval = 1.0 / self.fps
        for fr in self.data.get("frames", []):
            dets = [Detection(**d) for d in fr.get("detections", [])]
            yield FrameResult(
                frame_idx=fr.get("frame_idx", 0),
                ts=time.time(),
                detections=dets,
                enhanced=True,
                lux=fr.get("lux"),
                fps=self.fps,
            )
            time.sleep(interval)   # 按真实帧率回放，营造实时感
