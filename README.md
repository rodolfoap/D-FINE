# D-FINE Inference

A streamlined inference implementation of **D-FINE** (Redefine Regression Task of DETRs as Fine-grained Distribution Refinement), based on the official PyTorch implementation of the paper [arXiv:2410.13842](https://arxiv.org/abs/2410.13842).

This is a **fork adapted for pure inference** — all training code, data loading, and evaluation utilities have been removed. Only the essentials for running object detection inference remain.

## What is D-FINE?

D-FINE is a real-time object detection framework built on Detection Transformers (DETRs). It redefines bounding box regression as Fine-grained Distribution Refinement (FDR) and includes Global Optimal Localization Self-Distillation (GO-LSD) for improved accuracy.

**Model Variants:**
- **D-FINE-N**: 4M params, 42.8% AP
- **D-FINE-S**: 8M params, 46.2% AP
- **D-FINE-M**: 17M params, 50.1% AP
- **D-FINE-L**: 31M params, 53.3% AP
- **D-FINE-X**: 62M params, 55.8% AP

All trained on MS COCO dataset.

## Quick Start

### Setup

```bash
# Create environment
conda create -n dfine python=3.11.9
conda activate dfine
pip install -r requirements.txt
```

### Run Inference

```bash
# Inference on sample image (auto-downloads model)
./inference

# Custom image
python tools/inference/torch_inf.py \
  -c configs/dfine/dfine_hgnetv2_l_coco.yml \
  -r dfine_l_coco.pth \
  --input your_image.jpg \
  -d cuda:0
```

**Arguments:**
- `-c, --config` — Model config file
- `-r, --resume` — Checkpoint file path
- `-i, --input` — Input image or video file
- `-d, --device` — Device (default: `cpu`, use `cuda:0` for GPU)

**Supported Models:** n, s, m, l, x (change in `inference` script or config path)

**Supported Inputs:** JPG, PNG, BMP (images), MP4 (video)

## How It Works

1. **Load Config** → YAML configuration defines model architecture
2. **Load Checkpoint** → Pre-trained weights (auto-downloaded on first run)
3. **Build Model** → Instantiate backbone (HGNetv2) + encoder + decoder
4. **Deploy Mode** → Convert to inference-optimized mode
5. **Process Input** → Resize to 640×640, normalize, run detection
6. **Post-process** → Extract boxes, scores, labels; scale back to original size
7. **Output** → Bounding boxes with confidence scores saved as `torch_results.jpg`

## Project Structure

```
D-FINE/
├── configs/              # Model configurations
│   └── dfine/           # D-FINE model configs (n/s/m/l/x sizes)
├── src/
│   ├── core/            # Config loading system (YAMLConfig)
│   ├── nn/
│   │   ├── backbone/    # HGNetv2 backbone networks
│   │   └── postprocessor/ # Output post-processing
│   └── zoo/
│       └── dfine/       # D-FINE model implementation
│           ├── dfine.py              # Main model class
│           ├── dfine_decoder.py      # Transformer decoder (FDR)
│           ├── hybrid_encoder.py     # Feature fusion encoder
│           ├── postprocessor.py      # Box decoding & filtering
│           └── *.py                  # Utilities (box ops, denoising, etc.)
├── tools/
│   ├── inference/
│   │   ├── torch_inf.py    # Inference script
│   │   └── requirements.txt # Minimal dependencies
│   └── dataset/horse.jpg    # Sample image for testing
├── inference             # Quick-run shell script
├── Dockerfile           # Container setup
└── requirements.txt     # Python dependencies
```

## Files

- **Config Files** (`configs/`) — YAML configurations for each model size. Base model config includes architecture parameters (layers, channels, attention heads).
- **Model Code** (`src/zoo/dfine/`) — Complete D-FINE architecture: backbone, multi-scale encoder, transformer decoder with FDR, and output processor.
- **Inference Script** (`tools/inference/torch_inf.py`) — Main entry point. Loads config, checkpoint, and model; processes images/videos.
- **Quick Script** (`inference`) — Bash wrapper that auto-downloads the L model and runs on sample image.

## Device Usage

By default, inference runs on **CPU**. To use GPU:

```bash
./inference              # CPU
python ... -d cuda:0     # GPU 0
python ... -d cuda:1     # GPU 1
```

The script prints which device is being used.

## Model Downloads

Pre-trained checkpoints are automatically downloaded from GitHub releases on first run:
```
https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_[n|s|m|l|x]_coco.pth
```

~120MB for L model. Subsequent runs use cached checkpoint.

## Output

Detection results are saved as:
- `torch_results.jpg` — Image with drawn bounding boxes, labels, and confidence scores
- `torch_results.mp4` — Video with detections (if input is video)

Confidence threshold is configurable (default: 0.4).

## References

- Original Paper: [Redefine Regression Task of DETRs as Fine-grained Distribution Refinement](https://arxiv.org/abs/2410.13842)
- Official Repository: [D-FINE on GitHub](https://github.com/Peterande/D-FINE)
