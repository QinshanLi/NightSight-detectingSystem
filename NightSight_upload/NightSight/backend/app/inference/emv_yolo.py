"""
EMV-YOLO / TGE-YOLO 实时推理封装。

对应论文（曾俊贤，《面向机器视觉的暗光图像增强目标检测》）管线：
  暗光帧 S
    → EMV: ① Retinex 分解(轻量浅层网络) 得 [I 光照, R 反射]
           ② 语义引导的潜在空间特征增强（低维空间，避免上采样）
           ③ 融合得增强图 S̄
    → YOLOv3 检测头  →  目标框 + 类别 + 置信度
  端到端训练，仅检测损失驱动；EMV 仅 ~27k 参数，适合边缘实时。
  TGE-YOLO：在此基础上用 SAM 蒸馏，仅增强前景区域、背景加过滤掩码。

成员A把训练好的权重 (.pt) 放到 weights/，这里加载并逐帧推理。
权重内部结构（EMVNet + YOLOv3Head）由成员A的训练代码决定，
下方 _load_model / _forward 处留出明确接入点。
"""
import time
from app.core.config import settings
from app.inference.base import BaseInference, Detection, FrameResult


class EMVYoloInference(BaseInference):
    def __init__(self, source=0):
        import torch, cv2  # 延迟导入：replay 模式无需装 torch
        self.torch, self.cv2 = torch, cv2
        self.device = settings.DEVICE if torch.cuda.is_available() else "cpu"
        self.size = settings.INPUT_SIZE
        self.conf, self.iou = settings.CONF_THRES, settings.IOU_THRES
        self.cap = cv2.VideoCapture(source)
        self.model = self._load_model()

    # ---- 接入点 1：加载论文模型（EMV/TGE + YOLOv3 头） ----
    def _load_model(self):
        torch = self.torch
        ckpt = torch.load(settings.WEIGHTS_PATH, map_location=self.device)
        # 约定：成员A保存为 {"model": nn.Module} 或可直接 torch.load 的整模型
        model = ckpt["model"] if isinstance(ckpt, dict) and "model" in ckpt else ckpt
        model.to(self.device).eval()
        return model

    # ---- 接入点 2：单帧前向（增强 + 检测一体，端到端） ----
    def _forward(self, frame_bgr):
        torch, cv2 = self.torch, self.cv2
        img = cv2.resize(frame_bgr, (self.size, self.size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x = torch.from_numpy(img).permute(2, 0, 1).float().div(255).unsqueeze(0).to(self.device)
        with torch.no_grad():
            # EMV/TGE 在模型内部完成增强，再过 YOLOv3 头
            out = self.model(x)        # 期望返回 [N,6] = x1,y1,x2,y2,conf,cls
            # 若模型还返回增强图 S̄，可解包：out, enhanced = self.model(x, return_enh=True)
        return self._postprocess(out, frame_bgr.shape[1], frame_bgr.shape[0])

    def _postprocess(self, out, W, H):
        dets = []
        try:
            arr = out[0].cpu().numpy() if hasattr(out, "__getitem__") else []
        except Exception:
            arr = []
        for d in arr:
            x1, y1, x2, y2, conf, cls = d[:6]
            if conf < self.conf:
                continue
            dets.append(Detection(
                cls=str(int(cls)), conf=float(conf),
                x=float(x1) / self.size, y=float(y1) / self.size,
                w=float(x2 - x1) / self.size, h=float(y2 - y1) / self.size,
            ))
        return dets

    def frames(self):
        idx = 0
        while True:
            ok, frame = self.cap.read()
            if not ok:
                break
            t0 = time.time()
            dets = self._forward(frame)
            dt = time.time() - t0
            yield FrameResult(
                frame_idx=idx, ts=time.time(), detections=dets,
                enhanced=True, fps=round(1 / dt, 1) if dt else None,
            )
            idx += 1

    def close(self):
        if self.cap:
            self.cap.release()
