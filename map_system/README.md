# 艾兰提亚世界地图系统

## 📁 目录结构
```
map_system/
├── map_system.py      # 主地图系统
├── demo_map.py        # 演示脚本
├── MAP_SYSTEM_GUIDE.md # 详细指南
├── README.md          # 本文件
└── start_map.sh       # 启动脚本
```

## 🚀 快速开始

### 启动交互式地图
```bash
./start_map.sh
```

### 运行演示
```bash
python3 demo_map.py
```

### 集成到项目
```python
from map_system import AetheriaMap

world = AetheriaMap()
world.move_to("齿轮之城")
```

## 🎯 核心功能

- **四大区域导航**: 齿轮之城、秘法之乡、翡翠之森、天穹武朝
- **子区域探索**: 每个主区域包含多个子区域
- **路径规划**: 自动计算最短路径
- **等级适配**: 基于玩家等级推荐区域
- **命令行界面**: 直观的交互体验

## 📖 使用示例

```bash
$ ./start_map.sh
[🗺️  裂星集] > look
[🗺️  裂星集] > go 齿轮之城
[🗺️  齿轮之城] > where
[🗺️  齿轮之城] > help
```

## 🔗 与现有系统集成

地图系统可以轻松集成到现有的D&D框架中，支持：
- 基于位置的遭遇生成
- 区域等级限制
- 任务地点管理
- NPC位置追踪
