# AIoT Low-Light Risk Event Stream System

## 📌 Project Overview
This project transforms publicly available low-light driving video datasets into a system-level continuous event stream for AIoT validation.

Unlike traditional single-test datasets (e.g., ExDark, DarkFace), this project constructs a structured and continuous low-light traffic risk scenario stream under driver first-person perspective.

## 🚗 Key Features
- Driver first-person low-light video scenario reconstruction
- Risk-based event classification and labeling
- Continuous event stream generation from segmented clips
- AIoT system-level validation (not only model accuracy testing)
- Multi-risk scenarios:
  - Vehicle-pedestrian co-occurrence risk
  - Weak-light small object detection risk
  - Strong glare interference risk
  - Blind spot approach risk
  - Dangerous area intrusion risk

## 🧠 System Pipeline
1. Raw low-light driving video collection
2. Risk-based segmentation
3. Scene classification and labeling
4. Programmatic recombination
5. Continuous event stream generation
6. AIoT system testing (enhancement + detection + alerting + logging)

## 🎯 Goal
Bridge the gap between algorithm-level evaluation and real-world AIoT system deployment in low-light traffic safety scenarios.

## 📂 Dataset Status
Dataset:
https://www.kaggle.com/datasets/evelynmimi/nightsightsystem-eventstream

---

## 🔍 Detection Model: YOLO11n + EMV

> **Summary:** The detector has been upgraded from YOLOv3 (MMDetection) to **YOLO11n + EMV (Ultralytics)**. The calling interface is different but simpler.

### What Changed and Why

| | Old Version | New Version |
|---|---|---|
| Detector | YOLOv3 | YOLO11n |
| Framework | MMDetection 2.x (legacy, hard to install) | Ultralytics (modern, easy to deploy) |
| Enhancement | EMV | EMV (retained — core contribution) |
| API | mmdet config files | `from ultralytics import YOLO` |

The old framework could not be installed on our GPU (RTX 4060). The new framework is modern, easy to deploy, and supports edge device export. **The EMV enhancement module — our core innovation — is preserved**, just ported to the new detector.

**The EMV enhancement runs automatically inside the model. The backend does not need to handle it explicitly.**

---

### Environment Setup

```bash
conda activate emv-yolo
pip install ultralytics fastapi uvicorn opencv-python
```

Model weights (after training completes):
```
runs/detect/emv_yolo11n/weights/best.pt
```

> Before training finishes, use `runs/detect/baseline_yolo11n-2/weights/best.pt` or `yolo11n.pt` as a placeholder for development.

---

### Loading the Model ⚠️

Our model is a custom YOLO11 + EMV architecture. **You must import the model definition before loading weights**, or deserialization will fail:

```python
import sys
sys.path.insert(0, "scripts")  # so Python can find emv_yolo_model.py
import emv_yolo_model           # ★ MUST come before YOLO() ★

from ultralytics import YOLO
model = YOLO("runs/detect/emv_yolo11n/weights/best.pt")
```

> `import emv_yolo_model` must precede `YOLO(...)`. The EMV enhancement is embedded in the model — calling `predict` automatically applies enhancement before detection; no extra preprocessing is needed.

---

### Running Inference

Pass an image path or an OpenCV numpy array:

```python
results = model.predict(source=img, imgsz=416, conf=0.25, verbose=False)
r = results[0]  # one result per image

for b in r.boxes:
    cls_id = int(b.cls[0])
    print(
        "class_id:", cls_id,
        "class_name:", r.names[cls_id],
        "confidence:", float(b.conf[0]),
        "box (xyxy, px):", b.xyxy[0].tolist(),  # [x1, y1, x2, y2]
    )
```

Each detection box exposes:

| Field | Description |
|---|---|
| `b.cls[0]` | Class ID (0–11) |
| `r.names[cls_id]` | Class name |
| `b.conf[0]` | Confidence score (0–1) |
| `b.xyxy[0]` | Bounding box in pixels [left, top, right, bottom] |
| `b.xywhn[0]` | Normalized [cx, cy, w, h] (use when relative coords needed) |

---

### Minimal FastAPI Backend

```python
# server.py
import sys
sys.path.insert(0, "scripts")
import emv_yolo_model                       # must come first
from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File
import numpy as np, cv2

app = FastAPI()
model = YOLO("runs/detect/emv_yolo11n/weights/best.pt")  # load once at startup

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    r = model.predict(source=img, imgsz=416, conf=0.25, verbose=False)[0]
    dets = []
    for b in r.boxes:
        cid = int(b.cls[0])
        dets.append({
            "class_id": cid,
            "class_name": r.names[cid],
            "confidence": round(float(b.conf[0]), 3),
            "box_xyxy": [round(v, 1) for v in b.xyxy[0].tolist()],
        })
    return {"count": len(dets), "detections": dets}

# Run: uvicorn server:app --host 0.0.0.0 --port 8000
```

Example response:
```json
{
  "count": 2,
  "detections": [
    {"class_id": 10, "class_name": "People", "confidence": 0.83, "box_xyxy": [120.5, 88.0, 210.3, 360.0]},
    {"class_id": 4,  "class_name": "Car",    "confidence": 0.77, "box_xyxy": [400.1, 150.2, 520.0, 240.7]}
  ]
}
```

---

### Class Labels (ExDark, 12 classes)

| ID | Name | ID | Name | ID | Name | ID | Name |
|---|---|---|---|---|---|---|---|
| 0 | Bicycle | 1 | Boat | 2 | Bottle | 3 | Bus |
| 4 | Car | 5 | Cat | 6 | Chair | 7 | Cup |
| 8 | Dog | 9 | Motorbike | 10 | People | 11 | Table |

> If the dataset is switched to DarkFace (face detection), there will be only 1 class: `face`.

---

### Video / Camera / Live Stream

```python
model.predict(source="video.mp4", save=True)  # detect and save annotated video
model.predict(source=0)                        # webcam real-time
```

For a live dashboard, call `model.predict(frame)` per frame and push detection JSON to the frontend via WebSocket.

---

### Backend Notes

1. **Load the model once** at service startup — do not call `YOLO(...)` per request.
2. **`import emv_yolo_model` must precede `YOLO(...)`** (see Loading section above).
3. Tune `conf` as needed: raise it (e.g., `0.4`) to reduce false positives, lower it (e.g., `0.15`) to reduce missed detections.
4. EMV enhancement is applied automatically — no manual image preprocessing required.
5. Use `imgsz=416` for inference (matches training resolution; conserves VRAM).
