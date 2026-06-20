# NightSight 守夜者 · 后端

面向机器视觉的暗光增强检测与 AIoT 联动预警系统 —— FastAPI 后端。
算法采用曾俊贤硕士论文《面向机器视觉的暗光图像增强目标检测》的 **EMV-YOLO / TGE-YOLO** 管线。

## 算法管线（对应论文）

```
暗光帧 S
  └─ EMV 模块（仅 ~27k 参数，边缘可实时）
       ① Retinex 分解：轻量浅层网络 → [I 光照分量(纹理), R 反射分量(颜色)]
       ② 语义引导潜在空间特征增强：低维特征空间增强，避免上采样
       ③ 融合 → 增强图 S̄
  └─ YOLOv3 检测头 → 目标框 + 类别 + 置信度
  端到端训练，仅检测损失驱动，无需 GT 图像
TGE-YOLO：在此之上用 SAM 蒸馏，仅增强前景、背景加过滤掩码，抑制噪声放大
```

实时推理在 `app/inference/emv_yolo.py`，两个接入点已标好：
`_load_model()` 加载成员A的 `.pt` 权重，`_forward()` 单帧前向（增强+检测一体）。

## 快速开始

### 方式一：真接 GPU 实时推理（报名表方案）
```bash
pip install -r requirements.txt          # 含 torch，按 CUDA 版本到 pytorch.org 选轮子
cp .env.example .env                      # 填 MySQL 账号、权重路径
# .env: INFER_MODE=realtime  MODEL_NAME=EMV-YOLO  WEIGHTS_PATH=weights/emv_yolo.pt  DEVICE=cuda
# 把成员A的权重放到 weights/emv_yolo.pt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 方式二：演示降级 / 无 GPU（replay 回放，零延迟稳定）
```bash
# 成员A先离线把视频跑成标签：
python scripts_offline_infer.py --video data/event_stream_v1.mp4 --out data/event_labels.json
# .env: INFER_MODE=replay
uvicorn main:app --port 8000
```

### 无 MySQL 时（应急）
`.env` 里设 `DB_URL=sqlite:///./nightsight.db`，零配置跑起来，表自动建。

文档：启动后访问 `http://localhost:8000/docs`（Swagger）。

## 目录结构

```
backend/
├── main.py                       应用入口：建表 + seed 设备 + 启动推理管线 + CORS
├── requirements.txt
├── .env.example                  所有配置项（推理模式/模型/MySQL/MQTT）
├── scripts_offline_infer.py      成员A离线工具：视频 → event_labels.json
├── weights/                      放 .pt 权重
├── data/                         视频 + event_labels.json
└── app/
    ├── core/
    │   ├── config.py             集中配置（pydantic-settings 读 .env）
    │   └── constants.py          五类风险定义 + 默认等级 + 联动动作
    ├── db/
    │   ├── database.py           MySQL 引擎（可 DB_URL 切 SQLite）
    │   └── models.py             表：risk_event / device / link_log
    ├── inference/
    │   ├── base.py               推理器接口 + Detection/FrameResult 数据类
    │   ├── emv_yolo.py           ★ EMV/TGE-YOLO 实时推理（论文管线，2 个接入点）
    │   ├── replay.py             JSON 回放推理（演示降级）
    │   └── factory.py            按 INFER_MODE 选推理器
    ├── services/
    │   ├── risk_rules.py         ★ 五类风险规则引擎（连续帧判定）
    │   ├── actuator.py           ESP32 联动（默认软件模拟，保留 MQTT 接口）
    │   └── pipeline.py           主流程：推理→规则→联动→入库→WS 广播
    ├── api/
    │   ├── ws.py                 WebSocket /ws + 广播器
    │   └── routes.py             REST：history/latest/stats/devices/toggle/link-logs/status
    └── schemas/dto.py            出参模型
```

## 接口一览

| 方法 | 路径 | 说明 |
|---|---|---|
| WS | `/ws` | 实时推送 `frame`（检测框）与 `alert`（风险告警） |
| GET | `/api/events/history?risk_type=&limit=` | 历史事件，可按风险类型筛选 |
| GET | `/api/events/latest?after_id=` | 轮询降级用（WS 不通时） |
| GET | `/api/events/stats` | 五类风险计数（前端统计图） |
| GET | `/api/devices` | 设备/节点在线状态 |
| POST | `/api/devices/{id}/toggle` | 开关声光设备（模拟或真发 MQTT） |
| GET | `/api/link-logs` | 联动操作日志 |
| GET | `/api/system/status` | 推理模式 + 传输链路状态 |

## WebSocket 消息格式（前端对接）

```jsonc
// 每帧检测框（叠框 + 实时画面）
{ "kind": "frame", "frame_idx": 12, "fps": 25, "lux": 6,
  "detections": [{"cls":"person","conf":0.91,"x":0.30,"y":0.46,"w":0.18,"h":0.20}] }

// 风险告警（弹窗 + 告警流 + 截图留存）
{ "kind": "alert", "id": 42, "type": "车人共现", "level": "高",
  "loc": "B2-03 坡道", "conf": 0.91, "boxes": [...],
  "actions": ["LED 警示灯","蜂鸣器","语音广播"], "ts": 1718... }
```
前端 `useEventStream.js` 已按此协议解析。检测框坐标为归一化 [0,1]，任意分辨率自适应。

## ESP32 联动

当前 `MQTT_ENABLED=false` → 纯软件模拟：只记日志、回传状态，**接口位置完整保留**。
硬件就绪后把它设 `true`，`actuator.py` 即真发指令到 `nightsight/actuator/cmd`，其它代码不动。

## 五类风险判定逻辑（risk_rules.py）

| 风险 | 规则 | 默认等级 |
|---|---|---|
| 车人共现 | 人框进入车辆行进 ROI 且画面有车 | 高 |
| 弱光小目标 | 低照度 + 小框 + 中低置信 | 中 |
| 强光干扰 | 整体置信较上一帧骤降 >0.25 | 低 |
| 盲区接近 | 连续 ≥3 帧目标框面积单调增大 | 中 |
| 危险区域入侵 | 目标进入禁入 ROI | 高 |

ROI 可由前端画框配置（`RiskEngine(danger_roi=, vehicle_path_roi=)`）。
