#!/usr/bin/env python3
"""简化测试新的状态效果系统"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chactors'))

from characters.status_effects import BurnEffect, PoisonEffect, DefenseBuffEffect
from characters.status_effects.status_manager import StatusManager


class MockCharacter:
    """模拟角色类用于测试"""
    def __init__(self, name, hp=100, defense=10):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.defense = defense
        self.status_manager = StatusManager(self)
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    
    def add_status_effect(self, effect):
        return self.status_manager.add_status(effect)
    
    def update_status_effects(self):
        return self.status_manager.update_all()
    
    def get_status_effects(self):
        return self.status_manager.get_status_summary()


def test_status_system():
    """测试状态系统"""
    print("=== 测试新的状态效果系统 ===")
    
    # 创建测试角色
    alice = MockCharacter("Alice", hp=100, defense=10)
    bob = MockCharacter("Bob", hp=100, defense=10)
    
    print(f"初始状态:")
    print(f"Alice: HP={alice.hp}/{alice.max_hp}, Defense={alice.defense}")
    print(f"Bob: HP={bob.hp}/{bob.max_hp}, Defense={bob.defense}")
    
    # 测试灼烧效果
    print("\n--- 测试灼烧效果 ---")
    burn = BurnEffect(duration=3, damage_per_turn=10)
    result = bob.add_status_effect(burn)
    print(f"添加灼烧效果: {result['message']}")
    
    # 测试防御强化
    print("\n--- 测试防御强化 ---")
    defense_buff = DefenseBuffEffect(duration=3, defense_bonus=20)
    result = alice.add_status_effect(defense_buff)
    print(f"添加防御强化: {result['message']}")
    print(f"Alice防御力: {alice.defense}")
    
    # 测试状态更新
    print("\n--- 测试状态更新 ---")
    for turn in range(1, 5):
        print(f"\n第{turn}回合:")
        
        # 更新Bob的状态
        bob_results = bob.update_status_effects()
        for result in bob_results:
            print(f"  Bob: {result['result']['message']}")
        
        # 更新Alice的状态
        alice_results = alice.update_status_effects()
        for result in alice_results:
            print(f"  Alice: {result['result']['message']}")
        
        print(f"  Bob状态: HP={bob.hp}/{bob.max_hp}")
        print(f"  Alice状态: HP={alice.hp}/{alice.max_hp}, Defense={alice.defense}")
    
    # 测试状态叠加
    print("\n--- 测试状态叠加 ---")
    defense_buff2 = DefenseBuffEffect(duration=2, defense_bonus=15)
    result = alice.add_status_effect(defense_buff2)
    print(f"叠加防御强化: {result['message']}")
    print(f"Alice防御力: {alice.defense}")
    
    
    # 测试状态互斥
    print("\n--- 测试状态互斥 ---")
    poison = PoisonEffect(duration=3, percent_per_turn=0.05)
    result = bob.add_status_effect(poison)
    print(f"添加中毒效果: {result['message']}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_status_system()
