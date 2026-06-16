FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy inference tools requirements
COPY tools/inference/requirements.txt tools/inference/requirements.txt
RUN pip install --no-cache-dir -r tools/inference/requirements.txt

# Copy project code
COPY . .

# Default command: run inference script (model downloaded at runtime)
CMD ["bash", "inference"]
