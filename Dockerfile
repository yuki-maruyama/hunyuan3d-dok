FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# OpenGL含めてインストール + キャッシュ削除
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.10 python3-pip git wget curl \
        libgl1-mesa-glx libglib2.0-0 \
        libopengl0 libglx0 libegl1 \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# PyTorch (CPU wheel使ってサイズ削減 - ランタイムでCUDA使う)
RUN pip3 install --no-cache-dir \
        torch torchvision --index-url https://download.pytorch.org/whl/cu121 \
    && rm -rf /root/.cache

# その他依存
RUN pip3 install --no-cache-dir \
        transformers accelerate safetensors \
        trimesh pillow requests numpy huggingface_hub hy3dgen \
    && rm -rf /root/.cache

RUN mkdir -p /opt/artifact

# モデルを事前ダウンロード（起動時間短縮のため）
RUN python3 -c "\
from huggingface_hub import snapshot_download; \
snapshot_download('tencent/Hunyuan3D-2mini', allow_patterns=['hunyuan3d-dit-v2-mini/*', '*.json'])"

COPY generate.py /app/generate.py

ENTRYPOINT ["python3", "/app/generate.py"]
