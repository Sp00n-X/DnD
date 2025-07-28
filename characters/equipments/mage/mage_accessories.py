"""
法师专用饰品
包含戒指、护符、徽章等法师特色饰品
"""

from ..base_equipments import Armor, EquipSlot, Stat, PercentModifier, EquipmentEffect
from typing import List


class ManaRegenerationEffect(EquipmentEffect):
    """法力回复效果：每回合恢复一定法力值"""
    
    def __init__(self, mana_per_turn: int = 5):
        self.mana_per_turn = mana_per_turn
    
    def on_hit(self, attacker, target):
        # 这个效果会在回合结束时触发
        pass


class SpellCritEffect(EquipmentEffect):
    """法术暴击效果：法术攻击有几率造成暴击"""
    
    def __init__(self, crit_chance: float = 0.15, crit_damage: float = 1.5):
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
    
    def on_hit(self, attacker, target):
        # 这个效果会在法术攻击时触发
        pass


class ArcanePowerEffect(EquipmentEffect):
    """奥术之力效果：提升法术强度"""
    
    def __init__(self, spell_power_boost: int = 10):
        self.spell_power_boost = spell_power_boost
    
    def on_hit(self, attacker, target):
        # 这个效果会在战斗开始时触发
        pass


class SpellWeavingEffect(EquipmentEffect):
    """法术编织效果：连续施法时提升伤害"""
    
    def __init__(self, damage_increase_per_cast: float = 0.05, max_stacks: int = 5):
        self.damage_increase_per_cast = damage_increase_per_cast
        self.max_stacks = max_stacks
    
    def on_hit(self, attacker, target):
        # 这个效果会在施法时触发
        pass


# ----------------------------------------
# 法师饰品定义
# ----------------------------------------

class ApprenticeRing(Armor):
    """学徒指环 - 初级法师的基础饰品"""
    
    def __init__(self):
        super().__init__(
            name="学徒指环",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.05),
                PercentModifier(Stat.MP, 0.10)
            ],
            effects=[],
            level_requirement=1
        )


class ManaCrystal(Armor):
    """法力水晶 - 提供法力回复的饰品"""
    
    def __init__(self):
        super().__init__(
            name="法力水晶",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.MP, 0.20),
                PercentModifier(Stat.SPELL_POWER, 0.08)
            ],
            effects=[
                ManaRegenerationEffect(mana_per_turn=3)
            ],
            level_requirement=3
        )


class ArcaneSeal(Armor):
    """奥术印章 - 提升法术暴击的饰品"""
    
    def __init__(self):
        super().__init__(
            name="奥术印章",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.15),
                PercentModifier(Stat.MP, 0.15)
            ],
            effects=[
                SpellCritEffect(crit_chance=0.10, crit_damage=1.3)
            ],
            level_requirement=5
        )


class ElementalFocus(Armor):
    """元素聚焦器 - 增强元素法术的饰品"""
    
    def __init__(self):
        super().__init__(
            name="元素聚焦器",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.25),
                PercentModifier(Stat.MP, 0.20)
            ],
            effects=[
                ArcanePowerEffect(spell_power_boost=15),
                SpellWeavingEffect(damage_increase_per_cast=0.03, max_stacks=3)
            ],
            level_requirement=7
        )


class ArchmageInsignia(Armor):
    """大法师徽章 - 顶级法师的终极饰品"""
    
    def __init__(self):
        super().__init__(
            name="大法师徽章",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.35),
                PercentModifier(Stat.MP, 0.30),
                PercentModifier(Stat.DEFENSE, 0.10)
            ],
            effects=[
                ManaRegenerationEffect(mana_per_turn=8),
                SpellCritEffect(crit_chance=0.20, crit_damage=1.5),
                ArcanePowerEffect(spell_power_boost=25)
            ],
            level_requirement=10
        )


class MysticAmulet(Armor):
    """神秘护符 - 提供平衡属性的饰品"""
    
    def __init__(self):
        super().__init__(
            name="神秘护符",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.12),
                PercentModifier(Stat.MP, 0.15),
                PercentModifier(Stat.DEFENSE, 0.08)
            ],
            effects=[
                ManaRegenerationEffect(mana_per_turn=2)
            ],
            level_requirement=4
        )


class SpellweaverCharm(Armor):
    """织法者护符 - 专为连续施法设计的饰品"""
    
    def __init__(self):
        super().__init__(
            name="织法者护符",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.18),
                PercentModifier(Stat.MP, 0.12)
            ],
            effects=[
                SpellWeavingEffect(damage_increase_per_cast=0.05, max_stacks=5)
            ],
            level_requirement=6
        )


class FrozenTalisman(Armor):
    """寒冰护符 - 冰系法师的专精饰品"""
    
    def __init__(self):
        super().__init__(
            name="寒冰护符",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.20),
                PercentModifier(Stat.MP, 0.10)
            ],
            effects=[
                ArcanePowerEffect(spell_power_boost=10)
            ],
            level_requirement=5
        )


class FireRuby(Armor):
    """火焰红宝石 - 火系法师的专精饰品"""
    
    def __init__(self):
        super().__init__(
            name="火焰红宝石",
            slot=EquipSlot.ACCESSORY,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.22),
                PercentModifier(Stat.MP, 0.08)
            ],
            effects=[
                SpellCritEffect(crit_chance=0.12, crit_damage=1.4)
            ],
            level_requirement=6
        )


# 预定义饰品实例
apprentice_ring = ApprenticeRing()
mana_crystal = ManaCrystal()
arcane_seal = ArcaneSeal()
elemental_focus = ElementalFocus()
archmage_insignia = ArchmageInsignia()
mystic_amulet = MysticAmulet()
spellweaver_charm = SpellweaverCharm()
frozen_talisman = FrozenTalisman()
fire_ruby = FireRuby()

# 按等级分类的饰品列表
MAGE_ACCESSORIES_BY_LEVEL = {
    1: [apprentice_ring],
    3: [mana_crystal],
    4: [mystic_amulet],
    5: [arcane_seal, frozen_talisman],
    6: [spellweaver_charm, fire_ruby],
    7: [elemental_focus],
    10: [archmage_insignia]
}

# 所有法师饰品列表
ALL_MAGE_ACCESSORIES = [
    apprentice_ring,
    mana_crystal,
    arcane_seal,
    elemental_focus,
    archmage_insignia,
    mystic_amulet,
    spellweaver_charm,
    frozen_talisman,
    fire_ruby
]
