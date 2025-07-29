# Boss系统升级指南

## 概述
本次升级将哥布林厨师长Boss改造为具备随机技能使用能力的智能敌人，并为所有敌人类设计了灵活的攻击模式系统。

## 新增功能

### 1. 攻击模式系统 (enemy/attack_patterns.py)
- **AttackPattern基类**: 所有攻击模式的抽象基类
- **RandomSkillPattern**: 随机选择可用技能
- **SequentialSkillPattern**: 按顺序循环使用技能
- **PrioritySkillPattern**: 根据血量等条件优先选择技能
- **EnragedPattern**: 低血量时进入狂暴状态

### 2. Boss技能系统 (enemy/boss_skills.py)
哥布林厨师长专属技能：
- **🔥辛辣调料**: 火属性伤害，50%几率灼烧
- **☠️腐烂食材**: 毒属性伤害，100%几率中毒
- **🍳烹饪狂怒**: 提升自身攻击力15点，持续3回合
- **👨‍🍳厨师特技**: 高伤害，30%几率眩晕
- **🥘剩菜炖锅**: 恢复生命值

### 3. 增强的FloorBoss类 (enemy/floor_boss.py)
- 支持技能系统
- 支持多种攻击模式
- 技能冷却管理
- 状态效果集成

### 4. 升级后的BossManager (enemy/boss_manager.py)
- 自动为Boss配置技能和攻击模式
- 提供详细的Boss信息查询

## 使用示例

### 获取Boss信息
```python
from enemy import BossManager

boss_manager = BossManager()
goblin_chef = boss_manager.get_boss(1)

# 查看技能
for skill in goblin_chef.get_skills_info():
    print(f"{skill['name']}: {skill['description']}")
```

### 战斗中使用
```python
# Boss选择并执行动作
action = goblin_chef.select_action(player)
result = goblin_chef.execute_action(action)
print(result['message'])
```

## 技能效果说明

| 技能名称 | 类型 | MP消耗 | 冷却 | 效果 |
|---------|------|--------|------|------|
| 辛辣调料 | 火属性攻击 | 10 | 2回合 | 32伤害，50%灼烧 |
| 腐烂食材 | 毒属性攻击 | 15 | 3回合 | 38伤害，100%中毒 |
| 烹饪狂怒 | 增益 | 20 | 4回合 | 攻击力+15，3回合 |
| 厨师特技 | 终极技能 | 30 | 5回合 | 58伤害，30%眩晕 |
| 剩菜炖锅 | 治疗 | 15 | 3回合 | 恢复40生命值 |

## 攻击模式特性

### 随机技能模式
- 70%概率使用技能
- 从可用技能中随机选择
- 考虑MP和冷却时间

### 其他模式（为其他Boss准备）
- **顺序模式**: 按固定顺序循环技能
- **优先级模式**: 根据血量选择治疗/防御/攻击
- **狂暴模式**: 低血量时优先使用高伤害技能

## 扩展指南

### 添加新Boss技能
1. 继承`Skill`类
2. 实现`execute`方法
3. 添加到对应Boss的技能列表

### 创建新攻击模式
1. 继承`AttackPattern`类
2. 实现`select_action`方法
3. 为Boss设置新的攻击模式

### 示例：添加新Boss
```python
# 创建新Boss
new_boss = FloorBoss(6, "火焰巨龙", 12, 400, 50, 25)

# 添加技能
from .boss_skills import create_dragon_skills
new_boss.add_skills(create_dragon_skills())

# 设置攻击模式
from .attack_patterns import EnragedPattern
new_boss.set_attack_pattern(EnragedPattern(enrage_threshold=0.3))
