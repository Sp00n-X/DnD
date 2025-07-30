#!/usr/bin/env python3
"""
测试洛希尔生物类的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enemy.lothir import (
    get_creature_by_name, 
    get_random_creature_by_tier,
    get_creatures_by_habitat,
    ALL_LOTHIR_CREATURES
)

def test_creature_creation():
    """测试生物创建"""
    print("=== 测试生物创建 ===")
    
    # 测试创建特定生物
    spider = get_creature_by_name("星辉织蛛", 3)
    print(f"创建生物: {spider.get_status()}")
    print(f"详细信息: {spider.get_detailed_info()}")
    print()
    
    # 测试创建传说级生物
    stag = get_creature_by_name("星穹牡鹿", 20)
    print(f"创建传说生物: {stag.get_status()}")
    print(f"传说生物信息: {stag.get_detailed_info()}")
    print()

def test_random_creature():
    """测试随机生物生成"""
    print("=== 测试随机生物生成 ===")
    
    for tier in ["low", "mid", "high", "legendary"]:
        creature = get_random_creature_by_tier(tier)
        if creature:
            print(f"{tier.upper()}级生物: {creature.name} (等级{creature.level})")
    print()

def test_habitat_creatures():
    """测试按栖息地获取生物"""
    print("=== 测试按栖息地获取生物 ===")
    
    habitats = ["canopy", "bridge", "underground", "root", "swamp"]
    for habitat in habitats:
        creatures = get_creatures_by_habitat(habitat)
        print(f"{habitat.upper()}层生物: {list(creatures.keys())}")
    print()

def test_all_creatures():
    """测试所有生物"""
    print("=== 测试所有洛希尔生物 ===")
    
    print(f"总共有 {len(ALL_LOTHIR_CREATURES)} 种洛希尔生物")
    
    # 按层级统计
    from enemy.lothir import LOW_LEVEL_CREATURES, MID_LEVEL_CREATURES, HIGH_LEVEL_CREATURES, LEGENDARY_LEVEL_CREATURES
    
    print(f"低级生物: {len(LOW_LEVEL_CREATURES)} 种")
    print(f"中级生物: {len(MID_LEVEL_CREATURES)} 种")
    print(f"高级生物: {len(HIGH_LEVEL_CREATURES)} 种")
    print(f"传说级生物: {len(LEGENDARY_LEVEL_CREATURES)} 种")
    print()
    
    # 测试每个生物的创建
    print("=== 生物创建测试 ===")
    for name, creature_class in ALL_LOTHIR_CREATURES.items():
        try:
            creature = creature_class(5)  # 用等级5测试
            print(f"✓ {name}: 等级{creature.level}, HP{creature.hp}, 攻击{creature.attack}")
        except Exception as e:
            print(f"✗ {name}: 创建失败 - {e}")

def test_combat_simulation():
    """测试战斗模拟"""
    print("=== 测试战斗模拟 ===")
    
    # 创建两个生物进行简单战斗测试
    spider = get_creature_by_name("星辉织蛛", 3)
    marten = get_creature_by_name("镜羽貂", 3)
    
    print(f"战斗开始: {spider.name} vs {marten.name}")
    
    round_num = 1
    while spider.is_alive() and marten.is_alive():
        print(f"\n--- 第{round_num}回合 ---")
        print(f"{spider.name}: {spider.hp}/{spider.max_hp} HP")
        print(f"{marten.name}: {marten.hp}/{marten.max_hp} HP")
        
        # 蜘蛛攻击
        action = spider.select_action(marten)
        result = spider.execute_action(action)
        print(f"{spider.name}行动: {result['message']}")
        
        if not marten.is_alive():
            break
            
        # 貂攻击
        action = marten.select_action(spider)
        result = marten.execute_action(action)
        print(f"{marten.name}行动: {result['message']}")
        
        round_num += 1
        
        if round_num > 10:  # 防止无限循环
            print("战斗超时结束")
            break
    
    winner = spider.name if spider.is_alive() else marten.name
    print(f"\n战斗结束! 胜利者: {winner}")

if __name__ == "__main__":
    print("🌲 洛希尔生物系统测试 🌲")
    print("=" * 50)
    
    try:
        test_creature_creation()
        test_random_creature()
        test_habitat_creatures()
        test_all_creatures()
        test_combat_simulation()
        
        print("=" * 50)
        print("✅ 所有测试完成!")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
