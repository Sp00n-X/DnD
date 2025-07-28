from __future__ import annotations
from abc import ABC
from typing import Dict, List, Optional, Callable
from enum import Enum, auto
from dataclasses import dataclass, field
import random


# ----------------------------------------
# 1. 数据枚举
# ----------------------------------------
class Stat(Enum):
    HP          = auto()
    ATTACK      = auto()
    DEFENSE     = auto()
    MP          = auto()
    SPELL_POWER = auto()

class EquipSlot(Enum):
    MAIN_HAND  = auto()
    OFF_HAND   = auto()
    UPPER      = auto()
    LOWER      = auto()
    ACCESSORY  = auto()

class DamageType(Enum):
    PHYSICAL = auto()
    MAGICAL  = auto()

# ----------------------------------------
# 2. 百分比修饰
# ----------------------------------------
@dataclass(frozen=True)
class PercentModifier:
    stat: Stat            # 作用属性
    percent: float        # +0.20 → +20%，-0.1 → -10%

# ----------------------------------------
# 3. 装备效果系统
# ----------------------------------------
class EquipmentEffect(ABC):
    """所有可触发的装备效果基类"""
    def on_hit(self) -> None: ...

@dataclass
class DamageEffect(EquipmentEffect):
    scale_stat: Stat              # 伤害随哪个属性成长
    coefficient: float            # 与属性的倍率
    dmg_type: DamageType

    def on_hit(self, attacker, target):
        raw = getattr(attacker, self.scale_stat.name.lower())
        damage = int(raw * self.coefficient)
        target.take_damage(damage, self.dmg_type)
        print(f"[效果] {attacker.name} 的装备追加 {damage} {self.dmg_type.name} 伤害!")



# ----------------------------------------
# 4. 装备基类
# ----------------------------------------
class Equipment:
    def __init__(self,
                 name: str,
                 slot: EquipSlot,
                 percent_mods: List[PercentModifier] | None = None,
                 effects: List[EquipmentEffect] | None = None,
                 level_requirement: int = 1):
        self.name              = name
        self.slot              = slot
        self.percent_mods      = percent_mods or []
        self.effects           = effects or []
        self.level_requirement = level_requirement


# Weapon/Armor 只是对合法槽位做检查
class Weapon(Equipment):
    def __init__(self, *args, **kwargs):
        slot = kwargs.get("slot")
        if slot not in (EquipSlot.MAIN_HAND, EquipSlot.OFF_HAND):
            raise ValueError("Weapon slot 必须是手持位")
        super().__init__(*args, **kwargs)

class Armor(Equipment):
    def __init__(self, *args, **kwargs):
        slot = kwargs.get("slot")
        if slot not in (EquipSlot.UPPER, EquipSlot.LOWER, EquipSlot.ACCESSORY):
            raise ValueError("Armor slot 不正确")
        super().__init__(*args, **kwargs)


# ----------------------------------------
# 6. 一个示例状态
# ----------------------------------------
@dataclass
class StatusEffect:
    name: str
    duration: int
# # ----------------------------------------
# # 8. 快速演示
# # ----------------------------------------
# if __name__ == "__main__":
#     alice = BaseCharacter("Alice")
#     bob   = BaseCharacter("Bob")

#     alice.equip(berserker_axe)
#     alice.equip(corrosion_amulet)

#     alice.attack_target(bob)
#     print(f"Bob 当前 HP = {bob.hp}")