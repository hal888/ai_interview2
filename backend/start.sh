#!/bin/bash

# 启动后端服务

# 进入脚本所在目录
cd "$(dirname "$0")"

# 检查是否安装了pip3
if ! command -v pip3 &> /dev/null
then
    echo "pip3 未安装，请先安装pip3"
    exit 1
fi

# 检查是否安装了python3
if ! command -v python3 &> /dev/null
then
    echo "python3 未安装，请先安装python3"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
pip3 install -r requirements.txt

# 启动服务
echo "启动后端服务..."
python3 run.py