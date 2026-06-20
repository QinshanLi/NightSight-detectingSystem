"""
成员A离线工具：用论文模型把视频跑成 event_labels.json（replay 模式数据源）。
有 GPU 时也可先离线跑好，演示当天用 replay 零延迟回放。

用法：
  python scripts_offline_infer.py --video data/event_stream_v1.mp4 --out data/event_labels.json
"""
import argparse, json
from app.inference.emv_yolo import EMVYoloInference


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", default="data/event_labels.json")
    args = ap.parse_args()

    infer = EMVYoloInference(source=args.video)
    frames = []
    for fr in infer.frames():
        frames.append({
            "frame_idx": fr.frame_idx,
            "lux": fr.lux,
            "detections": [d.__dict__ for d in fr.detections],
        })
    infer.close()
    json.dump({"fps": 25, "video": args.video, "frames": frames},
              open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"已写出 {len(frames)} 帧 → {args.out}")


if __name__ == "__main__":
    main()
