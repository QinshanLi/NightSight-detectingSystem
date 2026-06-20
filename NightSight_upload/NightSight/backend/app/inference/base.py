"""推理器统一接口：realtime（真接模型）与 replay（JSON回放）都实现它。"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Detection:
    cls: str
    conf: float
    # 归一化坐标 [0,1]，便于前端在任意分辨率上叠框
    x: float; y: float; w: float; h: float


@dataclass
class FrameResult:
    frame_idx: int
    ts: float
    detections: list[Detection] = field(default_factory=list)
    enhanced: bool = True            # 是否经暗光增强
    lux: int | None = None           # 估计照度（可由光照传感器覆盖）
    fps: float | None = None
    enhanced_jpg: bytes | None = None  # 增强后帧（可选，给前端做增强前后对比）


class BaseInference(ABC):
    @abstractmethod
    def frames(self):
        """生成器：逐帧产出 FrameResult。"""
        raise NotImplementedError

    def close(self):
        pass
