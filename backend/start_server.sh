#!/bin/bash

# SQL Agent 后端启动脚本

export OPENAI_API_KEY="sk-proj-xxx"
export OPENAI_BASE_URL="https://ai.devtool.tech/proxy/v1"

# 禁用 CUDA 和 transformers 编译
export CUDA_VISIBLE_DEVICES=""
export TRANSFORMERS_OFFLINE=1
export TF_CPP_MIN_LOG_LEVEL=3

# 禁用不必要的警告
export PYTHONWARNINGS="ignore"

echo "===================================="
echo "SQL Agent 后端服务启动中..."
echo "===================================="
echo "API Key: ${OPENAI_API_KEY:0:20}..."
echo "Base URL: $OPENAI_BASE_URL"
echo "===================================="

cd "$(dirname "$0")"
python api_with_db.py

