# DND 状态效果系统重构指南

## 概述

本次重构将原有的状态效果系统升级为更加强大、灵活和可扩展的新系统。新系统提供了统一的状态管理、丰富的状态类型、清晰的接口和完整的生命周期管理。

## 新系统特性

### 1. 统一的状态管理
- **StatusManager**: 集中管理所有角色的状态效果
- **BaseStatusEffect**: 所有状态效果的基类
- **状态生命周期**: 应用(on_apply) → 持续(on_tick) → 移除(on_remove)

### 2. 丰富的状态类型
- **DOT (持续伤害)**: 灼烧、中毒等
- **HOT (持续治疗)**: 持续恢复
- **BUFF (增益效果)**: 属性提升
- **DEBUFF (减益效果)**: 属性降低
- **CROWD_CONTROL (控制效果)**: 冰冻、眩晕等

### 3. 高级功能
- **状态叠加**: 支持层数叠加
- **状态互斥**: 防止冲突状态共存
- **优先级系统**: 控制状态处理顺序
- **刷新机制**: 重新施加时刷新持续时间

## 文件结构

```
chactors/
├── status_effects/
│   ├── __init__.py          # 导出所有状态效果
│   ├── base_status.py       # 状态效果基类
│   ├── status_manager.py    # 状态管理器
│   └── status_effects.py    # 具体状态效果实现
├── base_chactor.py          # 更新后的角色基类
├── skills/                  # 更新后的技能系统
└── statusinflicteffect/     # 更新后的装备效果系统
```

## 使用方法

### 1. 添加状态效果

```python
from chactors.status_effects import BurnEffect, DefenseBuffEffect

# 创建状态效果
burn = BurnEffect(duration=3, damage_per_turn=10)
defense_buff = DefenseBuffEffect(duration=3, defense_bonus=20)

# 添加到角色
character.add_status_effect(burn)
character.add_status_effect(defense_buff)
```

### 2. 更新状态效果

```python
# 每回合调用
results = character.update_status_effects()
for result in results:
    print(result['message'])
```

### 3. 检查状态效果

```python
# 检查是否拥有特定状态
if character.has_status_effect("灼烧"):
    print("角色处于灼烧状态")

# 获取所有状态
status_summary = character.get_status_effects()
print(status_summary)
```

### 4. 移除状态效果

```python
character.remove_status_effect("灼烧")
```

## 可用的状态效果

### 伤害类状态
- **BurnEffect**: 灼烧，每回合造成固定伤害
- **PoisonEffect**: 中毒，每回合造成百分比伤害

### 增益类状态
- **DefenseBuffEffect**: 防御强化，提升防御力
- **AttackBuffEffect**: 攻击强化，提升攻击力
- **HealOverTimeEffect**: 持续治疗，每回合恢复生命

### 控制类状态
- **FreezeEffect**: 冰冻，阻止行动
- **StunEffect**: 眩晕，阻止行动和施法

## 创建自定义状态效果

```python
from chactors.status_effects.base_status import BaseStatusEffect, StatusEffectData, StatusType, StatusPriority

class CustomEffect(BaseStatusEffect):
    def __init__(self, duration=3, power=10):
        data = StatusEffectData(
            name="自定义效果",
            duration=duration,
            max_stacks=5,
            refresh_on_reapply=True
        )
        super().__init__(data)
        self.power = power
    
    def get_status_type(self) -> StatusType:
        return StatusType.BUFF
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.MEDIUM
    
    def on_apply(self, character):
        # 应用效果时的逻辑
        character.attack += self.power * self.stacks
        return {"success": True, "message": f"{character.name} 攻击力提升 {self.power * self.stacks}"}
    
    def on_remove(self, character):
        # 移除效果时的逻辑
        character.attack -= self.power * self.stacks
        return {"success": True, "message": f"{character.name} 攻击力恢复"}
    
    def on_tick(self, character):
        # 每回合的逻辑
        result = super().on_tick(character)
        # 可以添加额外的每回合效果
        return result
```

## 装备集成

装备可以通过 `StatusInflictEffect` 类集成新的状态系统：

```python
from chactors.statusinflicteffect.base_inflicteffect import StatusInflictEffect
from chactors.status_effects import PoisonEffect

# 创建装备效果
poison_weapon = StatusInflictEffect(
    status_factory=lambda: PoisonEffect(duration=3, percent_per_turn=0.05),
    chance=0.3
)

# 添加到装备
weapon.effects.append(poison_weapon)
```

## 技能集成

技能可以直接使用新的状态效果：

```python
from chactors.skills.base_skill import Skill, SkillType
from chactors.status_effects import BurnEffect

class Fireball(Skill):
    def __init__(self):
        super().__init__(
            name="火球术",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=1,
            description="造成魔法伤害并附加灼烧"
        )
    
    def execute(self, caster, target=None):
        damage = 20 + caster.spell_power
        target.take_damage(damage)
        
        burn = BurnEffect(duration=2, damage_per_turn=5)
        target.add_status_effect(burn)
        
        return {
            "success": True,
            "message": f"火球术造成 {damage} 点伤害并附加灼烧"
        }
```

## 迁移指南

### 从旧系统迁移

1. **移除旧的状态效果类**: 删除旧的 `StatusEffect` 类
2. **更新角色类**: 使用新的 `StatusManager`
3. **更新技能**: 使用新的状态效果类
4. **更新装备**: 使用新的 `StatusInflictEffect`

### 兼容性

新系统完全向后兼容，可以逐步迁移，无需一次性替换所有代码。

## 最佳实践

1. **状态命名**: 使用清晰、描述性的状态名称
2. **持续时间**: 合理设置状态持续时间，避免过长或过短
3. **互斥规则**: 明确定义哪些状态不能共存
4. **优先级**: 为重要状态设置较高优先级
5. **测试**: 充分测试状态效果的叠加、刷新和移除逻辑

## 性能考虑

- 状态管理器使用高效的字典查找
- 状态更新采用批量处理
- 内存使用经过优化，适合大量角色

## 扩展性

系统设计支持轻松添加新的状态类型和功能：
- 新的状态类型可以通过继承 `BaseStatusEffect` 实现
- 新的状态管理功能可以通过扩展 `StatusManager` 实现
- 支持自定义状态行为和交互规则
