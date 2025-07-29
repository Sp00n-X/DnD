# 艾兰提亚世界地图系统指南

## 🗺️ 系统概述

这是一个基于命令行的D&D地图导航系统，专为艾兰提亚世界设计。系统支持：
- 四大区域间的无缝导航
- 子区域探索
- 路径规划
- 地点搜索
- 等级适配建议

## 🚀 快速开始

### 方法1：交互式命令行
```bash
python3 map_system.py
```

### 方法2：集成到现有系统
```python
from map_system import AetheriaMap

# 创建地图实例
world = AetheriaMap()

# 获取当前位置信息
info = world.get_current_location_info()
print(info)

# 移动到指定位置
world.move_to("齿轮之城")
```

## 🎯 核心功能

### 1. 世界结构
- **裂星集** - 中心枢纽，所有冒险的起点
- **齿轮之城** - 科技都市，真空管科技巅峰
- **秘法之乡** - 魔法圣地，九塔倒悬
- **翡翠之森** - 精灵领地，800年寿命奥秘
- **天穹武朝** - 武道圣地，九宫格山水

### 2. 地点类型
- **Hub**: 中心枢纽，连接所有区域
- **City**: 城市区域，科技/商业发达
- **Magical**: 魔法区域，法术研究
- **Forest**: 森林区域，自然魔法
- **Martial**: 武道区域，真气修炼

### 3. 等级范围
每个区域都有推荐的等级范围：
- 裂星集: 1-20 (全等级)
- 齿轮之城: 5-15
- 秘法之乡: 3-18
- 翡翠之森: 7-20
- 天穹武朝: 4-17

## 🔧 命令行使用

### 基础命令
```
look                    - 查看当前位置详细信息
go [地点]               - 前往指定位置
map                     - 显示世界地图
path [地点]             - 显示到指定位置的路径
where                   - 显示当前位置和可前往地点
discovered              - 显示已发现的地点
search [关键词]         - 搜索地点
help                    - 显示帮助信息
quit/exit               - 退出系统
```

### 使用示例
```
[🗺️  裂星集] > look
📍 当前位置: 裂星集
📝 描述: 中立城寨，四国交汇的冒险者聚集地
🔗 可前往: 齿轮之城, 秘法之乡, 翡翠之森, 天穹武朝

[🗺️  裂星集] > go 齿轮之城
✅ 已前往: 齿轮之城

[🗺️  齿轮之城] > look
📍 当前位置: 齿轮之城
📝 描述: 阿斯图里亚 - 云层都市，真空管科技巅峰
🏛️ 子区域:
   • 七炉议会: 齿轮城最高权力机构...
   • 黑扳手总部: 工人行会秘密基地...
   • 废弃雾根: 地表废弃区域...
```

## 🔄 系统集成

### 与战斗系统集成
```python
# 基于位置的遭遇生成
location_encounters = {
    "齿轮之城": ["机械守卫", "黑扳手间谍", "以太电流泄漏"],
    "秘法之乡": ["星图研究员", "阶梯法师", "以太病感染者"],
    "翡翠之森": ["精灵哨兵", "星辉兽", "母树守卫"],
    "天穹武朝": ["真气武者", "剑圣传人", "巨构守卫"]
}

# 获取当前位置遭遇
current_location = world.current_location
encounters = location_encounters.get(current_location, [])
```

### 与任务系统集成
```python
# 基于等级的区域限制
player_level = 8
for loc_name, loc_data in world.map_data.items():
    level_range = loc_data.get("level_range", "1-20")
    min_level, max_level = map(int, level_range.split("-"))
    
    if min_level <= player_level <= max_level:
        print(f"{loc_name}: 适合探索")
```

## 📊 地图数据结构

### 地点信息结构
```python
{
    "name": "地点名称",
    "description": "详细描述",
    "type": "地点类型",
    "connections": ["可前往的地点列表"],
    "lore": "背景故事",
    "level_range": "推荐等级范围",
    "coordinates": (x, y),  # 地图坐标
    "sub_locations": {
        "子区域名称": "子区域描述"
    }
}
```

## 🎮 扩展建议

### 1. 添加更多子区域
```python
# 在地图数据中增加更多子区域
"sub_locations": {
    "新区域": "新区域描述",
    "隐藏区域": "需要特殊条件才能进入"
}
```

### 2. 添加传送门/快速旅行
```python
# 添加特殊连接
"connections": ["正常连接", "传送门:特殊地点"]
```

### 3. 添加天气/时间影响
```python
# 扩展地点数据
"weather_effects": {
    "雨天": "影响某些法术",
    "夜晚": "出现特殊敌人"
}
```

### 4. 添加商店/服务
```python
# 添加服务信息
"services": {
    "商店": ["装备", "药水"],
    "训练师": ["技能升级", "职业转换"]
}
```

## 🛠️ 技术细节

### 依赖
- Python 3.6+
- 标准库 (cmd, json, os, sys)

### 文件结构
```
map_system.py      # 主地图系统
demo_map.py        # 演示脚本
start_map.sh       # 启动脚本
MAP_SYSTEM_GUIDE.md # 本指南
```

### 性能考虑
- 使用BFS算法进行路径查找
- 内存中存储所有地点数据
- 支持快速查询和导航

## 🎨 自定义

### 添加新地点
```python
# 在_initialize_world方法中添加
"新地点": {
    "description": "新地点描述",
    "connections": ["连接地点1", "连接地点2"],
    "type": "新类型",
    "coordinates": (x, y)
}
```

### 修改现有地点
直接编辑`map_system.py`中的`_initialize_world`方法即可。

## 📞 支持

如需帮助或建议，请查看：
- 使用`help`命令获取内置帮助
- 查看`demo_map.py`获取使用示例
- 阅读世界设定文档了解背景
