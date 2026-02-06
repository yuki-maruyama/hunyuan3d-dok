#!/usr/bin/env python3
"""
Hunyuan3D Generator for Sakura DOK
"""
import os
import sys
import traceback

# ログをアーティファクトに保存
artifact_dir = os.environ.get('SAKURA_ARTIFACT_DIR', '/opt/artifact')
os.makedirs(artifact_dir, exist_ok=True)
log_path = os.path.join(artifact_dir, 'run.log')

class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    def flush(self):
        for f in self.files:
            f.flush()

log_file = open(log_path, 'w')
sys.stdout = Tee(sys.stdout, log_file)
sys.stderr = Tee(sys.stderr, log_file)

def main():
    import argparse
    import requests
    from io import BytesIO
    from PIL import Image
    
    HF_MODEL_ID = "tencent/Hunyuan3D-2mini"
    
    parser = argparse.ArgumentParser(description='Generate 3D model from image')
    parser.add_argument('--input', '-i', required=True, help='Input image URL or path')
    parser.add_argument('--output', '-o', default='output.glb', help='Output filename')
    args = parser.parse_args()

    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    
    # 画像取得
    if args.input.startswith('http://') or args.input.startswith('https://'):
        print(f"Downloading image from: {args.input}")
        response = requests.get(args.input, timeout=60)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
    else:
        image = Image.open(args.input)
    
    print(f"Image loaded: {image.size}, mode: {image.mode}")

    # モデルロード
    print(f"Loading model: {HF_MODEL_ID}")
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(HF_MODEL_ID)
    
    # 生成
    print("Generating 3D mesh...")
    mesh = pipeline(image=image)[0]
    
    # 出力
    output_path = os.path.join(artifact_dir, args.output)
    mesh.export(output_path)
    print(f"Saved: {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
    finally:
        log_file.close()
