#!/usr/bin/env python3
"""D-FINE detector - raw performance mode (no Kafka/RTSP overhead)"""

import os
import sys
import torch
import cv2
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))

from src.core import YAMLConfig

# Config
device = os.getenv("DEVICE", "cuda:0" if torch.cuda.is_available() else "cpu").strip()
model_size = os.getenv("MODEL_SIZE", "l").strip()
conf_thresh = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
input_addr = os.getenv("MEIA_INPUT_ADDRESS", "/data/video.mp4").strip()

print(f"Device: {device}, Model: {model_size}, Threshold: {conf_thresh}, Input: {input_addr}")

# Download model
model_file = f"dfine_{model_size}_coco.pth"
if not os.path.exists(model_file):
    url = f"https://github.com/Peterande/storage/releases/download/dfinev1.0/{model_file}"
    print(f"Downloading {model_file}...")
    os.system(f"wget -q '{url}'")

# Load model
cfg = YAMLConfig(f"configs/dfine/dfine_hgnetv2_{model_size}_coco.yml", resume=model_file)
if "HGNetv2" in cfg.yaml_cfg:
    cfg.yaml_cfg["HGNetv2"]["pretrained"] = False

checkpoint = torch.load(model_file, map_location=device, weights_only=True)
state = checkpoint.get("ema", {}).get("module") or checkpoint["model"]
cfg.model.load_state_dict(state)

model = cfg.model.deploy().to(device).eval()
postprocessor = cfg.postprocessor.deploy()

print(f"Model loaded on {device}")

# Open video file
cap = cv2.VideoCapture(input_addr)
if not cap.isOpened():
    print(f"ERROR: Cannot open {input_addr}")
    sys.exit(1)

fps_video = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Video: {fps_video:.1f} FPS nominal, {total_frames} frames")

frame_count = 0
last_time = time.time()
fps = 0
times_infer = []

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        h, w = frame.shape[:2]

        # Inference
        img = cv2.resize(frame, (640, 640))
        img_t = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float().to(device) / 255.0
        size = torch.tensor([[w, h]], dtype=torch.float32).to(device)

        t_start_infer = time.time()
        with torch.no_grad(), torch.amp.autocast('cuda'):
            outputs = model(img_t)
            labels, boxes, scores = postprocessor(outputs, size)
        t_end_infer = time.time()

        infer_time = (t_end_infer - t_start_infer) * 1000
        times_infer.append(infer_time)

        # Unpack batch
        labels = labels[0]
        boxes = boxes[0]
        scores = scores[0]

        # Count detections above threshold
        num_dets = (scores >= conf_thresh).sum().item()

        # Print every 30 frames
        if frame_count % 30 == 0:
            now = time.time()
            elapsed = now - last_time
            if elapsed > 0:
                fps = 30 / elapsed
            avg_infer = sum(times_infer[-30:]) / len(times_infer[-30:])
            print(f"Frame {frame_count}/{total_frames}: {num_dets} dets | FPS: {fps:.1f} | infer avg: {avg_infer:.1f}ms", flush=True)

except KeyboardInterrupt:
    print("\nInterrupted")
finally:
    cap.release()

# Final summary
if times_infer:
    avg_infer = sum(times_infer) / len(times_infer)
    min_infer = min(times_infer)
    max_infer = max(times_infer)
    theoretical_fps = 1000 / avg_infer
    print(f"\n=== PERFORMANCE SUMMARY ===")
    print(f"Total frames: {frame_count}")
    print(f"Inference time: avg={avg_infer:.2f}ms, min={min_infer:.2f}ms, max={max_infer:.2f}ms")
    print(f"Theoretical FPS: {theoretical_fps:.1f} FPS")
