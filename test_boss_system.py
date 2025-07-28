#!/usr/bin/env python3
"""测试新的Boss系统 - 哥布林厨师长技能演示"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enemy import BossManager
from characters.base_character import BaseCharacter

def test_goblin_chef_boss():
    """测试哥布林厨师长的技能系统"""
    print("=== 哥布林厨师长技能系统测试 ===\n")
    
    # 创建Boss管理器
    boss_manager = BossManager()
    
    # 获取哥布林厨师长
    goblin_chef = boss_manager.get_boss(1)
    
    if not goblin_chef:
        print("错误：无法获取哥布林厨师长")
        return
    
    print(f"Boss信息: {goblin_chef.get_status()}")
    print(f"攻击模式: {goblin_chef.attack_pattern.name}")
    print()
    
    # 显示技能信息
    print("可用技能:")
    for skill_info in goblin_chef.get_skills_info():
        status = "可用" if skill_info['can_use'] else f"冷却中({skill_info['current_cooldown']})"
        print(f"  {skill_info['name']} - MP: {skill_info['mp_cost']} - {status}")
        print(f"    {skill_info['description']}")
    print()
    
    # 创建测试玩家
    player = BaseCharacter("测试玩家", 3)
    player.base_hp = 100
    player.base_attack = 20
    player.base_defense = 5
    player.recalc_stats()
    player.hp = player.max_hp
    
    print(f"玩家信息: {player.name} - HP: {player.hp}/{player.max_hp}")
    print()
    
    # 模拟战斗回合
    print("=== 模拟战斗回合 ===")
    for turn in range(5):
        print(f"\n--- 回合 {turn + 1} ---")
        
        # Boss选择动作
        action = goblin_chef.select_action(player)
        
        # 执行动作
        result = goblin_chef.execute_action(action)
        print(result['message'])
        
        if 'damage' in result:
            print(f"造成伤害: {result['damage']}")
        
        if 'heal_amount' in result:
            print(f"恢复生命: {result['heal_amount']}")
        
        if 'burn_applied' in result and result['burn_applied']:
            print("目标被灼烧！")
        
        if 'poison_applied' in result and result['poison_applied']:
            print("目标中毒了！")
        
        if 'stun_applied' in result and result['stun_applied']:
            print("目标被眩晕！")
        
        # 显示当前状态
        print(f"Boss状态: HP {goblin_chef.hp}/{goblin_chef.max_hp}, MP {goblin_chef.mp}")
        print(f"玩家状态: HP {player.hp}/{player.max_hp}")
        
        # 处理状态效果
        if hasattr(player, 'status_manager'):
            player.status_manager.tick()
        
        if hasattr(goblin_chef, 'status_manager'):
            goblin_chef.status_manager.tick()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_goblin_chef_boss()
