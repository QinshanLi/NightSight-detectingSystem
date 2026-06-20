from app.core.config import settings
from app.inference.base import BaseInference


def build_inference(source=0) -> BaseInference:
    """realtime → 真接 EMV/TGE-YOLO；replay → JSON 回放。"""
    if settings.INFER_MODE == "replay":
        from app.inference.replay import ReplayInference
        return ReplayInference()
    from app.inference.emv_yolo import EMVYoloInference
    return EMVYoloInference(source=source)
