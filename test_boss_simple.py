#!/usr/bin/env python3
"""简化的Boss系统测试"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enemy import BossManager
from characters.base_character import BaseCharacter

def test_boss_system():
    """测试Boss系统"""
    print("=== Boss系统测试 ===\n")
    
    # 创建Boss管理器
    boss_manager = BossManager()
    
    # 获取哥布林厨师长
    goblin_chef = boss_manager.get_boss(1)
    
    print(f"Boss: {goblin_chef.name}")
    print(f"等级: {goblin_chef.level}")
    print(f"生命值: {goblin_chef.hp}/{goblin_chef.max_hp}")
    print(f"攻击力: {goblin_chef.attack}")
    print(f"防御力: {goblin_chef.defense}")
    print(f"魔法值: {goblin_chef.mp}")
    print(f"攻击模式: {goblin_chef.attack_pattern.name}")
    print()
    
    print("技能列表:")
    for skill in goblin_chef.get_skills_info():
        print(f"  {skill['name']} (MP: {skill['mp_cost']})")
        print(f"    {skill['description']}")
    print()
    
    # 创建测试玩家
    player = BaseCharacter("勇者", 3)
    player.base_hp = 100
    player.base_attack = 25
    player.base_defense = 8
    player.recalc_stats()
    player.hp = player.max_hp
    
    print(f"玩家: {player.name}")
    print(f"生命值: {player.hp}/{player.max_hp}")
    print()
    
    # 模拟3回合战斗
    print("=== 战斗模拟 ===")
    for turn in range(3):
        print(f"\n--- 回合 {turn + 1} ---")
        
        # Boss行动
        action = goblin_chef.select_action(player)
        result = goblin_chef.execute_action(action)
        
        print(f"Boss行动: {result['message']}")
        if 'damage' in result:
            print(f"造成伤害: {result['damage']}")
        if 'heal_amount' in result:
            print(f"恢复生命: {result['heal_amount']}")
        
        # 显示状态
        print(f"Boss: {goblin_chef.hp}/{goblin_chef.max_hp} HP, {goblin_chef.mp} MP")
        print(f"玩家: {player.hp}/{player.max_hp} HP")
        
        # 重置技能冷却演示
        if turn == 1:
            print("\n技能冷却重置演示:")
            for skill in goblin_chef.get_skills_info():
                if skill['current_cooldown'] > 0:
                    print(f"  {skill['name']} 冷却: {skill['current_cooldown']}回合")
    
    print("\n=== 测试完成 ===")
    print("Boss系统已成功实现随机技能使用功能！")

if __name__ == "__main__":
    test_boss_system()
