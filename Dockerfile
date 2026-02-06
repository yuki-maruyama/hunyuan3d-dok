FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/models

# 基本パッケージ
RUN apt-get update && apt-get install -y \
    python3.10 python3-pip python3.10-venv git wget curl \
    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係
RUN pip3 install --no-cache-dir \
    torch torchvision --index-url https://download.pytorch.org/whl/cu121

RUN pip3 install --no-cache-dir \
    transformers accelerate safetensors \
    trimesh pillow requests numpy huggingface_hub

# hy3dgen (Hunyuan3D)
RUN pip3 install --no-cache-dir hy3dgen

# 作業ディレクトリ
WORKDIR /app

# モデルを事前ダウンロード (ビルド時にDL → イメージに含める)
RUN python3 -c "\
from huggingface_hub import snapshot_download; \
snapshot_download('tencent/Hunyuan3D-2mini', local_dir='/app/models/hunyuan3d-2mini')"

COPY generate.py /app/generate.py

# 成果物ディレクトリ
RUN mkdir -p /opt/artifact

ENTRYPOINT ["python3", "/app/generate.py"]
