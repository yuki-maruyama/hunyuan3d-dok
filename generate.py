#!/usr/bin/env python3
"""
Hunyuan3D Generator for Sakura DOK
Usage: python generate.py --input <image_url_or_path> [--output output.glb]
"""
import os
import sys
import argparse
import requests
from io import BytesIO
from PIL import Image

# ローカルモデルパス (イメージに事前DL済み)
LOCAL_MODEL_PATH = "/app/models/hunyuan3d-2mini"

def download_image(url):
    """URLから画像をダウンロード"""
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

    # モデルロード (ローカルパスを優先)
    model_path = LOCAL_MODEL_PATH if os.path.exists(LOCAL_MODEL_PATH) else 'tencent/Hunyuan3D-2mini'
    print(f"Loading model from: {model_path}")
    
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(model_path)
    
    # 生成
    print("Generating 3D mesh...")
    mesh = pipeline(image=image)[0]
    
    # 出力先 (SAKURA_ARTIFACT_DIR を優先)
    artifact_dir = os.environ.get('SAKURA_ARTIFACT_DIR', '/opt/artifact')
    os.makedirs(artifact_dir, exist_ok=True)
    output_path = os.path.join(artifact_dir, args.output)
    
    # 保存
    mesh.export(output_path)
    print(f"Saved: {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")

if __name__ == '__main__':
    main()
