#!/usr/bin/env python3
"""测试新的状态效果系统"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chactors'))

from characters.base_character import BaseCharacter
from status_effects import (
    BurnEffect, PoisonEffect, FreezeEffect, 
    DefenseBuffEffect, AttackBuffEffect, HealOverTimeEffect
)
from characters.skills import Fireball, FrostBolt, DefenseBoost, ManaHeal


def test_status_effects():
    """测试状态效果系统"""
    print("=== 测试状态效果系统 ===")
    
    # 创建测试角色
    alice = BaseCharacter("Alice", level=5)
    bob = BaseCharacter("Bob", level=5)
    
    print(f"初始状态:")
    print(f"Alice: HP={alice.hp}/{alice.max_hp}, MP={alice.mp}/{alice.max_mp}")
    print(f"Bob: HP={bob.hp}/{bob.max_hp}, MP={bob.mp}/{bob.max_mp}")
    
    # 测试灼烧效果
    print("\n--- 测试灼烧效果 ---")
    burn = BurnEffect(duration=3, damage_per_turn=10)
    result = bob.add_status_effect(burn)
    print(f"添加灼烧效果: {result['message']}")
    
    # 测试中毒效果
    print("\n--- 测试中毒效果 ---")
    poison = PoisonEffect(duration=4, percent_per_turn=0.05)
    result = bob.add_status_effect(poison)
    print(f"添加中毒效果: {result['message']}")
    
    # 测试冰冻效果
    print("\n--- 测试冰冻效果 ---")
    freeze = FreezeEffect(duration=2)
    result = bob.add_status_effect(freeze)
    print(f"添加冰冻效果: {result['message']}")
    
    # 测试状态更新
    print("\n--- 测试状态更新 ---")
    for turn in range(1, 5):
        print(f"\n第{turn}回合:")
        results = bob.update_status_effects()
        for result in results:
            print(f"  {result['result']['message']}")
        
        print(f"  Bob状态: HP={bob.hp}/{bob.max_hp}")
        print(f"  当前状态: {bob.get_status_effects()['effects']}")
    
    # 测试防御强化
    print("\n--- 测试防御强化 ---")
    defense_buff = DefenseBuffEffect(duration=3, defense_bonus=20)
    result = alice.add_status_effect(defense_buff)
    print(f"添加防御强化: {result['message']}")
    print(f"Alice防御力: {alice.defense}")
    
    # 测试持续治疗
    print("\n--- 测试持续治疗 ---")
    heal_effect = HealOverTimeEffect(duration=3, heal_per_turn=15)
    result = alice.add_status_effect(heal_effect)
    print(f"添加持续治疗: {result['message']}")
    
    # 测试技能使用
    print("\n--- 测试技能使用 ---")
    alice.learn_skill(Fireball())
    alice.learn_skill(FrostBolt())
    alice.learn_skill(DefenseBoost())
    alice.learn_skill(ManaHeal())
    
    # 使用火球术
    result = alice.use_skill("火球术", target=bob)
    print(f"使用火球术: {result['message']}")
    print(f"Bob状态: HP={bob.hp}/{bob.max_hp}")
    
    # 使用防御强化
    result = alice.use_skill("防御强化")
    print(f"使用防御强化: {result['message']}")
    
    # 使用法术回复
    result = alice.use_skill("法术回复")
    print(f"使用法术回复: {result['message']}")
    print(f"Alice状态: HP={alice.hp}/{alice.max_hp}, MP={alice.mp}/{alice.max_mp}")
    
    # 测试状态互斥
    print("\n--- 测试状态互斥 ---")
    burn2 = BurnEffect(duration=2, damage_per_turn=15)
    result = bob.add_status_effect(burn2)
    print(f"尝试添加第二个灼烧: {result['message']}")
    
    # 测试状态叠加
    print("\n--- 测试状态叠加 ---")
    defense_buff2 = DefenseBuffEffect(duration=2, defense_bonus=10)
    result = alice.add_status_effect(defense_buff2)
    print(f"叠加防御强化: {result['message']}")
    print(f"Alice防御力: {alice.defense}")
    
    # 测试状态移除
    print("\n--- 测试状态移除 ---")
    result = alice.remove_status_effect("防御强化")
    print(f"移除防御强化: {result['message']}")
    print(f"Alice防御力: {alice.defense}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_status_effects()
