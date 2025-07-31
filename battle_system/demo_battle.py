"""战斗系统演示"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from battle_system import BattleEngine, BattleConfig
from characters.base_character import BaseCharacter
from enemy.bosses.boss_manager import BossManager

def demo_simple_battle():
    """演示简单战斗"""
    print("🎮 演示简单战斗")
    print("=" * 50)
    
    # 创建玩家
    from main_process import PlayerCharacter, CharacterClass
    player = PlayerCharacter("测试玩家", CharacterClass.MAGE)
    player.level = 5
    
    # 创建敌人
    enemy = BaseCharacter("哥布林", level=3)
    enemy.max_hp = 50
    enemy.hp = 50
    enemy.attack = 8
    enemy.defense = 2
    
    # 创建战斗引擎
    config = BattleConfig(allow_flee=True, show_detailed_log=True)
    battle = BattleEngine(player, enemy, config)
    
    # 开始战斗
    result = battle.start_battle()
    print(f"\n战斗结果: {result}")
    
    return result

def demo_boss_battle():
    """演示Boss战斗"""
    print("\n🎮 演示Boss战斗")
    print("=" * 50)
    
    # 创建玩家
    from main_process import PlayerCharacter, CharacterClass
    player = PlayerCharacter("勇者", CharacterClass.WARRIOR)
    player.level = 10
    
    # 创建Boss
    boss_manager = BossManager()
    boss = boss_manager.get_boss(1)  # 获取第一层Boss
    
    # 创建战斗引擎
    config = BattleConfig(allow_flee=False, show_detailed_log=True)
    battle = BattleEngine(player, boss, config)
    
    # 开始战斗
    result = battle.start_battle()
    print(f"\n战斗结果: {result}")
    
    return result

def demo_auto_battle():
    """演示自动战斗"""
    print("\n🎮 演示自动战斗")
    print("=" * 50)
    
    # 创建玩家
    from main_process import PlayerCharacter, CharacterClass
    player = PlayerCharacter("自动玩家", CharacterClass.ROGUE)
    player.level = 8
    
    # 创建敌人
    enemy = BaseCharacter("狼人", level=5)
    enemy.max_hp = 80
    enemy.hp = 80
    enemy.attack = 12
    enemy.defense = 4
    
    # 创建战斗引擎
    config = BattleConfig(allow_flee=True, show_detailed_log=False, auto_battle=True)
    battle = BattleEngine(player, enemy, config)
    
    # 开始战斗
    result = battle.start_battle()
    
    # 获取战斗摘要
    summary = battle.get_battle_summary()
    print(f"\n战斗摘要:")
    print(f"结果: {summary['result']}")
    print(f"回合数: {summary['turns']}")
    print(f"获得经验: {summary['rewards']['experience']}")
    
    return result

def main():
    """主函数"""
    print("🎮 战斗系统演示")
    print("=" * 50)
    
    while True:
        print("\n选择演示:")
        print("1. 简单战斗")
        print("2. Boss战斗")
        print("3. 自动战斗")
        print("0. 退出")
        
        choice = input("请选择: ").strip()
        
        if choice == "1":
            demo_simple_battle()
        elif choice == "2":
            demo_boss_battle()
        elif choice == "3":
            demo_auto_battle()
        elif choice == "0":
            break
        else:
            print("❗ 无效选择")

if __name__ == "__main__":
    main()
