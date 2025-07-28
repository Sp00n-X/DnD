#!/usr/bin/env python3
"""
测试enemy模块的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enemy.boss_manager import BossManager
from enemy.floor_boss import FloorBoss

def test_enemy_module():
    """测试enemy模块"""
    print("=== 测试Enemy模块 ===")
    
    # 测试BossManager
    print("\n1. 测试BossManager:")
    boss_manager = BossManager()
    
    print(f"总层数: {boss_manager.get_total_floors()}")
    
    # 获取所有Boss信息
    for floor in range(1, boss_manager.get_total_floors() + 1):
        boss_info = boss_manager.get_boss_info(floor)
        if boss_info:
            print(f"第{floor}层: {boss_info['name']} (等级{boss_info['level']})")
            print(f"  HP: {boss_info['hp']}/{boss_info['max_hp']}")
            print(f"  攻击: {boss_info['attack']}, 防御: {boss_info['defense']}")
    
    # 测试FloorBoss
    print("\n2. 测试FloorBoss:")
    boss = boss_manager.get_boss(1)
    print(f"Boss名称: {boss.name}")
    print(f"Boss状态: {boss.get_status()}")
    
    # 测试伤害
    print("\n3. 测试伤害系统:")
    initial_hp = boss.hp
    boss.take_damage(20)
    print(f"受到伤害前HP: {initial_hp}")
    print(f"受到伤害后HP: {boss.hp}")
    print(f"Boss是否存活: {boss.is_alive()}")
    
    # 测试重置
    print("\n4. 测试重置功能:")
    boss.reset()
    print(f"重置后HP: {boss.hp}")
    print(f"重置后状态: {boss.get_status()}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_enemy_module()
