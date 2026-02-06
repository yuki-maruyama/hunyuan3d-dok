FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/models
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# 全部1レイヤーにまとめる (最小イメージサイズ)
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.10 python3-pip git wget curl \
        libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir \
        torch torchvision --index-url https://download.pytorch.org/whl/cu121 \
    && pip3 install --no-cache-dir \
        transformers accelerate safetensors \
        trimesh pillow requests numpy huggingface_hub hy3dgen \
    && python3 -c "\
from huggingface_hub import snapshot_download; \
snapshot_download('tencent/Hunyuan3D-2mini', local_dir='/app/models/hunyuan3d-2mini')" \
    && rm -rf /root/.cache/pip \
    && mkdir -p /opt/artifact

COPY generate.py /app/generate.py

ENTRYPOINT ["python3", "/app/generate.py"]
