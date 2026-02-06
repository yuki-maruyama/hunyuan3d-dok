#!/bin/bash
# Hunyuan3D DOK Task Runner

# 設定
API_BASE="https://secure.sakura.ad.jp/cloud/zone/is1a/api/managed-container/1.0"
IMAGE="ghcr.io/yuki-maruyama/hunyuan3d-dok:latest"

# 引数チェック
if [ -z "$1" ]; then
    echo "Usage: $0 <image_url>"
    exit 1
fi

INPUT_URL="$1"
TASK_NAME="hunyuan3d-$(date +%Y%m%d-%H%M%S)"

# タスク作成
echo "Creating task: $TASK_NAME"
RESPONSE=$(usacloud rest request "${API_BASE}/tasks/" \
    --method POST \
    -d "{
        \"name\": \"${TASK_NAME}\",
        \"containers\": [{
            \"image\": \"${IMAGE}\",
            \"command\": [\"--input\", \"${INPUT_URL}\"],
            \"plan\": \"v100-32gb\"
        }],
        \"tags\": [\"hunyuan3d\", \"auto\"]
    }" 2>&1)

echo "$RESPONSE" | jq .

# タスクID取得
TASK_ID=$(echo "$RESPONSE" | jq -r '.id')
echo "Task ID: $TASK_ID"
