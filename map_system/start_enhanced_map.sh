#!/bin/bash
# 启动增强版艾兰提亚世界地图系统

echo "🗺️  启动增强版艾兰提亚世界地图系统..."
echo "📍 支持主区域和子区域导航！"
echo ""

# 确保Python路径正确
export PYTHONPATH="${PYTHONPATH}:$(dirname "$0")"

# 运行增强版地图系统
python3 "$(dirname "$0")/enhanced_map_system.py"
