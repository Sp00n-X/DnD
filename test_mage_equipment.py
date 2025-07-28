#!/usr/bin/env python3
"""
法师装备系统测试文件
演示法师专用装备的使用和效果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from characters.base_character import BaseCharacter
from characters.equipments.mage.mage_weapons import *
from characters.equipments.mage.mage_armors import *
from characters.equipments.mage.mage_accessories import *


def test_mage_equipment():
    """测试法师装备系统"""
    print("=== 法师装备系统测试 ===\n")
    
    # 创建一个法师角色
    mage = BaseCharacter("测试法师")
    print(f"创建法师角色: {mage.name}")
    print(f"初始属性: HP={mage.hp}, MP={mage.mp}, 攻击={mage.attack}, 防御={mage.defense}, 法强={mage.spell_power}")
    
    print("\n" + "="*50)
    print("1. 测试法师武器")
    print("="*50)
    
    # 测试装备武器
    print("\n装备学徒法杖:")
    mage.equip(apprentice_staff)
    print(f"装备后属性: 法强={mage.spell_power}, MP={mage.mp}")
    
    print("\n装备水晶球(副手):")
    mage.equip(crystal_orb)
    print(f"装备后属性: 法强={mage.spell_power}, MP={mage.mp}")
    
    print("\n装备奥术法杖:")
    mage.unequip_slot(apprentice_staff.slot)  # 卸下学徒法杖
    mage.equip(arcane_staff)
    print(f"装备后属性: 法强={mage.spell_power}, MP={mage.mp}, 攻击={mage.attack}")
    
    print("\n" + "="*50)
    print("2. 测试法师防具")
    print("="*50)
    
    # 测试装备防具
    print("\n装备学徒法袍:")
    mage.equip(apprentice_robe)
    print(f"装备后属性: 防御={mage.defense}, MP={mage.mp}")
    
    print("\n装备丝绸长裤:")
    mage.equip(silk_trousers)
    print(f"装备后属性: 防御={mage.defense}, MP={mage.mp}")
    
    print("\n装备奥术长袍:")
    mage.unequip_slot(apprentice_robe.slot)  # 卸下学徒法袍
    mage.equip(arcane_robes)
    print(f"装备后属性: 防御={mage.defense}, MP={mage.mp}, 法强={mage.spell_power}")
    
    print("\n" + "="*50)
    print("3. 测试法师饰品")
    print("="*50)
    
    # 测试装备饰品
    print("\n装备学徒指环:")
    mage.equip(apprentice_ring)
    print(f"装备后属性: 法强={mage.spell_power}, MP={mage.mp}")
    
    print("\n装备法力水晶:")
    mage.equip(mana_crystal)
    print(f"装备后属性: 法强={mage.spell_power}, MP={mage.mp}")
    
    print("\n装备大法师徽章:")
    mage.unequip_slot(apprentice_ring.slot)  # 卸下学徒指环
    mage.equip(archmage_insignia)
    print(f"装备后属性: 法强={mage.spell_power}, MP={mage.mp}, 防御={mage.defense}")
    
    print("\n" + "="*50)
    print("4. 完整装备测试")
    print("="*50)
    
    # 装备完整套装
    mage.unequip_slot(EquipSlot.MAIN_HAND)
    mage.unequip_slot(EquipSlot.OFF_HAND)
    mage.unequip_slot(EquipSlot.UPPER)
    mage.unequip_slot(EquipSlot.LOWER)
    mage.unequip_slot(EquipSlot.ACCESSORY)
    
    print("\n装备完整套装:")
    mage.equip(archmage_staff)
    mage.equip(crystal_orb)  # 副手
    mage.equip(archmage_robes)
    mage.equip(mystic_legwraps)
    mage.equip(archmage_insignia)
    
    print(f"最终属性:")
    print(f"HP: {mage.hp}")
    print(f"MP: {mage.mp}")
    print(f"攻击: {mage.attack}")
    print(f"防御: {mage.defense}")
    print(f"法术强度: {mage.spell_power}")
    
    print("\n" + "="*50)
    print("5. 装备列表展示")
    print("="*50)
    
    print(f"\n所有法师武器 ({len(ALL_MAGE_WEAPONS)}件):")
    for weapon in ALL_MAGE_WEAPONS:
        print(f"  - {weapon.name} (等级{weapon.level_requirement})")
    
    print(f"\n所有法师防具 ({len(ALL_MAGE_ARMORS)}件):")
    for armor in ALL_MAGE_ARMORS:
        print(f"  - {armor.name} (等级{armor.level_requirement})")
    
    print(f"\n所有法师饰品 ({len(ALL_MAGE_ACCESSORIES)}件):")
    for accessory in ALL_MAGE_ACCESSORIES:
        print(f"  - {accessory.name} (等级{accessory.level_requirement})")
    
    print("\n" + "="*50)
    print("6. 按等级分类展示")
    print("="*50)
    
    for level in range(1, 11):
        weapons = MAGE_WEAPONS_BY_LEVEL.get(level, [])
        armors = MAGE_ARMORS_BY_LEVEL.get(level, [])
        accessories = MAGE_ACCESSORIES_BY_LEVEL.get(level, [])
        
        if weapons or armors or accessories:
            print(f"\n等级 {level} 可用装备:")
            for w in weapons:
                print(f"  武器: {w.name}")
            for a in armors:
                print(f"  防具: {a.name}")
            for acc in accessories:
                print(f"  饰品: {acc.name}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_mage_equipment()
