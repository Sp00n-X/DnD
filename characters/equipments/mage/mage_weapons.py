"""
法师专用武器
包含各种法杖、魔典、水晶球等法师特色武器
"""

from ..base_equipments import Weapon, EquipSlot, Stat, PercentModifier, DamageType, DamageEffect, EquipmentEffect
from typing import List


class ManaSurgeEffect(EquipmentEffect):
    """法力涌动效果：攻击时有几率恢复法力值"""
    
    def __init__(self, chance: float = 0.3, mana_restore: int = 10):
        self.chance = chance
        self.mana_restore = mana_restore
    
    def on_hit(self, attacker, target):
        import random
        if random.random() < self.chance:
            attacker.mp = min(attacker.mp + self.mana_restore, attacker.max_mp)
            print(f"[法力涌动] {attacker.name} 恢复了 {self.mana_restore} 点法力值!")


class SpellVampEffect(EquipmentEffect):
    """法术吸血效果：造成的法术伤害的一部分转化为生命值"""
    
    def __init__(self, vamp_ratio: float = 0.15):
        self.vamp_ratio = vamp_ratio
    
    def on_hit(self, attacker, target):
        # 这个效果会在技能系统中处理
        pass


class ArcaneExplosionEffect(EquipmentEffect):
    """奥术爆炸效果：攻击时有几率造成额外的范围伤害"""
    
    def __init__(self, chance: float = 0.25, damage_scale: float = 0.5):
        self.chance = chance
        self.damage_scale = damage_scale
    
    def on_hit(self, attacker, target):
        import random
        if random.random() < self.chance:
            damage = int(attacker.spell_power * self.damage_scale)
            print(f"[奥术爆炸] {attacker.name} 引发了奥术爆炸，造成 {damage} 点额外魔法伤害!")


# ----------------------------------------
# 法师武器定义
# ----------------------------------------

class ApprenticeStaff(Weapon):
    """学徒法杖 - 初级法师的标准装备"""
    
    def __init__(self):
        super().__init__(
            name="学徒法杖",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.15),
                PercentModifier(Stat.MP, 0.10)
            ],
            effects=[],
            level_requirement=1
        )


class CrystalOrb(Weapon):
    """水晶球 - 增强法术威力的副手装备"""
    
    def __init__(self):
        super().__init__(
            name="水晶球",
            slot=EquipSlot.OFF_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.20),
                PercentModifier(Stat.MP, 0.05)
            ],
            effects=[
                ManaSurgeEffect(chance=0.2, mana_restore=5)
            ],
            level_requirement=3
        )


class ArcaneStaff(Weapon):
    """奥术法杖 - 中级法师的强力武器"""
    
    def __init__(self):
        super().__init__(
            name="奥术法杖",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.30),
                PercentModifier(Stat.MP, 0.15),
                PercentModifier(Stat.ATTACK, 0.10)
            ],
            effects=[
                ArcaneExplosionEffect(chance=0.25, damage_scale=0.4)
            ],
            level_requirement=5
        )


class ElementalStaff(Weapon):
    """元素法杖 - 掌控元素之力的强大武器"""
    
    def __init__(self):
        super().__init__(
            name="元素法杖",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.40),
                PercentModifier(Stat.MP, 0.20)
            ],
            effects=[
                DamageEffect(
                    scale_stat=Stat.SPELL_POWER,
                    coefficient=0.3,
                    dmg_type=DamageType.MAGICAL
                ),
                ManaSurgeEffect(chance=0.3, mana_restore=8)
            ],
            level_requirement=8
        )


class ArchmageStaff(Weapon):
    """大法师之杖 - 顶级法师的终极武器"""
    
    def __init__(self):
        super().__init__(
            name="大法师之杖",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.60),
                PercentModifier(Stat.MP, 0.30),
                PercentModifier(Stat.ATTACK, 0.20)
            ],
            effects=[
                ArcaneExplosionEffect(chance=0.35, damage_scale=0.6),
                ManaSurgeEffect(chance=0.4, mana_restore=15),
                DamageEffect(
                    scale_stat=Stat.SPELL_POWER,
                    coefficient=0.5,
                    dmg_type=DamageType.MAGICAL
                )
            ],
            level_requirement=10
        )


class SpellbookOfPower(Weapon):
    """力量法典 - 古老的魔法书，蕴含强大魔力"""
    
    def __init__(self):
        super().__init__(
            name="力量法典",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.35),
                PercentModifier(Stat.MP, 0.25)
            ],
            effects=[
                SpellVampEffect(vamp_ratio=0.15)
            ],
            level_requirement=6
        )


class MysticWand(Weapon):
    """神秘魔杖 - 小巧但威力不俗的魔法武器"""
    
    def __init__(self):
        super().__init__(
            name="神秘魔杖",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.25),
                PercentModifier(Stat.MP, 0.10)
            ],
            effects=[
                ManaSurgeEffect(chance=0.25, mana_restore=10)
            ],
            level_requirement=4
        )


class FrozenHeartStaff(Weapon):
    """寒冰之心法杖 - 冰系法师的专精武器"""
    
    def __init__(self):
        super().__init__(
            name="寒冰之心法杖",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.45),
                PercentModifier(Stat.MP, 0.15)
            ],
            effects=[
                DamageEffect(
                    scale_stat=Stat.SPELL_POWER,
                    coefficient=0.2,
                    dmg_type=DamageType.MAGICAL
                )
            ],
            level_requirement=7
        )


class FirelordStaff(Weapon):
    """火焰之王法杖 - 火系法师的终极武器"""
    
    def __init__(self):
        super().__init__(
            name="火焰之王法杖",
            slot=EquipSlot.MAIN_HAND,
            percent_mods=[
                PercentModifier(Stat.SPELL_POWER, 0.50),
                PercentModifier(Stat.MP, 0.20)
            ],
            effects=[
                DamageEffect(
                    scale_stat=Stat.SPELL_POWER,
                    coefficient=0.3,
                    dmg_type=DamageType.MAGICAL
                ),
                ManaSurgeEffect(chance=0.3, mana_restore=12)
            ],
            level_requirement=9
        )


# 预定义武器实例
apprentice_staff = ApprenticeStaff()
crystal_orb = CrystalOrb()
arcane_staff = ArcaneStaff()
elemental_staff = ElementalStaff()
archmage_staff = ArchmageStaff()
spellbook_of_power = SpellbookOfPower()
mystic_wand = MysticWand()
frozen_heart_staff = FrozenHeartStaff()
firelord_staff = FirelordStaff()

# 按等级分类的武器列表
MAGE_WEAPONS_BY_LEVEL = {
    1: [apprentice_staff],
    3: [crystal_orb],
    4: [mystic_wand],
    5: [arcane_staff],
    6: [spellbook_of_power],
    7: [frozen_heart_staff],
    8: [elemental_staff],
    9: [firelord_staff],
    10: [archmage_staff]
}

# 所有法师武器列表
ALL_MAGE_WEAPONS = [
    apprentice_staff,
    crystal_orb,
    arcane_staff,
    elemental_staff,
    archmage_staff,
    spellbook_of_power,
    mystic_wand,
    frozen_heart_staff,
    firelord_staff
]
