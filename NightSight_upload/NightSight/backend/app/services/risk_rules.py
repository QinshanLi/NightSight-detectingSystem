"""
五类风险规则引擎：把逐帧检测框 → 风险事件。
判定基于连续帧（论文中盲区接近用连续帧逼近判断），这里维护短历史。
"""
from collections import deque
from app.core.constants import (
    RiskType, RISK_META, VEHICLE_CLASSES, PERSON_CLASSES,
)


def _iou(a, b):
    ax2, ay2 = a.x + a.w, a.y + a.h
    bx2, by2 = b.x + b.w, b.y + b.h
    ix1, iy1 = max(a.x, b.x), max(a.y, b.y)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    union = a.w * a.h + b.w * b.h - inter
    return inter / union if union > 0 else 0.0


class RiskEngine:
    def __init__(self, danger_roi=(0.4, 0.0, 0.2, 0.5), vehicle_path_roi=(0.3, 0.4, 0.4, 0.6)):
        # ROI 格式 (x, y, w, h) 归一化；可由前端画框配置
        self.danger_roi = danger_roi
        self.vehicle_path = vehicle_path_roi
        self.history = deque(maxlen=8)   # 连续帧缓存（盲区接近用）

    def _in_roi(self, det, roi):
        rx, ry, rw, rh = roi
        cx, cy = det.x + det.w / 2, det.y + det.h / 2
        return rx <= cx <= rx + rw and ry <= cy <= ry + rh

    def evaluate(self, frame_result):
        """返回触发的风险事件列表 [{risk_type, level, confidence, boxes, ...}]。"""
        dets = frame_result.detections
        self.history.append(dets)
        events = []

        persons = [d for d in dets if d.cls in PERSON_CLASSES or d.cls == "0"]
        vehicles = [d for d in dets if d.cls in VEHICLE_CLASSES]

        # 1) 车人共现：人进入车辆行进 ROI，且画面同时有车
        for p in persons:
            if vehicles and self._in_roi(p, self.vehicle_path):
                events.append(self._make(RiskType.COOCCUR, p))
                break

        # 2) 弱光小目标：低照度 + 小框 + 中低置信
        small = [d for d in dets if d.w * d.h < 0.01 and d.conf < 0.7]
        if small and (frame_result.lux is None or frame_result.lux <= 15):
            events.append(self._make(RiskType.SMALL_TARGET, max(small, key=lambda d: d.conf)))

        # 3) 强光干扰：检测到框但整体置信骤降（与上一帧对比）
        if len(self.history) >= 2:
            prev = self.history[-2]
            if prev and dets:
                drop = (sum(d.conf for d in prev) / len(prev)) - \
                       (sum(d.conf for d in dets) / len(dets))
                if drop > 0.25:
                    events.append(self._make(RiskType.GLARE, dets[0]))

        # 4) 盲区接近：连续帧中某目标框面积持续增大（逼近）
        approaching = self._detect_approach()
        if approaching:
            events.append(self._make(RiskType.BLIND_SPOT, approaching))

        # 5) 危险区域入侵：任意目标进入禁入 ROI
        for d in dets:
            if self._in_roi(d, self.danger_roi):
                events.append(self._make(RiskType.INTRUSION, d))
                break

        return events

    def _detect_approach(self):
        """连续 ≥3 帧同位置目标面积单调增大 → 逼近。简化版用最大框近似。"""
        if len(self.history) < 3:
            return None
        areas = []
        last = None
        for frame in list(self.history)[-3:]:
            if not frame:
                return None
            big = max(frame, key=lambda d: d.w * d.h)
            areas.append(big.w * big.h)
            last = big
        if areas[0] < areas[1] < areas[2] and areas[2] > 0.02:
            return last
        return None

    def _make(self, rtype: RiskType, det):
        meta = RISK_META[rtype]
        return {
            "risk_type": rtype.value,
            "level": meta["level"].value,
            "actions": meta["actions"],
            "confidence": round(det.conf, 3),
            "boxes": [{"x": det.x, "y": det.y, "w": det.w, "h": det.h,
                       "cls": det.cls, "conf": det.conf}],
        }
