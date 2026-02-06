#!/usr/bin/env python3
"""
Hunyuan3D Generator for Sakura DOK
"""
import os
import sys
import argparse
import requests
from io import BytesIO
from PIL import Image

# ローカルモデルパス (HuggingFace形式で保存)
LOCAL_MODEL_PATH = "/app/models/tencent/Hunyuan3D-2mini"
HF_MODEL_ID = "tencent/Hunyuan3D-2mini"

def download_image(url):
    print(f"Downloading image from: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def main():
    parser = argparse.ArgumentParser(description='Generate 3D model from image')
    parser.add_argument('--input', '-i', required=True, help='Input image URL or path')
    parser.add_argument('--output', '-o', default='output.glb', help='Output filename')
    args = parser.parse_args()

    # 画像取得
    if args.input.startswith('http://') or args.input.startswith('https://'):
        image = download_image(args.input)
    else:
        image = Image.open(args.input)
    
    print(f"Image loaded: {image.size}")

    # モデルロード (HuggingFace IDを使う - ローカルにキャッシュ済み)
    print(f"Loading model: {HF_MODEL_ID}")
    
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(HF_MODEL_ID)
    
    # 生成
    print("Generating 3D mesh...")
    mesh = pipeline(image=image)[0]
    
    # 出力先
    artifact_dir = os.environ.get('SAKURA_ARTIFACT_DIR', '/opt/artifact')
    os.makedirs(artifact_dir, exist_ok=True)
    output_path = os.path.join(artifact_dir, args.output)
    
    mesh.export(output_path)
    print(f"Saved: {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")

if __name__ == '__main__':
    main()
