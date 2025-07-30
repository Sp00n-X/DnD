# 艾兰提亚世界地图系统

## 📁 目录结构

### 增强版系统（推荐）
```
map_system/
├── enhanced_map_system.py      # 增强版地图系统（支持子区域导航）
├── demo_enhanced_navigation.py # 增强版导航演示
├── start_enhanced_map.sh       # 增强版启动脚本
├── regions/                    # 四大区域子区域
│   ├── __init__.py            # 区域统一管理
│   ├── gearhaven/             # 齿轮之城
│   ├── selintar/              # 秘法之乡
│   ├── lothir/                # 翡翠之森
│   └── wulong/                # 天穹武朝
```

### 基础系统（兼容）
```
map_system/
├── map_system.py      # 基础地图系统
├── demo_map.py        # 基础地图演示
├── demo_sub_regions.py # 子区域演示
├── start_map.sh       # 基础启动脚本
└── regions/           # 四大区域子区域
    ├── __init__.py
    ├── gearhaven/     # 齿轮之城
    ├── selintar/      # 秘法之乡
    ├── lothir/        # 翡翠之森
    └── wulong/        # 天穹武朝
```

## 🚀 快速开始

### 增强版地图系统（推荐）
```bash
./start_enhanced_map.sh     # 启动增强版地图系统
python3 demo_enhanced_navigation.py  # 增强版导航演示
```

### 基础地图系统
```bash
./start_map.sh              # 启动基础地图系统
python3 demo_map.py         # 基础地图演示
python3 demo_sub_regions.py # 子区域演示
```

### 集成到项目
```python
# 增强版地图系统（支持子区域导航）
from enhanced_map_system import EnhancedAetheriaMap

world = EnhancedAetheriaMap()
world.move_to("齿轮之城")           # 前往主区域
world.enter_sub_region("SevenFurnaceParliament")  # 进入子区域
world.exit_sub_region()            # 返回主区域

# 基础地图系统
from map_system import AetheriaMap
from regions import get_sub_regions, gearhaven, selintar, lothir, wulong

world = AetheriaMap()
world.move_to("齿轮之城")
sub_regions = get_sub_regions("齿轮之城")
parliament = gearhaven.SevenFurnaceParliament()
```

## 🎯 核心功能

### 主地图系统
- **四大区域导航**: 齿轮之城、秘法之乡、翡翠之森、天穹武朝
- **中心枢纽**: 裂星集作为起始点
- **路径规划**: 自动计算最短路径
- **等级适配**: 每个区域有推荐的等级范围

### 子区域系统
- **齿轮之城**: 5个详细子区域（七炉议会、黑扳手总部等）
- **秘法之乡**: 6个九塔子区域（第一塔·星尘、第五塔·星图等）
- **翡翠之森**: 5个精灵聚落（苔阶聚落、环居、苔堡等）
- **天穹武朝**: 6个九宫格山水（天剑壁、倒岳城、赤霄剑冢等）

### 区域特色
- **齿轮之城**: 真空管科技，机械敌人，以太科技装备
- **秘法之乡**: 阶梯魔法，星图研究，法术卷轴
- **翡翠之森**: 精灵亲和度，自然魔法，星辉装备
- **天穹武朝**: 真气需求，武道修炼，神兽传承

## 📊 等级分布

| 区域 | 等级范围 | 特色要求 |
|------|----------|----------|
| 齿轮之城 | 5-18 | 科技亲和 |
| 秘法之乡 | 1-20 | 魔法阶梯 |
| 翡翠之森 | 5-20 | 精灵亲和度1-5 |
| 天穹武朝 | 5-20 | 真气需求3-8 |

## 🔗 系统集成

### 子区域连接
每个区域的子区域都有内部连接网络，支持：
- 区域内导航
- 等级递进
- 特色要求验证
- 敌人/战利品系统

### 使用示例
```python
# 获取区域信息
from regions import get_sub_regions
sub_regions = get_sub_regions("齿轮之城")
# 返回: ['七炉议会', '黑扳手总部', '废弃雾根', '天空码头', '以太发电厂']

# 创建子区域实例
parliament = gearhaven.SevenFurnaceParliament()
print(f"等级: {parliament.level_range}")  # (10, 15)
print(f"敌人: {parliament.enemies}")      # ['机械守卫MK-III', ...]
print(f"战利品: {parliament.loot}")       # ['真空管核心', ...]
```

## 🎮 扩展使用

### 区域特色系统
- **精灵亲和度**: 翡翠之森独有，影响进入权限
- **真气需求**: 天穹武朝独有，影响修炼效果
- **魔法阶梯**: 秘法之乡独有，影响法术学习
- **科技等级**: 齿轮之城独有，影响装备使用

### 敌人与战利品
每个子区域都包含：
- 专属敌人列表
- 特色战利品
- 区域背景故事
- 连接关系网络

## 📞 支持

### 增强版系统文档
- 查看`ENHANCED_SYSTEM_GUIDE.md`获取增强版系统完整指南
- 运行`demo_enhanced_navigation.py`查看增强版演示
- 使用`./start_enhanced_map.sh`启动交互式增强版系统

### 基础系统文档
- 使用`help`命令获取内置帮助
- 查看`demo_sub_regions.py`获取子区域使用示例
- 阅读`MAP_SYSTEM_GUIDE.md`获取详细指南

## 🔄 版本对比

| 功能 | 基础版 | 增强版 |
|------|--------|--------|
| 主区域导航 | ✅ | ✅ |
| 子区域导航 | ❌ | ✅ |
| 交互式界面 | ✅ | ✅ |
| 子区域详情 | ❌ | ✅ |
| 等级推荐 | ❌ | ✅ |
| 探索记录 | ❌ | ✅ |
| 搜索功能 | 基础 | 增强 |
| 系统集成 | 手动 | 自动 |

## 🎯 推荐使用
**新手用户**: 直接使用增强版系统 `./start_enhanced_map.sh`
**开发者**: 参考增强版代码进行集成开发
