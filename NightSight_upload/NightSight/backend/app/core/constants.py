"""五类风险事件定义。与前端 risk 类型、报名表完全对齐。"""
from enum import Enum


class RiskType(str, Enum):
    COOCCUR = "车人共现"          # 行人框进入车辆行进 ROI
    SMALL_TARGET = "弱光小目标"    # 暗光增强后检出的小目标
    GLARE = "强光干扰"            # 眩光区域置信骤降
    BLIND_SPOT = "盲区接近"        # 遮挡边缘连续帧逼近
    INTRUSION = "危险区域入侵"      # 目标进入禁入 ROI


class RiskLevel(str, Enum):
    HIGH = "高"
    MID = "中"
    LOW = "低"


# 默认等级 + 联动动作（规则引擎用；可在 services/risk_rules 覆盖）
RISK_META = {
    RiskType.COOCCUR:      {"level": RiskLevel.HIGH, "actions": ["led", "buzzer", "voice"]},
    RiskType.SMALL_TARGET: {"level": RiskLevel.MID,  "actions": ["fill_light", "popup"]},
    RiskType.GLARE:        {"level": RiskLevel.LOW,  "actions": ["enhance"]},
    RiskType.BLIND_SPOT:   {"level": RiskLevel.MID,  "actions": ["led", "popup"]},
    RiskType.INTRUSION:    {"level": RiskLevel.HIGH, "actions": ["led", "buzzer", "log"]},
}

# YOLO 类别 → 是否“车” / “人”（车人共现判定用）
VEHICLE_CLASSES = {"car", "bus", "truck", "motorbike", "bicycle", "Car", "Bus"}
PERSON_CLASSES = {"person", "People", "Person", "pedestrian"}
