# 增强版艾兰提亚世界地图系统使用指南

## 🚀 快速开始

### 启动系统
```bash
cd map_system
./start_enhanced_map.sh
```

### 基本导航流程
1. 从裂星集开始
2. 前往四大主区域之一
3. 在主区域中探索子区域
4. 在子区域间自由移动
5. 随时返回主区域

## 🎯 核心功能

### 主区域导航
- **裂星集**: 起始点，连接所有主区域
- **齿轮之城**: 真空管科技都市
- **秘法之乡**: 魔法圣地
- **翡翠之森**: 精灵森林
- **天穹武朝**: 武道圣地

### 子区域系统
每个主区域包含多个子区域，具有：
- 独立等级范围
- 专属敌人列表
- 特色战利品
- 区域背景故事
- 内部连接网络

## 🎮 使用示例

### 交互式命令
```bash
# 查看当前位置
look

# 前往主区域
go 翡翠之森

# 查看可探索子区域
where
# 输出: 可前往: 裂星集, 探索:苔阶聚落, 探索:环居, 探索:苔堡, 探索:星辉池, 探索:远古圣林

# 进入子区域（必须使用完整格式）
go 探索:星辉池

# 查看子区域详情
look

# 返回主区域
go 返回翡翠之森

# 查看所有子区域
regions

# 查看已探索记录
discovered
```

### 程序化使用
```python
from enhanced_map_system import EnhancedAetheriaMap

# 创建地图实例
world = EnhancedAetheriaMap()

# 导航到主区域
world.move_to("齿轮之城")

# 进入子区域
world.enter_sub_region("七炉议会")

# 获取子区域信息
info = world.get_current_location_info()
print(f"区域: {info['name']}")
print(f"等级: {info['level_range']}")
print(f"敌人: {info['enemies']}")
print(f"战利品: {info['loot']}")

# 返回主区域
world.exit_sub_region()
```

## 📊 子区域等级分布

### 齿轮之城
| 子区域 | 等级范围 | 特色 |
|--------|----------|------|
| 废弃雾根 | 5-10 | 锈蚀机械，古代零件 |
| 黑扳手总部 | 8-12 | 工人反抗，改装工具 |
| 天空码头 | 7-13 | 飞梭起降，走私货物 |
| 七炉议会 | 10-15 | 权力中枢，真空管核心 |
| 以太发电厂 | 12-18 | 能源核心，以太电池 |

### 秘法之乡
| 子区域 | 等级范围 | 特色 |
|--------|----------|------|
| 第一塔·星尘 | 1-5 | 初级法术，星尘研究 |
| 以太实验室 | 3-8 | 魔法实验，以太结晶 |
| 星桥 | 5-10 | 连接各塔，星图碎片 |
| 禁书库 | 7-12 | 禁忌知识，古老卷轴 |
| 第五塔·星图 | 10-15 | 高级法术，星图运算 |
| 第九塔·螺旋顶点 | 15-20 | 最高魔法，9阶法术 |

### 翡翠之森
| 子区域 | 等级范围 | 特色 |
|--------|----------|------|
| 苔阶聚落 | 5-8 | 精灵亲和，自然魔法 |
| 星辉池 | 7-12 | 星辉装备，月光精华 |
| 环居 | 10-15 | 巨树环绕，精灵工艺 |
| 远古圣林 | 12-18 | 古老秘密，自然之力 |
| 苔堡 | 15-20 | 精灵议会，最高权限 |

### 天穹武朝
| 子区域 | 等级范围 | 特色 |
|--------|----------|------|
| 白虎竞技场 | 5-8 | 武道修炼，真气入门 |
| 青龙峰 | 7-12 | 青龙传承，身法训练 |
| 朱雀宫 | 10-15 | 朱雀秘法，内功心法 |
| 天剑壁 | 12-18 | 剑意领悟，剑痕传承 |
| 倒岳城 | 15-20 | 倒立城市，反重力修炼 |
| 赤霄剑冢 | 18-20 | 剑圣埋剑，最强剑意 |

## 🔗 系统集成

### 与角色系统结合
```python
# 根据角色等级推荐区域
def recommend_areas(character_level):
    recommendations = []
    
    # 检查所有子区域
    regions = ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"]
    for region in regions:
        sub_regions = get_sub_regions(region)
        for sub_name in sub_regions:
            class_name = get_sub_region_class(region, sub_name)
            if class_name:
                # 动态导入并实例化
                module = importlib.import_module(f'regions.{get_region_module(region)}.sub_regions')
                sub_region = getattr(module, class_name)()
                
                min_level, max_level = sub_region.level_range
                if min_level <= character_level <= max_level:
                    recommendations.append((region, sub_name, sub_region))
    
    return recommendations
```

### 与战斗系统结合
每个子区域提供：
- 敌人列表（用于战斗生成）
- 战利品列表（用于奖励系统）
- 区域特色（用于环境效果）

## 💡 使用技巧

1. **等级匹配**: 选择适合角色等级的子区域
2. **特色需求**: 注意各区域的特殊要求
3. **探索顺序**: 建议从低等级子区域开始
4. **记录追踪**: 使用`discovered`命令查看探索进度
5. **搜索功能**: 使用`search`快速找到特定地点

## 🎮 高级功能

### 子区域连接
子区域间存在内部连接，支持：
- 区域内快速移动
- 等级递进式探索
- 故事线连续性

### 动态内容
- 根据角色等级调整敌人强度
- 基于探索历史解锁新内容
- 区域状态影响可获取战利品

## 📞 故障排除

### 常见问题
1. **无法进入子区域**: 确保已在对应的主区域中
2. **类导入错误**: 检查子区域名称拼写
3. **路径问题**: 确保从map_system目录运行

### 调试命令
```bash
# 测试子区域系统
python3 demo_enhanced_navigation.py

# 查看所有子区域
python3 -c "from regions import get_sub_regions; print(get_sub_regions('齿轮之城'))"

# 测试特定子区域
python3 -c "from regions.gearhaven.sub_regions import SevenFurnaceParliament; s=SevenFurnaceParliament(); print(s.name, s.level_range)"
