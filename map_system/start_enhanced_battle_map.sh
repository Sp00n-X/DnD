#!/bin/bash
# 启动增强版地图战斗系统

echo "🗺️ 启动增强版艾兰提亚世界地图系统（集成战斗）"
echo "================================================"

# 确保Python路径正确
export PYTHONPATH="${PYTHONPATH}:$(dirname "$(pwd)")"

# 启动系统
python3 enhanced_map_system.py
