#!/usr/bin/env python3
"""
洛希尔生物系统演示
展示如何使用新创建的洛希尔生物类
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

def demo_creature_exploration():
    """演示生物探索功能"""
    print("🌲 翡翠之森·洛希尔 生物探索演示 🌲")
    print("=" * 60)
    
    # 1. 展示不同栖息地的生物
    habitats = {
        "冠幕层": "canopy",
        "枝桥层": "bridge", 
        "灌草层": "underground",
        "苔根层": "root",
        "幽沼带": "swamp"
    }
    
    print("\n📍 各栖息地生物分布：")
    for habitat_name, habitat_key in habitats.items():
        creatures = get_creatures_by_habitat(habitat_key)
        print(f"\n{habitat_name}:")
        for name, creature_class in creatures.items():
            creature = creature_class(5)
            print(f"  🦌 {name} - 等级{creature.level} - HP{creature.hp}")
    
    # 2. 展示不同等级的生物
    print("\n⚔️ 按等级分类的生物：")
    tiers = ["low", "mid", "high", "legendary"]
    tier_names = ["低级", "中级", "高级", "传说级"]
    
    for tier, name in zip(tiers, tier_names):
        print(f"\n{name}生物示例：")
        for _ in range(2):
            creature = get_random_creature_by_tier(tier)
            if creature:
                print(f"  🐾 {creature.name} - 等级{creature.level}")
    
    # 3. 展示特定生物的详细信息
    print("\n📊 特定生物详细信息：")
    example_creatures = ["星辉织蛛", "影纹豹", "星穹牡鹿"]
    
    for name in example_creatures:
        creature = get_creature_by_name(name, 10)
        info = creature.get_detailed_info()
        print(f"\n🎯 {name}:")
        print(f"  等级: {info['level']}")
        print(f"  类型: {info['type']} - {info['tier']}")
        print(f"  属性: HP{info['hp']}, 攻击{info['attack']}, 防御{info['defense']}")
        print(f"  栖息地: {info['habitat']}")
        print(f"  描述: {info['description']}")
        print(f"  技能: {', '.join(info['skills'])}")
        print(f"  掉落: {len(info['rewards']['items'])}种物品")

def demo_combat_scenario():
    """演示战斗场景"""
    print("\n⚔️ 战斗场景演示")
    print("=" * 60)
    
    # 创建战斗场景
    player_level = 8
    enemy = get_creature_by_name("影纹豹", player_level)
    
    print(f"\n🎯 遭遇敌人: {enemy.name}")
    print(f"   等级: {enemy.level}")
    print(f"   HP: {enemy.hp}/{enemy.max_hp}")
    print(f"   攻击: {enemy.attack}")
    print(f"   防御: {enemy.defense}")
    print(f"   技能: {', '.join([skill.name for skill in enemy.skills])}")
    
    # 模拟战斗
    print("\n🎮 战斗开始！")
    player_hp = 100
    round_num = 1
    
    while player_hp > 0 and enemy.is_alive():
        print(f"\n--- 第{round_num}回合 ---")
        print(f"玩家 HP: {player_hp}")
        print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
        
        # 敌人行动
        action = enemy.select_action(None)  # 简化版，实际应该传入玩家对象
        if action['type'] == 'skill':
            print(f"{enemy.name} 准备使用技能...")
        else:
            damage = action.get('damage', enemy.attack)
            print(f"{enemy.name} 发动攻击，造成 {damage} 点伤害！")
            player_hp -= damage
        
        # 玩家行动（简化）
        player_damage = 25
        print(f"玩家反击，造成 {player_damage} 点伤害！")
        enemy.take_damage(player_damage)
        
        round_num += 1
        
        if round_num > 5:  # 限制回合数
            break
    
    if enemy.is_alive():
        print(f"\n💀 你被 {enemy.name} 击败了！")
    else:
        print(f"\n🎉 你击败了 {enemy.name}！")
        print(f"获得经验: {enemy.experience_reward}")
        print(f"获得金币: {enemy.gold_reward}")
        if enemy.drop_items:
            print("可能掉落物品:")
            for item, rate in enemy.drop_items:
                print(f"  - {item} (概率: {rate*100}%)")

def demo_ecological_system():
    """演示生态系统"""
    print("\n🌿 生态系统演示")
    print("=" * 60)
    
    # 展示生物间的生态关系
    ecosystem = {
        "食物链": {
            "顶级掠食者": ["影纹豹"],
            "中级掠食者": ["光刃隼", "镜沼鹭"],
            "草食动物": ["月轮狍", "苔背貘"],
            "植物": ["风哨藤群", "星藻浮莲", "静语苔"]
        },
        "特殊关系": {
            "精灵盟友": ["影纹豹"],
            "精灵坐骑": ["星穹牡鹿"],
            "精灵工具": ["叶桥甲虫", "星露蚕"]
        }
    }
    
    for category, creatures in ecosystem.items():
        print(f"\n{category}:")
        for role, names in creatures.items():
            print(f"  {role}: {', '.join(names)}")

if __name__ == "__main__":
    print("🌲 洛希尔生物系统完整演示 🌲")
    print("基于《翡翠之森·洛希尔生物志》实现")
    
    try:
        demo_creature_exploration()
        demo_combat_scenario()
        demo_ecological_system()
        
        print("\n" + "=" * 60)
        print("✅ 演示完成！")
        print("🎯 洛希尔生物系统已成功集成到游戏中")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
