"""
法师专用防具
包含法袍、护符等法师特色防具
"""

from ..base_equipments import Armor, EquipSlot, Stat, PercentModifier, EquipmentEffect
from typing import List


class ManaShieldEffect(EquipmentEffect):
    """法力护盾效果：受到伤害时消耗法力值来减少伤害"""
    
    def __init__(self, reduction_ratio: float = 0.3, mana_cost_ratio: float = 0.5):
        self.reduction_ratio = reduction_ratio
        self.mana_cost_ratio = mana_cost_ratio
    
    def on_hit(self, attacker, target):
        # 这个效果会在战斗系统中处理
        pass


class ArcaneBarrierEffect(EquipmentEffect):
    """奥术屏障效果：提升法术抗性"""
    
    def __init__(self, spell_resistance: int = 15):
        self.spell_resistance = spell_resistance
    
    def on_hit(self, attacker, target):
        # 这个效果会在战斗系统中处理
        pass


# ----------------------------------------
# 法师防具定义
# ----------------------------------------

class ApprenticeRobe(Armor):
    """学徒法袍 - 初级法师的基础防具"""
    
    def __init__(self):
        super().__init__(
            name="学徒法袍",
            slot=EquipSlot.UPPER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.10),
                PercentModifier(Stat.MP, 0.15)
            ],
            effects=[],
            level_requirement=1
        )


class MysticCloak(Armor):
    """神秘斗篷 - 提供额外法力值的防具"""
    
    def __init__(self):
        super().__init__(
            name="神秘斗篷",
            slot=EquipSlot.UPPER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.20),
                PercentModifier(Stat.MP, 0.25),
                PercentModifier(Stat.SPELL_POWER, 0.10)
            ],
            effects=[
                ArcaneBarrierEffect(spell_resistance=10)
            ],
            level_requirement=4
        )


class ArcaneRobes(Armor):
    """奥术长袍 - 中级法师的防具"""
    
    def __init__(self):
        super().__init__(
            name="奥术长袍",
            slot=EquipSlot.UPPER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.25),
                PercentModifier(Stat.MP, 0.30),
                PercentModifier(Stat.SPELL_POWER, 0.15)
            ],
            effects=[
                ManaShieldEffect(reduction_ratio=0.2, mana_cost_ratio=0.4)
            ],
            level_requirement=6
        )


class ElementalVestments(Armor):
    """元素法衣 - 高级法师的防具"""
    
    def __init__(self):
        super().__init__(
            name="元素法衣",
            slot=EquipSlot.UPPER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.35),
                PercentModifier(Stat.MP, 0.35),
                PercentModifier(Stat.SPELL_POWER, 0.20)
            ],
            effects=[
                ArcaneBarrierEffect(spell_resistance=20),
                ManaShieldEffect(reduction_ratio=0.25, mana_cost_ratio=0.3)
            ],
            level_requirement=8
        )


class ArchmageRobes(Armor):
    """大法师之袍 - 顶级法师的终极防具"""
    
    def __init__(self):
        super().__init__(
            name="大法师之袍",
            slot=EquipSlot.UPPER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.50),
                PercentModifier(Stat.MP, 0.50),
                PercentModifier(Stat.SPELL_POWER, 0.30)
            ],
            effects=[
                ArcaneBarrierEffect(spell_resistance=30),
                ManaShieldEffect(reduction_ratio=0.35, mana_cost_ratio=0.25)
            ],
            level_requirement=10
        )


class SilkTrousers(Armor):
    """丝绸长裤 - 提供基础防护的下装"""
    
    def __init__(self):
        super().__init__(
            name="丝绸长裤",
            slot=EquipSlot.LOWER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.15),
                PercentModifier(Stat.MP, 0.10)
            ],
            effects=[],
            level_requirement=2
        )


class EnchantedLeggings(Armor):
    """附魔护腿 - 中级法师的下装"""
    
    def __init__(self):
        super().__init__(
            name="附魔护腿",
            slot=EquipSlot.LOWER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.25),
                PercentModifier(Stat.MP, 0.20)
            ],
            effects=[],
            level_requirement=5
        )


class MysticLegwraps(Armor):
    """神秘裹腿 - 高级法师的下装"""
    
    def __init__(self):
        super().__init__(
            name="神秘裹腿",
            slot=EquipSlot.LOWER,
            percent_mods=[
                PercentModifier(Stat.DEFENSE, 0.35),
                PercentModifier(Stat.MP, 0.25),
                PercentModifier(Stat.SPELL_POWER, 0.10)
            ],
            effects=[],
            level_requirement=8
        )


# 预定义防具实例
apprentice_robe = ApprenticeRobe()
mystic_cloak = MysticCloak()
arcane_robes = ArcaneRobes()
elemental_vestments = ElementalVestments()
archmage_robes = ArchmageRobes()
silk_trousers = SilkTrousers()
enchanted_leggings = EnchantedLeggings()
mystic_legwraps = MysticLegwraps()

# 按等级分类的防具列表
MAGE_ARMORS_BY_LEVEL = {
    1: [apprentice_robe],
    2: [silk_trousers],
    4: [mystic_cloak],
    5: [enchanted_leggings],
    6: [arcane_robes],
    8: [elemental_vestments, mystic_legwraps],
    10: [archmage_robes]
}

# 所有法师防具列表
ALL_MAGE_ARMORS = [
    apprentice_robe,
    mystic_cloak,
    arcane_robes,
    elemental_vestments,
    archmage_robes,
    silk_trousers,
    enchanted_leggings,
    mystic_legwraps
]
