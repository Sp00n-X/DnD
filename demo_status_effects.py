#!/usr/bin/env python3
"""演示增强的状态效果系统"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from characters.base_character import BaseCharacter
from status_effects import (
    BurnEffect, PoisonEffect, FreezeEffect, 
    DefenseBuffEffect, AttackBuffEffect, HealOverTimeEffect
)

def demo_enhanced_status_effects():
    """演示增强的状态效果功能"""
    print("=== 增强状态效果系统演示 ===\n")
    
    # 创建角色
    hero = BaseCharacter("英雄", level=10)
    enemy = BaseCharacter("敌人", level=8)
    
    print("初始状态:")
    print(f"{hero.name}: HP={hero.hp}/{hero.max_hp}, 攻击={hero.attack}, 防御={hero.defense}")
    print(f"{enemy.name}: HP={enemy.hp}/{enemy.max_hp}, 攻击={enemy.attack}, 防御={enemy.defense}")
    
    print("\n--- 使用便捷方法添加状态效果 ---")
    
    # 使用便捷方法添加状态效果
    result = hero.apply_status_effect("attack_buff", duration=3, attack_bonus=30)
    print(f"添加攻击强化: {result['message']}")
    
    result = hero.apply_status_effect("defense_buff", duration=3, defense_bonus=20)
    print(f"添加防御强化: {result['message']}")
    
    print(f"\n强化后状态:")
    print(f"{hero.name}: 攻击={hero.attack}, 防御={hero.defense}")
    
    print("\n--- 测试状态效果互斥 ---")
    
    # 测试互斥效果
    result = enemy.apply_status_effect("burn", duration=3, damage_per_turn=15)
    print(f"添加灼烧: {result['message']}")
    
    result = enemy.apply_status_effect("freeze", duration=2)
    print(f"尝试添加冰冻: {result['message']}")
    
    print("\n--- 测试状态效果叠加 ---")
    
    # 测试叠加效果
    result = hero.apply_status_effect("heal_over_time", duration=3, heal_per_turn=25)
    print(f"添加持续治疗: {result['message']}")
    
    # 再次添加相同效果测试叠加
    result = hero.apply_status_effect("heal_over_time", duration=2, heal_per_turn=15)
    print(f"叠加持续治疗: {result['message']}")
    
    print("\n--- 状态效果更新演示 ---")
    
    print("\n第1回合:")
    print(f"敌人状态: HP={enemy.hp}/{enemy.max_hp}")
    print(f"英雄状态: HP={hero.hp}/{hero.max_hp}")
    
    # 更新状态效果
    enemy.update_status_effects()
    hero.update_status_effects()
    
    print("\n状态效果更新后:")
    print(f"敌人状态: HP={enemy.hp}/{enemy.max_hp}")
    print(f"英雄状态: HP={hero.hp}/{hero.max_hp}")
    
    print("\n--- 状态效果查询 ---")
    
    # 查询状态效果
    effects = hero.get_status_effects()
    print(f"英雄当前状态效果数量: {effects['total_effects']}")
    for effect in effects['effects']:
        print(f"  - {effect['name']}: {effect['description']}")
    
    # 检查特定状态
    if hero.has_status_effect("攻击强化"):
        print("✓ 英雄拥有攻击强化效果")
    
    if not enemy.has_status_effect("冰冻"):
        print("✓ 敌人没有冰冻效果（被灼烧互斥）")
    
    print("\n--- 清除所有状态效果 ---")
    
    result = hero.clear_all_status_effects()
    print(f"清除英雄所有状态: {result['message']}")
    
    print(f"\n最终状态:")
    print(f"{hero.name}: 攻击={hero.attack}, 防御={hero.defense}")
    print(f"状态效果数量: {hero.get_status_effects()['total_effects']}")
    
    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    demo_enhanced_status_effects()
