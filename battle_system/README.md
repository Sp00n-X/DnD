# 战斗系统 Battle System

## 概述

战斗系统是一个独立的模块，提供了完整的回合制战斗逻辑，可以轻松集成到地图探索系统或其他游戏系统中。

## 架构

```
battle_system/
├── __init__.py          # 模块导出
├── battle_types.py      # 类型定义
├── battle_context.py    # 战斗上下文
├── battle_ui.py         # 战斗界面
├── battle_engine.py     # 战斗引擎核心
├── demo_battle.py       # 演示程序
└── README.md           # 说明文档
```

## 核心组件

### 1. BattleEngine (战斗引擎)
- 核心战斗逻辑处理
- 支持回合制战斗
- 集成Boss技能系统
- 装备效果触发
- 状态效果管理

### 2. BattleContext (战斗上下文)
- 存储战斗状态
- 管理战斗日志
- 处理状态效果
- 计算战斗结果

### 3. BattleUI (战斗界面)
- 用户交互界面
- 显示战斗信息
- 处理玩家输入
- 格式化输出

### 4. BattleTypes (类型定义)
- 枚举类型定义
- 数据结构定义
- 配置选项

## 使用方法

### 基本用法

```python
from battle_system import BattleEngine, BattleConfig
from characters.base_character import BaseCharacter

# 创建玩家和敌人
player = BaseCharacter("勇者", level=10)
enemy = BaseCharacter("哥布林", level=5)

# 创建战斗引擎
config = BattleConfig(allow_flee=True, show_detailed_log=True)
battle = BattleEngine(player, enemy, config)

# 开始战斗
result = battle.start_battle()
print(f"战斗结果: {result}")
```

### 集成到地图系统

```python
from battle_system import BattleEngine
from enemy.bosses.boss_manager import BossManager

# 在地图系统中使用
def encounter_enemy(player, enemy):
    battle = BattleEngine(player, enemy)
    result = battle.start_battle()
    
    if result == "victory":
        # 处理胜利奖励
        summary = battle.get_battle_summary()
        exp_gained = summary["rewards"]["experience"]
        player.gain_experience(exp_gained)
```

### 自定义配置

```python
config = BattleConfig(
    allow_flee=True,        # 允许逃跑
    show_detailed_log=True, # 显示详细日志
    auto_battle=False,      # 自动战斗
    turn_limit=100         # 回合限制
)
```

## 功能特性

### 1. 回合制战斗
- 玩家回合和敌人回合交替进行
- 支持普通攻击、防御、技能使用
- 状态效果系统（灼烧、中毒、眩晕等）

### 2. Boss技能系统
- 集成现有的Boss技能系统
- 支持多种攻击模式
- 智能技能选择

### 3. 装备效果
- 自动触发装备特效
- 支持多种效果类型
- 与战斗系统无缝集成

### 4. 战斗日志
- 详细的战斗记录
- 支持战斗回放
- 便于调试和分析

### 5. 奖励系统
- 经验值奖励
- 金币奖励
- 物品掉落

## 扩展接口

### 添加新的战斗行动
```python
# 在 battle_types.py 中添加新的 BattleAction
class BattleAction(Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    SKILL = "skill"
    ITEM = "item"
    FLEE = "flee"
    NEW_ACTION = "new_action"  # 新增行动
```

### 添加新的状态效果
```python
# 在 battle_context.py 中添加新的状态效果处理
def apply_status_effects(self):
    # 在现有基础上添加新的状态效果处理
    if effect_name == "freeze":
        # 处理冰冻效果
        pass
```

### 自定义战斗界面
```python
# 继承 BattleUI 类并重写方法
class CustomBattleUI(BattleUI):
    def display_battle_start(self):
        # 自定义战斗开始界面
        pass
```

## 演示程序

运行演示程序查看战斗系统效果：

```bash
cd battle_system
python demo_battle.py
```

演示包含：
1. 简单战斗 - 基础战斗流程
2. Boss战斗 - 集成Boss技能系统
3. 自动战斗 - 快速测试

## 集成指南

### 1. 与地图系统集成
- 在地图探索中遇到敌人时创建 BattleEngine 实例
- 战斗结束后根据结果更新地图状态
- 处理战斗奖励和状态更新

### 2. 与角色系统集成
- 确保角色类继承自 BaseCharacter
- 实现必要的方法（is_alive, take_damage等）
- 集成技能和装备系统

### 3. 与敌人系统集成
- 支持普通敌人和Boss
- Boss需要实现 select_action 和 execute_action 方法
- 普通敌人使用基础攻击逻辑

## 注意事项

1. **依赖关系**：确保所有依赖模块已正确导入
2. **角色类**：玩家和敌人需要继承自 BaseCharacter
3. **Boss类**：Boss需要实现完整的技能系统接口
4. **装备效果**：确保装备效果类有正确的接口

## 未来扩展

- [ ] 物品系统
- [ ] 多人战斗
- [ ] 战斗动画
- [ ] AI战斗策略
- [ ] 战斗回放系统
- [ ] PVP战斗模式
